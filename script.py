import os
import shutil
import argparse
import PyPDF2
import difflib
from pathlib import Path
from collections import defaultdict
import concurrent.futures
import time
import re
import hashlib
from PIL import Image
import pdf2image
import io
import tqdm


def get_pdf_metadata(filepath, clean_for_comparison=False):
    """Get the page count and visual hash from a PDF file."""
    try:
        with open(filepath, "rb") as file:
            pdf_bytes = file.read()
            # Get page count from original file
            reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
            page_count = len(reader.pages)

            # Clean PDF for flattened files only if specified
            if clean_for_comparison:
                clean_pdf_bytes = clean_pdf_for_comparison(pdf_bytes)
            else:
                clean_pdf_bytes = pdf_bytes

            # Create visual hash from first 3 pages (or all if fewer than 3)
            visual_hash = ""
            if page_count > 0:
                # Convert PDF pages to images
                pages = []
                try:
                    # Use only first 3 pages (or all if fewer)
                    pages_to_convert = list(range(min(3, page_count)))
                    for page_num in pages_to_convert:
                        # Use cleaned PDF for image conversion
                        pages.extend(
                            pdf2image.convert_from_bytes(
                                clean_pdf_bytes,
                                first_page=page_num + 1,
                                last_page=page_num + 1,
                                dpi=150,  # Higher DPI for better comparison
                            )
                        )
                    # Create visual hash
                    for page_image in pages:
                        # Use larger image size for better comparison
                        small_img = page_image.resize(
                            (64, 64), Image.Resampling.LANCZOS
                        )
                        # Convert to grayscale
                        gray_img = small_img.convert("L")
                        # Get pixel data
                        pixels = list(gray_img.getdata())
                        # Calculate average pixel value
                        avg = sum(pixels) / len(pixels)
                        # Create binary hash
                        bits = "".join("1" if p > avg else "0" for p in pixels)
                        # Convert to hex for easier storage
                        page_hash = hashlib.md5(bits.encode()).hexdigest()
                        visual_hash += page_hash
                except Exception as e:
                    print(f"Visual hash error for {filepath}: {e}")
                    # Fallback to file size if visual hash fails
                    visual_hash = str(os.path.getsize(filepath))
            return {"page_count": page_count, "visual_hash": visual_hash}
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return {"page_count": None, "visual_hash": ""}


def clean_pdf_for_comparison(pdf_bytes):
    """Remove annotations and highlights from the first 3 pages of a PDF before comparison."""
    try:
        reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
        writer = PyPDF2.PdfWriter()

        # Determine how many pages to process (first 3 or all if fewer)
        num_pages = min(3, len(reader.pages))

        # Copy only the first 3 pages without annotations
        for i in range(num_pages):
            page = reader.pages[i]
            writer.add_page(page)
            # Remove annotations if they exist
            if "/Annots" in page:
                writer._objects[writer._pages[-1].indirect_reference.idnum - 1][
                    "/Annots"
                ] = []

        # Write to bytes
        output = io.BytesIO()
        writer.write(output)
        return output.getvalue()
    except Exception as e:
        print(f"Error cleaning PDF: {e}")
        return pdf_bytes  # Return original if cleaning fails


def process_file(args):
    """Process a single file to extract metadata."""
    filepath, base_dir, is_flattened = args
    rel_path = os.path.relpath(filepath, base_dir)
    if filepath.lower().endswith(".pdf"):
        # Only clean PDFs from the flattened directory
        metadata = get_pdf_metadata(filepath, clean_for_comparison=is_flattened)
        return rel_path, {
            "page_count": metadata["page_count"],
            "visual_hash": metadata["visual_hash"],
            "path": filepath,
        }
    return None


def process_directory(directory, is_flattened=False, max_workers=None):
    """Process all PDF files in a directory with parallel execution."""
    files_to_process = []
    # Collect all PDF files
    for root, _, files in os.walk(directory):
        for file in files:
            if file == "Thumbs.db":
                continue
            filepath = os.path.join(root, file)
            if filepath.lower().endswith(".pdf"):
                files_to_process.append((filepath, directory, is_flattened))

    # Process files in parallel
    results = {}
    total_files = len(files_to_process)
    if total_files == 0:
        print(f"No PDF files found in {directory}")
        return results

    print(f"Processing {total_files} PDF files in {directory}...")
    start_time = time.time()

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Use tqdm to create a progress bar
        for result in tqdm.tqdm(
            executor.map(process_file, files_to_process),
            total=total_files,
            desc="Extracting metadata",
            unit="files",
        ):
            if result:
                rel_path, metadata = result
                results[rel_path] = metadata

    elapsed = time.time() - start_time
    files_per_second = total_files / elapsed if elapsed > 0 else 0
    print(
        f"Completed processing {total_files} files in {elapsed:.2f} seconds ({files_per_second:.2f} files/sec)"
    )

    return results


def calculate_hash_similarity(hash1, hash2):
    """Calculate similarity between two visual hashes."""
    # Quick check for empty hashes
    if not hash1 or not hash2:
        return 0.0
    # Calculate Hamming distance for hex strings
    if len(hash1) != len(hash2):
        # If lengths differ, use sequence matcher
        return difflib.SequenceMatcher(None, hash1, hash2).ratio()
    # Convert hex strings to binary
    try:
        bin1 = bin(int(hash1, 16))[2:].zfill(len(hash1) * 4)
        bin2 = bin(int(hash2, 16))[2:].zfill(len(hash2) * 4)
    except ValueError:
        # Fallback if hash is not a valid hex string
        return difflib.SequenceMatcher(None, hash1, hash2).ratio()
    # Calculate Hamming distance
    distance = sum(b1 != b2 for b1, b2 in zip(bin1, bin2))
    max_distance = len(bin1)
    # Convert distance to similarity (0-1)
    return 1 - (distance / max_distance)


def match_files_by_metadata(
    flattened_dir,
    original_dir,
    output_dir=None,
    dry_run=True,
    similarity_threshold=0.7,
    max_workers=None,
):
    """
    Match files in the flattened directory to files in the original directory structure
    based on page count and visual similarity in PDF files.
    """
    # Process directories in parallel
    print("Scanning directories...")
    original_files = process_directory(
        original_dir, is_flattened=False, max_workers=max_workers
    )
    flattened_files = process_directory(
        flattened_dir, is_flattened=True, max_workers=max_workers
    )

    # Group original files by page count for faster lookup
    original_by_page_count = defaultdict(list)
    for rel_path, metadata in original_files.items():
        page_count = metadata["page_count"]
        if page_count is not None:
            original_by_page_count[page_count].append(rel_path)

    # Match files based on page count and visual similarity
    matches = []
    ambiguous = []
    resolved_by_visual = []
    unmatched = []

    print(f"\nMatching files...")
    start_time = time.time()

    # Pre-calculate similarity for ambiguous matches
    ambiguous_matches_data = []

    # First pass - identify unique matches and collect ambiguous ones
    for flat_file, flat_info in tqdm.tqdm(
        flattened_files.items(), desc="Identifying matches", unit="files"
    ):
        page_count = flat_info["page_count"]
        if page_count is None:
            unmatched.append(flat_file)
            continue

        matching_originals = original_by_page_count.get(page_count, [])
        if len(matching_originals) == 1:
            # Unique match based on page count
            matches.append((flat_file, matching_originals[0]))
        elif len(matching_originals) > 1:
            # Multiple possible matches - collect for later visual similarity processing
            ambiguous_matches_data.append((flat_file, flat_info, matching_originals))
        else:
            # No match found based on page count
            unmatched.append(flat_file)

    # Process ambiguous matches with visual similarity
    print(
        f"Resolving {len(ambiguous_matches_data)} ambiguous matches using visual similarity..."
    )

    for flat_file, flat_info, matching_originals in tqdm.tqdm(
        ambiguous_matches_data, desc="Resolving ambiguous matches", unit="files"
    ):
        flat_hash = flat_info["visual_hash"]
        best_match = None
        best_similarity = 0

        for orig_rel_path in matching_originals:
            orig_hash = original_files[orig_rel_path]["visual_hash"]
            similarity = calculate_hash_similarity(flat_hash, orig_hash)
            if similarity > best_similarity:
                best_similarity = similarity
                best_match = orig_rel_path

        if best_similarity >= similarity_threshold:
            resolved_by_visual.append((flat_file, best_match, best_similarity))
        else:
            ambiguous.append((flat_file, matching_originals))

    # Print results
    print(f"\nMatching Results:")
    print(f"  Total processing time: {time.time() - start_time:.2f} seconds")
    print(f"  Unique matches by page count: {len(matches)}")
    print(f"  Matches resolved by visual similarity: {len(resolved_by_visual)}")
    print(f"  Ambiguous matches: {len(ambiguous)}")
    print(f"  Unmatched files: {len(unmatched)}")

    # Print detailed information
    if matches:
        print("\nUnique Matches by Page Count (showing first 10):")
        for i, (flat_file, orig_file) in enumerate(matches[:10]):
            print(f"  {flat_file} -> {orig_file}")
        if len(matches) > 10:
            print(f"  ... and {len(matches) - 10} more")

    if resolved_by_visual:
        print("\nMatches Resolved by Visual Similarity (showing first 10):")
        for i, (flat_file, orig_file, similarity) in enumerate(resolved_by_visual[:10]):
            print(f"  {flat_file} -> {orig_file} (similarity: {similarity:.2f})")
        if len(resolved_by_visual) > 10:
            print(f"  ... and {len(resolved_by_visual) - 10} more")

    if ambiguous:
        print("\nAmbiguous Matches (showing first 5):")
        for i, (flat_file, candidates) in enumerate(ambiguous[:5]):
            print(f"  {flat_file} has {len(candidates)} possible matches:")
            for j, candidate in enumerate(candidates[:3]):
                print(f"    - {candidate}")
            if len(candidates) > 3:
                print(f"    ... and {len(candidates) - 3} more")
        if len(ambiguous) > 5:
            print(f"  ... and {len(ambiguous) - 5} more ambiguous files")

    if unmatched:
        print("\nUnmatched Files (showing first 10):")
        for i, flat_file in enumerate(unmatched[:10]):
            print(f"  {flat_file}")
        if len(unmatched) > 10:
            print(f"  ... and {len(unmatched) - 10} more")

    # Combine all confirmed matches
    all_matches = matches + [(flat, orig) for flat, orig, _ in resolved_by_visual]

    # If not a dry run and output directory is provided, copy matched files
    if not dry_run and output_dir:
        print(f"\nCopying {len(all_matches)} matched files to {output_dir}...")
        os.makedirs(output_dir, exist_ok=True)

        for flat_file, orig_file in tqdm.tqdm(
            all_matches, desc="Copying files", unit="files"
        ):
            source = os.path.join(flattened_dir, flat_file)
            target = os.path.join(output_dir, orig_file)

            # Create directory structure
            os.makedirs(os.path.dirname(target), exist_ok=True)

            # Copy the file
            try:
                shutil.copy2(source, target)
            except Exception as e:
                print(f"Error copying {flat_file} to {orig_file}: {e}")

        print(
            f"Restoration complete. {len(all_matches)} files restored to {output_dir}"
        )
    elif dry_run:
        print("\nDry run completed. No files were copied.")

    return all_matches, ambiguous, unmatched


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Match files between flattened and original directories based on metadata and visual similarity."
    )
    parser.add_argument(
        "-f", "--flattened", required=True, help="Path to the flattened directory"
    )
    parser.add_argument(
        "-o",
        "--original",
        required=True,
        help="Path to the original directory structure",
    )
    parser.add_argument(
        "-r",
        "--restore",
        help="Path to restore matched files (if not provided, performs dry run only)",
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Execute the restoration (without this flag, performs dry run only)",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.9,
        help="Similarity threshold for visual matching (0.0-1.0, default: 0.9)",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=None,
        help="Maximum number of worker threads (default: CPU count)",
    )
    args = parser.parse_args()

    # Validate similarity threshold
    if args.threshold < 0 or args.threshold > 1:
        parser.error("Similarity threshold must be between 0.0 and 1.0")

    # Resolve paths
    flattened_dir = os.path.abspath(args.flattened)
    original_dir = os.path.abspath(args.original)
    output_dir = os.path.abspath(args.restore) if args.restore else None

    print(f"Flattened directory: {flattened_dir}")
    print(f"Original directory: {original_dir}")
    if output_dir:
        print(f"Output directory: {output_dir}")
    print(f"Similarity threshold: {args.threshold}")
    print(f"Worker threads: {args.workers or 'Auto'}")
    print(f"Mode: {'Execution' if args.execute and output_dir else 'Dry run'}")
    print("-" * 50)

    match_files_by_metadata(
        flattened_dir,
        original_dir,
        output_dir=output_dir,
        dry_run=not (args.execute and output_dir),
        similarity_threshold=args.threshold,
        max_workers=args.workers,
    )
