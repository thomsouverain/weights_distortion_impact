#!/bin/bash

# Path to the repository containing .xlsx files
repo_path="$1"

# Find all .xlsx files and convert them to .pdf
find "$repo_path" -type f -name "*.xlsx" | while read xlsx_file; do
    python convert_xlsx_to_md.py "$xlsx_file"
done
