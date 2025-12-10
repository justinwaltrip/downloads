import os
import shutil
import uuid
import json
import argparse


def flatten_directory(source_dir, target_dir, mapping_file_path):
    """
    Flattens a directory structure by:
    1. Creating a new target directory
    2. Copying all files to the target directory with UUID filenames
    3. Creating a mapping file that links UUID filenames to original paths
    Args:
        source_dir (str): Path to the source directory
        target_dir (str): Path to the target directory
        mapping_file_path (str): Path to save the mapping JSON file
    """
    # Create target directory if it doesn't exist
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    # Dictionary to store mapping of UUID to original filepath
    file_mapping = {}
    # Walk through the source directory
    for root, _, files in os.walk(source_dir):
        for file in files:
            # Skip Thumbs.db files
            if file == "Thumbs.db":
                continue
            # Get the full path of the source file
            source_path = os.path.join(root, file)
            # Generate a UUID for the new filename
            new_filename = str(uuid.uuid4())
            # Get the file extension
            _, file_extension = os.path.splitext(file)
            # Create the new filename with the original extension
            new_filename_with_ext = new_filename + file_extension
            # Path to the new file in the target directory
            target_path = os.path.join(target_dir, new_filename_with_ext)
            # Copy the file to the target directory
            shutil.copy2(source_path, target_path)
            # Store the mapping
            relative_source_path = os.path.relpath(source_path, source_dir)
            file_mapping[new_filename_with_ext] = relative_source_path
            print(f"Copied: {relative_source_path} -> {new_filename_with_ext}")
    # Write the mapping to a JSON file
    with open(mapping_file_path, "w") as f:
        json.dump(file_mapping, f, indent=4)
    print(f"\nFlattening complete. Mapping stored in {mapping_file_path}")
    print(f"Total files processed: {len(file_mapping)}")


def unflatten_directory(flattened_dir, output_dir, mapping_file_path):
    """
    Unflattens a directory structure using a mapping file:
    1. Creates the original directory structure
    2. Copies files from the flattened directory to their original locations

    Args:
        flattened_dir (str): Path to the flattened directory
        output_dir (str): Path to the output directory
        mapping_file_path (str): Path to the mapping JSON file
    """
    # Check if the mapping file exists
    if not os.path.exists(mapping_file_path):
        print(f"Error: Mapping file {mapping_file_path} does not exist.")
        return

    # Load the mapping file
    with open(mapping_file_path, "r") as f:
        file_mapping = json.load(f)

    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Process each file in the mapping
    files_processed = 0
    for uuid_filename, original_path in file_mapping.items():
        # Source file in flattened directory
        source_file = os.path.join(flattened_dir, uuid_filename)

        # Target file in output directory
        target_file = os.path.join(output_dir, original_path)

        # Create the directory structure if it doesn't exist
        os.makedirs(os.path.dirname(target_file), exist_ok=True)

        # Copy the file if it exists
        if os.path.exists(source_file):
            shutil.copy2(source_file, target_file)
            print(f"Restored: {uuid_filename} -> {original_path}")
            files_processed += 1
        else:
            print(f"Warning: {uuid_filename} not found in flattened directory")

    print(f"\nUnflattening complete. Files restored to {output_dir}")
    print(f"Total files processed: {files_processed}")


if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(
        description="Flatten or unflatten a directory structure and create/use a mapping file."
    )
    # Define arguments
    parser.add_argument(
        "-s",
        "--source",
        help="Source directory to flatten (default: ./VenueMarketableBatch2)",
        default="VenueMarketableBatch2",
    )
    parser.add_argument(
        "-t",
        "--target",
        help="Target directory for flattened files (default: ./VenueMarketableBatch2_Flattened)",
        default="VenueMarketableBatch2_Flattened",
    )
    parser.add_argument(
        "-m",
        "--mapping",
        help="Path for the mapping JSON file (default: ./VenueMarketableBatch2.json)",
        default="VenueMarketableBatch2.json",
    )
    parser.add_argument(
        "-u",
        "--unflatten",
        action="store_true",
        help="Unflatten the directory structure using the mapping file",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Output directory for unflattened files (default: ./VenueMarketableBatch2_Restored)",
        default="VenueMarketableBatch2_Restored",
    )

    # Parse arguments
    args = parser.parse_args()

    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Resolve paths (use absolute paths if provided, otherwise relative to current dir)
    source_directory = os.path.abspath(args.source)
    target_directory = os.path.abspath(args.target)
    mapping_file_path = os.path.abspath(args.mapping)
    output_directory = os.path.abspath(args.output)

    if args.unflatten:
        # Unflatten mode
        print(f"Flattened directory: {source_directory}")
        print(f"Output directory: {output_directory}")
        print(f"Mapping file: {mapping_file_path}")
        print("-" * 50)
        unflatten_directory(source_directory, output_directory, mapping_file_path)
    else:
        # Flatten mode
        print(f"Source directory: {source_directory}")
        print(f"Target directory: {target_directory}")
        print(f"Mapping file: {mapping_file_path}")
        print("-" * 50)
        flatten_directory(source_directory, target_directory, mapping_file_path)
