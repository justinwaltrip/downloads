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
import pytesseract
from PIL import Image
import pdf2image


def get_pdf_metadata(filepath):
    """Get the page count and extract sample text from a PDF file using OCR."""
    try:
        with open(filepath, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            page_count = len(reader.pages)

            # Extract text using OCR from first and last page only
            sample_text = ""
            if page_count > 0:
                # Convert PDF pages to images
                pages = []
                try:
                    # Only convert first and last page
                    pages_to_convert = [0]
                    if page_count > 1:
                        pages_to_convert.append(page_count - 1)

                    for page_num in pages_to_convert:
                        pages.extend(
                            pdf2image.convert_from_path(
                                filepath,
                                first_page=page_num + 1,
                                last_page=page_num + 1,
                                dpi=200,  # Lower DPI for faster processing
                            )
                        )

                    # Extract text using OCR
                    for page_image in pages:
                        page_text = pytesseract.image_to_string(page_image)
                        sample_text += page_text + " "
                except Exception as e:
                    print(f"OCR error for {filepath}: {e}")
                    # Fallback to PyPDF2 if OCR fails
                    if page_count > 0:
                        sample_text += reader.pages[0].extract_text() or ""
                        if page_count > 1:
                            sample_text += reader.pages[-1].extract_text() or ""

            # Clean and normalize text
            sample_text = re.sub(r"\s+", " ", sample_text).strip()
            return {"page_count": page_count, "sample_text": sample_text}
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return {"page_count": None, "sample_text": ""}


def process_file(args):
    """Process a single file to extract metadata."""
    filepath, base_dir = args
    rel_path = os.path.relpath(filepath, base_dir)

    if filepath.lower().endswith(".pdf"):
        metadata = get_pdf_metadata(filepath)
        return rel_path, {
            "page_count": metadata["page_count"],
            "sample_text": metadata["sample_text"],
            "path": filepath,
        }
    return None


def process_directory(directory, max_workers=None):
    """Process all PDF files in a directory with parallel execution."""
    files_to_process = []

    # Collect all PDF files
    for root, _, files in os.walk(directory):
        for file in files:
            if file == "Thumbs.db":
                continue

            filepath = os.path.join(root, file)
            if filepath.lower().endswith(".pdf"):
                files_to_process.append((filepath, directory))

    # Process files in parallel
    results = {}
    total_files = len(files_to_process)

    if total_files == 0:
        print(f"No PDF files found in {directory}")
        return results

    print(f"Processing {total_files} PDF files in {directory}...")

    start_time = time.time()
    processed = 0

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        for result in executor.map(process_file, files_to_process):
            if result:
                rel_path, metadata = result
                results[rel_path] = metadata

                processed += 1
                if processed % 10 == 0 or processed == total_files:
                    elapsed = time.time() - start_time
                    files_per_second = processed / elapsed if elapsed > 0 else 0
                    print(
                        f"Processed {processed}/{total_files} files ({files_per_second:.2f} files/sec)",
                        end="\r",
                    )

    print(
        f"\nCompleted processing {processed} files in {time.time() - start_time:.2f} seconds"
    )
    return results


def calculate_text_similarity(text1, text2):
    """Calculate similarity ratio between two text strings."""
    # Quick check for empty texts
    if not text1 or not text2:
        return 0.0

    # Use a faster comparison for long texts
    if len(text1) > 1000 and len(text2) > 1000:
        # Create sets of words for faster comparison of large texts
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())

        # Jaccard similarity
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))

        return intersection / union if union > 0 else 0.0
    else:
        # Use sequence matcher for shorter texts
        return difflib.SequenceMatcher(None, text1, text2).ratio()


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
    based on page count and text similarity in PDF files.

    Args:
        flattened_dir (str): Path to the flattened directory
        original_dir (str): Path to the original directory
        output_dir (str): Path to the output directory for restored files
        dry_run (bool): If True, only report matches without copying files
        similarity_threshold (float): Minimum similarity ratio to consider a match (0.0 to 1.0)
        max_workers (int): Maximum number of worker threads for parallel processing
    """
    # Process directories in parallel
    print("Scanning directories...")
    original_files = process_directory(original_dir, max_workers)
    flattened_files = process_directory(flattened_dir, max_workers)

    # Group original files by page count for faster lookup
    original_by_page_count = defaultdict(list)
    for rel_path, metadata in original_files.items():
        page_count = metadata["page_count"]
        if page_count is not None:
            original_by_page_count[page_count].append(rel_path)

    # Match files based on page count and text similarity
    matches = []
    ambiguous = []
    resolved_by_text = []
    unmatched = []

    print(f"\nMatching files...")
    total_flat_files = len(flattened_files)
    start_time = time.time()

    # Pre-calculate similarity for ambiguous matches
    ambiguous_matches_data = []

    for i, (flat_file, flat_info) in enumerate(flattened_files.items()):
        if i % 10 == 0 or i == total_flat_files - 1:
            print(f"Processing file {i+1}/{total_flat_files}", end="\r")

        page_count = flat_info["page_count"]
        if page_count is None:
            unmatched.append(flat_file)
            continue

        matching_originals = original_by_page_count.get(page_count, [])

        if len(matching_originals) == 1:
            # Unique match based on page count
            matches.append((flat_file, matching_originals[0]))
        elif len(matching_originals) > 1:
            # Multiple possible matches - collect for later text similarity processing
            ambiguous_matches_data.append((flat_file, flat_info, matching_originals))
        else:
            # No match found based on page count
            unmatched.append(flat_file)

    # Process ambiguous matches with text similarity
    print(
        f"\nResolving {len(ambiguous_matches_data)} ambiguous matches using text similarity..."
    )

    for idx, (flat_file, flat_info, matching_originals) in enumerate(
        ambiguous_matches_data
    ):
        if idx % 10 == 0 or idx == len(ambiguous_matches_data) - 1:
            print(
                f"Processing ambiguous match {idx+1}/{len(ambiguous_matches_data)}",
                end="\r",
            )

        flat_text = flat_info["sample_text"]

        best_match = None
        best_similarity = 0

        for orig_rel_path in matching_originals:
            orig_text = original_files[orig_rel_path]["sample_text"]
            similarity = calculate_text_similarity(flat_text, orig_text)

            if similarity > best_similarity:
                best_similarity = similarity
                best_match = orig_rel_path

        if best_similarity >= similarity_threshold:
            resolved_by_text.append((flat_file, best_match, best_similarity))
        else:
            ambiguous.append((flat_file, matching_originals))

    print(" " * 80, end="\r")  # Clear the processing line

    # Print results
    print(f"\nMatching Results:")
    print(f"  Total processing time: {time.time() - start_time:.2f} seconds")
    print(f"  Unique matches by page count: {len(matches)}")
    print(f"  Matches resolved by text similarity: {len(resolved_by_text)}")
    print(f"  Ambiguous matches: {len(ambiguous)}")
    print(f"  Unmatched files: {len(unmatched)}")

    # Print detailed information
    if matches:
        print("\nUnique Matches by Page Count (showing first 10):")
        for i, (flat_file, orig_file) in enumerate(matches[:10]):
            print(f"  {flat_file} -> {orig_file}")
        if len(matches) > 10:
            print(f"  ... and {len(matches) - 10} more")

    if resolved_by_text:
        print("\nMatches Resolved by Text Similarity (showing first 10):")
        for i, (flat_file, orig_file, similarity) in enumerate(resolved_by_text[:10]):
            print(f"  {flat_file} -> {orig_file} (similarity: {similarity:.2f})")
        if len(resolved_by_text) > 10:
            print(f"  ... and {len(resolved_by_text) - 10} more")

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
    all_matches = matches + [(flat, orig) for flat, orig, _ in resolved_by_text]

    # If not a dry run and output directory is provided, copy matched files
    if not dry_run and output_dir:
        print(f"\nCopying {len(all_matches)} matched files to {output_dir}...")
        os.makedirs(output_dir, exist_ok=True)

        copied = 0
        for flat_file, orig_file in all_matches:
            source = os.path.join(flattened_dir, flat_file)
            target = os.path.join(output_dir, orig_file)

            # Create directory structure
            os.makedirs(os.path.dirname(target), exist_ok=True)

            # Copy the file
            try:
                shutil.copy2(source, target)
                copied += 1
                if copied % 20 == 0 or copied == len(all_matches):
                    print(f"Copied {copied}/{len(all_matches)} files", end="\r")
            except Exception as e:
                print(f"Error copying {flat_file} to {orig_file}: {e}")

        print(f"\nRestoration complete. {copied} files restored to {output_dir}")
    elif dry_run:
        print("\nDry run completed. No files were copied.")

    return all_matches, ambiguous, unmatched


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Match files between flattened and original directories based on metadata and text similarity."
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
        help="Similarity threshold for text matching (0.0-1.0, default: 0.7)",
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
