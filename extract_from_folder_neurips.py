import os
import re
import shutil
import json
from wand.image import Image
from tqdm import tqdm

def extract_figures_and_captions(src_folder, dest_folder):
    """
    Extracts figures and their captions from LaTeX source files in the specified folder.

    Args:
    src_folder (str): The folder containing LaTeX source files.
    dest_folder (str): The destination folder where extracted figures will be saved.
    """
    # Regex pattern to identify figures and captions in LaTeX files
    figure_pattern = re.compile(
        r'\\begin{figure}.*?\\includegraphics.*?{(.*?)}.*?\\caption{([^}]*)}.*?\\end{figure}',
        re.DOTALL)

    for root, _, files in os.walk(src_folder):
        for file in files:
            if file.endswith('.tex'):
                with open(os.path.join(root, file), 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                    # Remove comments from the content
                    cleaned_content = '\n'.join([line.split('%')[0] for line in content.split('\n')])

                    for match in figure_pattern.findall(cleaned_content):
                        figure_path, caption = match
                        # Clean the caption text
                        caption = ' '.join(caption.split()).strip()

                        # Skip if caption contains unbalanced braces
                        if "{" in caption or "}" in caption:
                            continue

                        # Construct full path to the figure
                        figure_full_path = os.path.join(root, figure_path).replace('\\', '/')
                        if os.path.exists(figure_full_path) and figure_full_path.endswith(('.png', '.jpg', '.jpeg')):
                            # Create destination folder if needed
                            os.makedirs(dest_folder, exist_ok=True)
                            shutil.copy(figure_full_path, dest_folder)

                            # Append figure information to the list
                            extracted_info.append({
                                "figure_path": os.path.join(dest_folder, os.path.basename(figure_path)).replace('\\', '/'),
                                "caption": caption,
                                "source": os.path.join(root, file).replace('\\', '/'),
                                "arxiv_id": src_folder.replace('\\', '/')
                            })

# Output JSON file and folders
top_folder = "neurips"
output_json = 'neurips_figures_and_captions.json'
output_figure_path = "neurips_figures"

# Load existing data if available
if os.path.exists(output_json):
    with open(output_json, 'r') as f:
        extracted_info = json.load(f)
else:
    extracted_info = []

# Process each arXiv folder
for arxiv_id in tqdm(os.listdir(top_folder)):
    src_folder_path = os.path.join(top_folder, arxiv_id)
    dest_folder_path = os.path.join(output_figure_path, arxiv_id)
    
    # Process only if it's a directory
    if os.path.isdir(src_folder_path):
        print(f"Processing {arxiv_id}")
        extract_figures_and_captions(src_folder_path, dest_folder_path)

# Write the extracted information to a JSON file
with open(output_json, 'w') as json_file:
    json.dump(extracted_info, json_file, indent=4)
