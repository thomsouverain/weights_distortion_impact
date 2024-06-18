import markdown2
import imgkit
import os
import sys


def remove_special_characters(filename):
    """ Remove specific characters from a filename. """
    filename = filename.replace("['", "").replace("']", "")
    filename = filename.replace("', '", "_")
    return filename

def remove_line_from_file(file_path, line_to_remove):
    """ Remove a specific line from a file. """
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    with open(file_path, 'w', encoding='utf-8') as f:
        for line in lines:
            if line.strip() != line_to_remove:
                f.write(line)

def replace_text_in_file(file_path, old_text, new_text):
    """ Replace old_text with new_text in a file. """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    content = content.replace(old_text, new_text)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def convert_md_to_png(md_file):
    # Remove special characters from the file name
    md_file_clean = remove_special_characters(md_file)

    # Remove the line '# Sheet1' from the Markdown file
    line_to_remove = '# Sheet1'  # Adjust as needed
    remove_line_from_file(md_file, line_to_remove)

    # Replace unnecessary Markdown text
    replace_text_in_file(md_file, '_rate', ' rate')
    replace_text_in_file(md_file, "Unnamed: 0", "Model")

    # Read the Markdown content
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # Convert Markdown to HTML with tables extension
    html_content = markdown2.markdown(md_content, extras=['tables'])

    # Generate a temporary HTML file path
    html_file = '/tmp/markdown_temp.html'

    # Write the HTML content to a temporary file
    with open(html_file, 'w', encoding='utf-8') as f:
        # Add custom CSS for table styling
        f.write('''
            <style>
            table {
                width: 100%;
                border-collapse: collapse;
            }
            th, td {
                border: 1px solid black;
                padding: 8px;
                text-align: center;
            }
            th {
                background-color: #f2f2f2;  /* Light gray background for headers */
                font-weight: bold;
            }
            </style>
        ''')
        f.write(html_content)

    # Generate the output PNG file path
    #png_file = os.path.splitext(md_file)[0] + '.png'
    png_file = os.path.splitext(md_file_clean)[0] + '.png'

    # Convert HTML to PNG using imgkit and wkhtmltoimage
    options = {
        'format': 'png',
        'quiet': '',
        'encoding': 'UTF-8',
    }
    imgkit.from_file(html_file, png_file, options=options)

    print(f'Converted {md_file} to {png_file}')

    # Cleanup: Remove temporary HTML file
    os.remove(html_file)

if __name__ == "__main__":
    # Take the file path from the command line argument
    md_file = sys.argv[1]
    convert_md_to_png(md_file)
