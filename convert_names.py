import os
import json
import argparse


def convert_uuid_to_original_names(uuid_list_file, mapping_file_path, output_file=None):
    """
    Converts a list of UUID filenames to their original names using the mapping file.

    Args:
        uuid_list_file (str): Path to file containing UUID filenames (one per line)
                             or None to read from stdin
        mapping_file_path (str): Path to the mapping JSON file
        output_file (str): Path to output file (optional, prints to stdout if not provided)
    """
    # Check if the mapping file exists
    if not os.path.exists(mapping_file_path):
        print(f"Error: Mapping file {mapping_file_path} does not exist.")
        return

    # Load the mapping file
    with open(mapping_file_path, "r") as f:
        file_mapping = json.load(f)

    # Read UUID filenames
    if uuid_list_file and os.path.exists(uuid_list_file):
        with open(uuid_list_file, "r") as f:
            uuid_filenames = [line.strip() for line in f if line.strip()]
    else:
        # Read from the error list you provided
        uuid_filenames = []

    # Process the conversion
    results = []
    not_found = []

    for uuid_filename in uuid_filenames:
        # Clean up the filename (remove bullet points, colons, etc.)
        clean_uuid = uuid_filename.strip().lstrip("-").strip().split(":")[0].strip()

        if clean_uuid in file_mapping:
            original_path = file_mapping[clean_uuid]
            results.append(f"{clean_uuid} -> {original_path}")
        else:
            not_found.append(clean_uuid)
            results.append(f"{clean_uuid} -> NOT FOUND IN MAPPING")

    # Output results
    if output_file:
        with open(output_file, "w") as f:
            for result in results:
                f.write(result + "\n")
        print(f"Conversion results written to {output_file}")
    else:
        for result in results:
            print(result)

    # Summary
    print(f"\n{'='*60}")
    print(f"Total files processed: {len(uuid_filenames)}")
    print(f"Found in mapping: {len(uuid_filenames) - len(not_found)}")
    print(f"Not found in mapping: {len(not_found)}")

    if not_found:
        print(f"\nFiles not found in mapping:")
        for nf in not_found:
            print(f"  - {nf}")


def convert_error_list(error_text, mapping_file_path, output_file=None):
    """
    Converts an error list (like the one you provided) to original filenames.

    Args:
        error_text (str): The error text containing UUID filenames
        mapping_file_path (str): Path to the mapping JSON file
        output_file (str): Path to output file (optional)
    """
    # Check if the mapping file exists
    if not os.path.exists(mapping_file_path):
        print(f"Error: Mapping file {mapping_file_path} does not exist.")
        return

    # Load the mapping file
    with open(mapping_file_path, "r") as f:
        file_mapping = json.load(f)

    # Parse the error text to extract UUID filenames
    import re

    # Pattern to match UUID filenames (with extensions)
    pattern = r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\.\w+"
    uuid_filenames = re.findall(pattern, error_text)

    # Process the conversion
    results = []
    error_details = {}

    lines = error_text.strip().split("\n")
    for line in lines:
        if line.strip().startswith("-"):
            # Extract UUID filename and error message
            parts = line.split(":", 1)
            if len(parts) == 2:
                uuid_part = parts[0].strip().lstrip("-").strip()
                error_msg = parts[1].strip()

                if uuid_part in file_mapping:
                    original_path = file_mapping[uuid_part]
                    results.append(f"- {original_path}: {error_msg}")
                    error_details[original_path] = error_msg
                else:
                    results.append(f"- {uuid_part} (NOT IN MAPPING): {error_msg}")

    # Output results
    if output_file:
        with open(output_file, "w") as f:
            for result in results:
                f.write(result + "\n")
        print(f"Converted error list written to {output_file}")
    else:
        print("\n" + "=" * 60)
        print("CONVERTED ERROR LIST:")
        print("=" * 60)
        for result in results:
            print(result)

    return error_details


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert UUID filenames to original names using mapping file."
    )

    parser.add_argument(
        "-m",
        "--mapping",
        help="Path to the mapping JSON file (default: ./VenueMarketableBatch2.json)",
        default="VenueMarketableBatch2.json",
    )

    parser.add_argument(
        "-i",
        "--input",
        help="Input file containing UUID filenames (one per line)",
        default=None,
    )

    parser.add_argument(
        "-o",
        "--output",
        help="Output file for converted names (prints to stdout if not provided)",
        default=None,
    )

    parser.add_argument(
        "-e",
        "--errors",
        help="Convert the error list format (paste your error text)",
        action="store_true",
    )

    args = parser.parse_args()

    mapping_file_path = os.path.abspath(args.mapping)

    if args.errors:
        # Handle the specific error format you provided
        error_text = """
- 827499a6-06fb-4e70-a0a3-e86b8c961f9d.tif: File "827499a6-06fb-4e70-a0a3-e86b8c961f9d.tif" has unsupported file type
- d8af4c1e-567f-4b49-ba36-d49b9853a140.xlsx: Can't detect encoding for file "d8af4c1e-567f-4b49-ba36-d49b9853a140.xlsx"
- 258a929c-c896-4710-9455-45c59c7fd0bb.xlsm: Cannot detect simple header in file "258a929c-c896-4710-9455-45c59c7fd0bb.xlsm"
- 38fbfa34-ff3c-4c16-9058-dfde858e20d7.aspx: 38fbfa34-ff3c-4c16-9058-dfde858e20d7.aspx failed to process
- 440fc715-d1fe-41e9-9f3f-f04faa1026c4.xlsm: Cannot detect simple header in file "440fc715-d1fe-41e9-9f3f-f04faa1026c4.xlsm"
- 6a551b26-b708-4112-826f-f6684313b5fa.kml: File "6a551b26-b708-4112-826f-f6684313b5fa.kml" has unsupported file type
- ce2f8ec2-1b1b-408d-9938-0b45c95e9893.kml: File "ce2f8ec2-1b1b-408d-9938-0b45c95e9893.kml" has unsupported file type
- 9459720e-8618-409f-8550-204f068474c7.xlsm: Cannot detect simple header in file "9459720e-8618-409f-8550-204f068474c7.xlsm"
        """
        convert_error_list(error_text, mapping_file_path, args.output)
    else:
        convert_uuid_to_original_names(args.input, mapping_file_path, args.output)
