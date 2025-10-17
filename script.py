import os
import shutil
import argparse
import PyPDF2
import tqdm
from concurrent.futures import ThreadPoolExecutor
import re
import json
import hashlib
import time
import numpy as np
import io
from PIL import Image
import fitz  # PyMuPDF
import tempfile  # <-- Add this import


def get_cache_path(directory):
    """Generate a cache file path for a given directory."""
    # Create a hash of the directory path to use in the cache filename
    dir_hash = hashlib.md5(directory.encode()).hexdigest()[:10]
    cache_dir = os.path.join(os.path.expanduser("~"), ".pdf_matcher_cache")
    os.makedirs(cache_dir, exist_ok=True)
    return os.path.join(cache_dir, f"metadata_cache_{dir_hash}.json")


def load_cache(cache_path):
    """Load cached metadata if it exists."""
    if os.path.exists(cache_path):
        try:
            with open(cache_path, "r") as f:
                cache_data = json.load(f)
                # Check if cache format is valid
                if isinstance(cache_data, dict) and "metadata" in cache_data:
                    print(f"Loaded cache from {cache_path}")
                    return cache_data
        except Exception as e:
            print(f"Error loading cache: {e}")
    return {"metadata": {}, "timestamp": time.time()}


def save_cache(cache_path, cache_data):
    """Save metadata to cache file."""
    try:
        with open(cache_path, "w") as f:
            json.dump(cache_data, f)
        print(f"Saved cache to {cache_path}")
    except Exception as e:
        print(f"Error saving cache: {e}")


def extract_first_page_text(filepath):
    """Extract text from the first page of a PDF file."""
    try:
        with open(filepath, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            if len(reader.pages) > 0:
                # Extract text from the first page
                text = reader.pages[0].extract_text()
                # Clean the text (remove extra whitespace, etc.)
                text = re.sub(r"\s+", " ", text).strip()
                return text
            return ""
    except Exception as e:
        print(f"Error extracting text from {filepath}: {e}")
        return ""


def get_first_page_image(filepath, dpi=72):
    """Extract the first page of a PDF as an image."""
    try:
        doc = fitz.open(filepath)
        if len(doc) > 0:
            page = doc[0]
            pix = page.get_pixmap(matrix=fitz.Matrix(dpi / 72, dpi / 72))
            img_data = pix.tobytes("png")
            img = Image.open(io.BytesIO(img_data))
            # Convert to grayscale and resize to standardize
            img = img.convert("L").resize((300, 300), Image.LANCZOS)
            return np.array(img)
        return None
    except Exception as e:
        print(f"Error extracting image from {filepath}: {e}")
        return None


def calculate_image_similarity(img1, img2):
    """Calculate similarity between two images using MSE."""
    if img1 is None or img2 is None:
        return 0.0

    # Ensure both images have the same dimensions
    if img1.shape != img2.shape:
        return 0.0

    # Calculate Mean Squared Error
    mse = np.mean((img1.astype(float) - img2.astype(float)) ** 2)
    if mse == 0:
        return 1.0  # Images are identical

    # Convert MSE to similarity score (1.0 = identical, 0.0 = completely different)
    # Using exponential decay function to map MSE to similarity
    max_mse = 10000  # Adjust based on your image characteristics
    similarity = np.exp(-mse / max_mse)
    return similarity


def remove_annotations(pdf_path, temp_output_path):
    """Create a copy of the PDF with all annotations removed."""
    try:
        reader = PyPDF2.PdfReader(pdf_path)
        writer = PyPDF2.PdfWriter()
        for page in reader.pages:
            new_page = writer.add_page(page)
            # Remove annotations if present
            if '/Annots' in new_page:
                del new_page['/Annots']
        with open(temp_output_path, 'wb') as output_file:
            writer.write(output_file)
        return temp_output_path
    except Exception as e:
        print(f"Error removing annotations from {pdf_path}: {e}")
        return pdf_path  # Fallback to original if error


def get_first_page_image_without_annotations(filepath, dpi=72):
    """Extract the first page image with annotations removed."""
    temp_path = os.path.join(tempfile.gettempdir(), f"temp_{os.path.basename(filepath)}")
    try:
        cleaned_pdf = remove_annotations(filepath, temp_path)
        img = get_first_page_image(cleaned_pdf, dpi)
        if os.path.exists(temp_path):
            os.remove(temp_path)
        return img
    except Exception as e:
        print(f"Error removing annotations: {e}")
        return get_first_page_image(filepath, dpi)


def extract_first_page_text_improved(filepath):
    """Extract text from first page with better handling of annotations."""
    try:
        doc = fitz.open(filepath)
        if len(doc) > 0:
            text = doc[0].get_text()
            return re.sub(r"\s+", " ", text).strip()
        return ""
    except Exception as e:
        print(f"Error extracting text: {e}")
        return ""


def get_pdf_metadata(filepath, extract_image=False):
    """Get the page count, first page text, and optionally first page image of a PDF file."""
    try:
        # Use improved text extraction
        page_count = 0
        first_page_text = ""
        with open(filepath, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            page_count = len(reader.pages)
        if page_count > 0:
            first_page_text = extract_first_page_text_improved(filepath)
        metadata = {
            "page_count": page_count,
            "first_page_text": first_page_text,
            "path": filepath,
            "mtime": os.path.getmtime(filepath),
            "first_page_image": None,
        }
        if extract_image and page_count > 0:
            metadata["first_page_image"] = True
        return metadata
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return {
            "page_count": None,
            "first_page_text": "",
            "path": filepath,
            "mtime": os.path.getmtime(filepath) if os.path.exists(filepath) else 0,
            "first_page_image": None,
        }


def process_file(args):
    """Process a single file to extract metadata."""
    filepath, base_dir, cache, extract_image = args
    rel_path = os.path.relpath(filepath, base_dir)

    # Check if file is in cache and hasn't been modified
    current_mtime = os.path.getmtime(filepath)
    if rel_path in cache and cache[rel_path].get("mtime", 0) == current_mtime:
        return rel_path, cache[rel_path]

    if filepath.lower().endswith(".pdf"):
        metadata = get_pdf_metadata(filepath, extract_image=extract_image)
        return rel_path, metadata
    return None


def process_directory(
    directory, max_workers=None, use_cache=True, extract_images=False
):
    """Process all PDF files in a directory with parallel execution."""
    cache_path = get_cache_path(directory)
    cache_data = (
        load_cache(cache_path)
        if use_cache
        else {"metadata": {}, "timestamp": time.time()}
    )
    cached_metadata = cache_data["metadata"]

    files_to_process = []
    # Collect all PDF files
    for root, _, files in os.walk(directory):
        for file in files:
            if file == "Thumbs.db":
                continue
            filepath = os.path.join(root, file)
            if filepath.lower().endswith(".pdf"):
                files_to_process.append(
                    (filepath, directory, cached_metadata, extract_images)
                )

    # Process files in parallel
    results = {}
    total_files = len(files_to_process)
    if total_files == 0:
        print(f"No PDF files found in {directory}")
        return results

    print(f"Processing {total_files} PDF files in {directory}...")
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for result in tqdm.tqdm(
            executor.map(process_file, files_to_process),
            total=total_files,
            desc="Extracting metadata",
            unit="files",
        ):
            if result:
                rel_path, metadata = result
                results[rel_path] = metadata

    # Update cache with new results
    if use_cache:
        cache_data["metadata"] = results
        cache_data["timestamp"] = time.time()
        save_cache(cache_path, cache_data)

    return results


def calculate_text_similarity(text1, text2):
    """Calculate similarity between two text strings."""
    if not text1 or not text2:
        return 0.0
    # Convert to lowercase for better matching
    text1 = text1.lower()
    text2 = text2.lower()
    # Find the longest common substring
    words1 = text1.split()
    words2 = text2.split()
    # If either text is very short, require an exact match
    if len(words1) < 5 or len(words2) < 5:
        return 1.0 if text1 == text2 else 0.0
    # Count matching words
    common_words = set(words1) & set(words2)
    # Calculate Jaccard similarity
    similarity = len(common_words) / (len(set(words1) | set(words2)))
    return similarity


def match_files_by_metadata(
    flattened_dir,
    original_dir,
    output_dir=None,
    dry_run=True,
    text_similarity_threshold=0.7,
    image_similarity_threshold=0.99,
    max_workers=None,
    use_cache=True,
):
    """Match files based on page count, text content, and visual similarity."""
    # Process directories in parallel
    print("Scanning directories...")
    original_files = process_directory(
        original_dir, max_workers=max_workers, use_cache=use_cache, extract_images=False
    )
    flattened_files = process_directory(
        flattened_dir,
        max_workers=max_workers,
        use_cache=use_cache,
        extract_images=False,
    )

    # Match files based on page count and text similarity
    matches = []
    text_matches = []
    image_matches = []
    ambiguous = []
    unmatched = []

    print(f"\nMatching files...")
    for flat_file, flat_info in tqdm.tqdm(
        flattened_files.items(), desc="Identifying matches", unit="files"
    ):
        page_count = flat_info["page_count"]
        if page_count is None:
            unmatched.append(flat_file)
            continue

        # Find all original files with the same page count
        matching_originals = []
        for orig_file, orig_info in original_files.items():
            if orig_info["page_count"] == page_count:
                matching_originals.append((orig_file, orig_info))

        if len(matching_originals) == 0:
            unmatched.append(flat_file)
        elif len(matching_originals) == 1:
            # Single match based on page count
            matches.append((flat_file, matching_originals[0][0]))
        else:
            # Multiple matches - try to resolve using first page text
            best_match = None
            best_similarity = 0
            flat_text = flat_info["first_page_text"]

            for orig_file, orig_info in matching_originals:
                orig_text = orig_info["first_page_text"]
                similarity = calculate_text_similarity(flat_text, orig_text)
                if similarity > best_similarity:
                    best_similarity = similarity
                    best_match = orig_file

            if best_similarity >= text_similarity_threshold:
                text_matches.append((flat_file, best_match, best_similarity))
            else:
                # If no good text match, mark for visual comparison
                ambiguous.append((flat_file, [o[0] for o in matching_originals]))

    # Try to resolve ambiguous matches with visual similarity
    if ambiguous:
        print(
            f"\nAttempting to resolve {len(ambiguous)} ambiguous matches using visual similarity..."
        )
        resolved_ambiguous = []

        for flat_file, possible_matches in tqdm.tqdm(
            ambiguous, desc="Visual comparison", unit="files"
        ):
            flat_path = os.path.join(flattened_dir, flat_file)
            # Use cleaned image for comparison
            flat_image = get_first_page_image_without_annotations(flat_path)

            if flat_image is None:
                continue

            best_match = None
            best_similarity = 0

            for orig_file in possible_matches:
                orig_path = os.path.join(original_dir, orig_file)
                orig_image = get_first_page_image_without_annotations(orig_path)

                if orig_image is None:
                    continue

                similarity = calculate_image_similarity(flat_image, orig_image)
                if similarity > best_similarity:
                    best_similarity = similarity
                    best_match = orig_file

            if best_similarity >= image_similarity_threshold:
                image_matches.append((flat_file, best_match, best_similarity))
                resolved_ambiguous.append(flat_file)

        # Remove resolved files from ambiguous list
        ambiguous = [(f, m) for f, m in ambiguous if f not in resolved_ambiguous]

    # Combine all matches
    all_matches = (
        matches
        + [(flat, orig) for flat, orig, _ in text_matches]
        + [(flat, orig) for flat, orig, _ in image_matches]
    )

    # Print results
    print(f"\nMatching Results:")
    print(f"  Unique matches by page count: {len(matches)}")
    print(f"  Matches resolved by text similarity: {len(text_matches)}")
    print(f"  Matches resolved by visual similarity: {len(image_matches)}")
    print(f"  Total matches: {len(all_matches)}")
    print(f"  Remaining ambiguous matches: {len(ambiguous)}")
    print(f"  Unmatched files: {len(unmatched)}")

    # Print detailed information
    if matches:
        print("\nUnique Matches by Page Count (showing first 10):")
        for i, (flat_file, orig_file) in enumerate(matches[:10]):
            print(f"  {flat_file} -> {orig_file}")
        if len(matches) > 10:
            print(f"  ... and {len(matches) - 10} more")

    if text_matches:
        print("\nMatches Resolved by Text Similarity (showing first 10):")
        for i, (flat_file, orig_file, similarity) in enumerate(text_matches[:10]):
            print(f"  {flat_file} -> {orig_file} (similarity: {similarity:.2f})")
        if len(text_matches) > 10:
            print(f"  ... and {len(text_matches) - 10} more")

    if image_matches:
        print("\nMatches Resolved by Visual Similarity (showing first 10):")
        for i, (flat_file, orig_file, similarity) in enumerate(image_matches[:10]):
            print(f"  {flat_file} -> {orig_file} (similarity: {similarity:.2f})")
        if len(image_matches) > 10:
            print(f"  ... and {len(image_matches) - 10} more")

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
        description="Match files between flattened and original directories based on page count, text content, and visual similarity."
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
        "--text-threshold",
        type=float,
        default=0.7,
        help="Text similarity threshold for matching (0.0-1.0, default: 0.7)",
    )
    parser.add_argument(
        "--image-threshold",
        type=float,
        default=0.99,
        help="Visual similarity threshold for matching (0.0-1.0, default: 0.99)",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=None,
        help="Maximum number of worker threads (default: CPU count)",
    )
    parser.add_argument(
        "--no-cache",
        action="store_true",
        help="Disable metadata caching (slower but ensures fresh data)",
    )
    args = parser.parse_args()

    # Validate similarity thresholds
    if args.text_threshold < 0 or args.text_threshold > 1:
        parser.error("Text similarity threshold must be between 0.0 and 1.0")
    if args.image_threshold < 0 or args.image_threshold > 1:
        parser.error("Image similarity threshold must be between 0.0 and 1.0")

    # Resolve paths
    flattened_dir = os.path.abspath(args.flattened)
    original_dir = os.path.abspath(args.original)
    output_dir = os.path.abspath(args.restore) if args.restore else None

    print(f"Flattened directory: {flattened_dir}")
    print(f"Original directory: {original_dir}")
    if output_dir:
        print(f"Output directory: {output_dir}")
    print(f"Text similarity threshold: {args.text_threshold}")
    print(f"Image similarity threshold: {args.image_threshold}")
    print(f"Worker threads: {args.workers or 'Auto'}")
    print(f"Caching: {'Disabled' if args.no_cache else 'Enabled'}")
    print(f"Mode: {'Execution' if args.execute and output_dir else 'Dry run'}")
    print("-" * 50)

    match_files_by_metadata(
        flattened_dir,
        original_dir,
        output_dir=output_dir,
        dry_run=not (args.execute and output_dir),
        text_similarity_threshold=args.text_threshold,
        image_similarity_threshold=args.image_threshold,
        max_workers=args.workers,
        use_cache=not args.no_cache,
    )
