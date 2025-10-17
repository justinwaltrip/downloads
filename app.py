import os
import streamlit as st
import PyPDF2
import pdf2image
from PIL import Image
import io
import shutil
from pathlib import Path
import base64


def get_pdf_preview(pdf_path, page_num=0, width=300):
    """Generate a preview image of a specific page from a PDF file."""
    try:
        images = pdf2image.convert_from_path(
            pdf_path, first_page=page_num + 1, last_page=page_num + 1
        )
        if images:
            img = images[0]
            # Resize while maintaining aspect ratio
            aspect_ratio = img.width / img.height
            height = int(width / aspect_ratio)
            return img.resize((width, height), Image.LANCZOS)
        return None
    except Exception as e:
        st.error(f"Error generating preview for {pdf_path}: {e}")
        return None


def get_pdf_info(pdf_path):
    """Get basic info about a PDF file."""
    try:
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            return {
                "pages": len(reader.pages),
                "size": os.path.getsize(pdf_path) // 1024,  # Size in KB
            }
    except Exception as e:
        st.error(f"Error reading {pdf_path}: {e}")
        return {"pages": "Error", "size": "Error"}


def find_pdf_files(directory):
    """Find all PDF files in a directory (non-recursive)."""
    pdf_files = []
    for item in os.listdir(directory):
        full_path = os.path.join(directory, item)
        if os.path.isfile(full_path) and full_path.lower().endswith(".pdf"):
            pdf_files.append(full_path)
    return pdf_files


def find_pdf_files_recursive(directory):
    """Find all PDF files in a directory (recursive)."""
    pdf_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(".pdf"):
                pdf_files.append(os.path.join(root, file))
    return pdf_files


# Set page config
st.set_page_config(page_title="PDF Matcher", layout="wide")

# App title and description
st.title("PDF Visual Matcher")
st.markdown(
    """
This tool helps you manually match PDFs from a flattened directory to their original structure by visually comparing them.
"""
)

# Sidebar for directory selection
with st.sidebar:
    st.header("Directory Settings")
    flattened_dir = st.text_input("Flattened Directory Path", "")
    original_dir = st.text_input("Original Directory Path", "")
    output_dir = st.text_input("Output Directory Path (for saving matches)", "")

    st.header("Display Settings")
    recursive_search = st.checkbox("Search original directory recursively", value=True)
    preview_width = st.slider(
        "Preview Width", min_value=200, max_value=600, value=300, step=50
    )

    if st.button("Load Files"):
        if not flattened_dir or not original_dir:
            st.error("Please provide both directory paths")
        elif not os.path.isdir(flattened_dir) or not os.path.isdir(original_dir):
            st.error("One or both directories do not exist")
        else:
            st.session_state.flattened_files = find_pdf_files(flattened_dir)
            if recursive_search:
                st.session_state.original_files = find_pdf_files_recursive(original_dir)
            else:
                st.session_state.original_files = find_pdf_files(original_dir)

            st.session_state.current_flat_index = 0
            st.session_state.matches = {}
            st.success(
                f"Loaded {len(st.session_state.flattened_files)} flattened files and {len(st.session_state.original_files)} original files"
            )

    if st.button("Save Matches"):
        if "matches" not in st.session_state or not output_dir:
            st.error("No matches to save or output directory not specified")
        else:
            os.makedirs(output_dir, exist_ok=True)
            copied = 0
            for flat_path, orig_path in st.session_state.matches.items():
                rel_path = os.path.relpath(orig_path, original_dir)
                target_path = os.path.join(output_dir, rel_path)

                # Create directory structure
                os.makedirs(os.path.dirname(target_path), exist_ok=True)

                # Copy the file
                try:
                    shutil.copy2(flat_path, target_path)
                    copied += 1
                except Exception as e:
                    st.error(f"Error copying {flat_path} to {target_path}: {e}")

            st.success(f"Copied {copied} files to {output_dir}")

# Main content area
if "flattened_files" in st.session_state and "original_files" in st.session_state:
    if len(st.session_state.flattened_files) == 0:
        st.warning("No PDF files found in the flattened directory")
    elif len(st.session_state.original_files) == 0:
        st.warning("No PDF files found in the original directory")
    else:
        # Display progress
        flat_files_count = len(st.session_state.flattened_files)
        current_index = st.session_state.current_flat_index
        matches_count = len(st.session_state.matches)

        st.progress(current_index / flat_files_count)
        st.write(
            f"Progress: {current_index}/{flat_files_count} files processed, {matches_count} matches found"
        )

        # Display current flattened file
        current_flat_file = st.session_state.flattened_files[current_index]
        flat_file_info = get_pdf_info(current_flat_file)

        col1, col2 = st.columns([1, 3])

        with col1:
            st.subheader("Current File to Match")
            st.write(f"File: {os.path.basename(current_flat_file)}")
            st.write(
                f"Pages: {flat_file_info['pages']}, Size: {flat_file_info['size']} KB"
            )

            flat_preview = get_pdf_preview(
                current_flat_file, page_num=0, width=preview_width
            )
            if flat_preview:
                st.image(flat_preview, caption="First page")

                # If multiple pages, show last page too
                if flat_file_info["pages"] > 1:
                    flat_last_preview = get_pdf_preview(
                        current_flat_file,
                        page_num=flat_file_info["pages"] - 1,
                        width=preview_width,
                    )
                    if flat_last_preview:
                        st.image(flat_last_preview, caption="Last page")

            # Navigation buttons
            col1a, col1b = st.columns(2)
            with col1a:
                if st.button("Previous File"):
                    if current_index > 0:
                        st.session_state.current_flat_index -= 1
                        st.experimental_rerun()

            with col1b:
                if st.button("Next File"):
                    if current_index < len(st.session_state.flattened_files) - 1:
                        st.session_state.current_flat_index += 1
                        st.experimental_rerun()

            if st.button("Skip this file"):
                if current_index < len(st.session_state.flattened_files) - 1:
                    st.session_state.current_flat_index += 1
                    st.experimental_rerun()

        with col2:
            st.subheader("Potential Matches")

            # Filter original files by page count for faster matching
            similar_files = []
            for orig_file in st.session_state.original_files:
                orig_info = get_pdf_info(orig_file)
                if orig_info["pages"] == flat_file_info["pages"]:
                    similar_files.append((orig_file, orig_info))

            st.write(
                f"Found {len(similar_files)} files with the same page count ({flat_file_info['pages']} pages)"
            )

            # Display potential matches in a grid
            if similar_files:
                cols = st.columns(3)
                for i, (orig_file, orig_info) in enumerate(
                    similar_files[:9]
                ):  # Show up to 9 matches
                    col_index = i % 3
                    with cols[col_index]:
                        st.write(f"**{os.path.basename(orig_file)}**")
                        st.write(
                            f"Pages: {orig_info['pages']}, Size: {orig_info['size']} KB"
                        )

                        orig_preview = get_pdf_preview(
                            orig_file, page_num=0, width=preview_width
                        )
                        if orig_preview:
                            st.image(orig_preview, caption="First page")

                            if st.button(f"Select Match #{i+1}", key=f"match_{i}"):
                                st.session_state.matches[current_flat_file] = orig_file
                                if (
                                    current_index
                                    < len(st.session_state.flattened_files) - 1
                                ):
                                    st.session_state.current_flat_index += 1
                                    st.experimental_rerun()
                                else:
                                    st.success("All files processed!")

                if len(similar_files) > 9:
                    st.write(
                        f"... and {len(similar_files) - 9} more potential matches not shown"
                    )

                    # Add search box for filtering by filename
                    st.subheader("Filter by filename")
                    filename_filter = st.text_input(
                        "Enter part of filename to filter matches"
                    )

                    if filename_filter:
                        filtered_files = [
                            (orig_file, orig_info)
                            for orig_file, orig_info in similar_files
                            if filename_filter.lower()
                            in os.path.basename(orig_file).lower()
                        ]

                        st.write(
                            f"Found {len(filtered_files)} files matching '{filename_filter}'"
                        )

                        for i, (orig_file, orig_info) in enumerate(filtered_files[:5]):
                            st.write(f"**{os.path.basename(orig_file)}**")
                            st.write(
                                f"Pages: {orig_info['pages']}, Size: {orig_info['size']} KB"
                            )

                            orig_preview = get_pdf_preview(
                                orig_file, page_num=0, width=preview_width
                            )
                            if orig_preview:
                                st.image(orig_preview, caption="First page")

                                if st.button(
                                    f"Select Filtered Match #{i+1}", key=f"filtered_{i}"
                                ):
                                    st.session_state.matches[current_flat_file] = (
                                        orig_file
                                    )
                                    if (
                                        current_index
                                        < len(st.session_state.flattened_files) - 1
                                    ):
                                        st.session_state.current_flat_index += 1
                                        st.experimental_rerun()
                                    else:
                                        st.success("All files processed!")
            else:
                st.warning("No files with matching page count found.")

                # Option to search by name
                st.subheader("Search by filename")
                search_term = st.text_input("Enter part of filename to search")

                if search_term:
                    search_results = [
                        orig_file
                        for orig_file in st.session_state.original_files
                        if search_term.lower() in os.path.basename(orig_file).lower()
                    ]

                    if search_results:
                        st.write(f"Found {len(search_results)} matching files")
                        for i, orig_file in enumerate(search_results[:5]):
                            orig_info = get_pdf_info(orig_file)
                            st.write(f"**{os.path.basename(orig_file)}**")
                            st.write(
                                f"Pages: {orig_info['pages']}, Size: {orig_info['size']} KB"
                            )

                            orig_preview = get_pdf_preview(
                                orig_file, page_num=0, width=preview_width
                            )
                            if orig_preview:
                                st.image(orig_preview, caption="First page")

                                if st.button(f"Select this match", key=f"search_{i}"):
                                    st.session_state.matches[current_flat_file] = (
                                        orig_file
                                    )
                                    if (
                                        current_index
                                        < len(st.session_state.flattened_files) - 1
                                    ):
                                        st.session_state.current_flat_index += 1
                                        st.experimental_rerun()
                                    else:
                                        st.success("All files processed!")
else:
    st.info("Please select directories and click 'Load Files' to start matching")

# Display current matches
if "matches" in st.session_state and st.session_state.matches:
    with st.expander("Current Matches"):
        for flat_path, orig_path in st.session_state.matches.items():
            st.write(
                f"- {os.path.basename(flat_path)} → {os.path.relpath(orig_path, original_dir)}"
            )
