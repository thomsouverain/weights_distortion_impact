import pandas as pd
import sys
import os

def convert_xlsx_to_md(xlsx_file):
    # Load the Excel file
    xl = pd.ExcelFile(xlsx_file)

    # Iterate over each sheet and convert to Markdown
    md_content = ""
    for sheet_name in xl.sheet_names:
        df = xl.parse(sheet_name)
        md_content += f"# {sheet_name}\n\n"
        md_content += df.to_markdown(index=False) + "\n\n"

    # Generate the output Markdown file path
    md_file = os.path.splitext(xlsx_file)[0] + '.md'

    # Write the Markdown content to file
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(md_content)

    print(f'Converted {xlsx_file} to {md_file}')

if __name__ == "__main__":
    # Take the file path from the command line argument
    xlsx_file = sys.argv[1]
    convert_xlsx_to_md(xlsx_file)
