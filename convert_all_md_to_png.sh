#!/bin/bash

# Path to the repository containing .md files
repo_path="$1"

# Find all .md files and convert them to .png
find "$repo_path" -type f -name "*.md" | while read md_file; do
    python convert_md_to_png.py "$md_file"
done

