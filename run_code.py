import json
import os
import matplotlib.pyplot as plt
import re
from copy import deepcopy

def ensure_dir(directory):
    """
    Ensures that the specified directory exists. If not, it creates the directory.

    Args:
    directory (str): The path of the directory to check or create.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)

def prepare_code(code, new_path):
    """
    Prepares the Python code for execution by modifying the save path of figures and removing plt.show().

    Args:
    code (str): The original Python code to be modified.
    new_path (str): The new path where the figures should be saved.

    Returns:
    str: The modified Python code.
    """
    # Escape forward slashes for the new path
    escaped_path = new_path.replace('\\', '/')
    # Replace plt.savefig() with the new path, regardless of the original parameters
    code = re.sub(r"plt\.savefig\([^)]+\)", f"plt.savefig('{escaped_path}')", code)
    # Remove plt.show()
    code = re.sub(r"plt\.show\(\)", '', code)
    return code

def generate_figure_path(base_path, arxiv_id, suffix):
    """
    Generates a new path for saving figures with a given suffix.

    Args:
    base_path (str): The original base path of the figure.
    arxiv_id (str): The ArXiv ID associated with the figure.
    suffix (str): The suffix to append to the figure filename.

    Returns:
    str: The new path for the figure.
    """
    # Extract the base filename and directory from the original path
    base_filename = os.path.basename(base_path)
    new_dir_path = f"llava/{arxiv_id}"
    
    # Ensure the new directory exists
    ensure_dir(new_dir_path)

    # Construct the full path for the new figure with the suffix
    new_figure_path = os.path.join(new_dir_path, f"{os.path.splitext(base_filename)[0]}_{suffix}.png")
    return new_figure_path

# Load JSON data from the file
with open('merged_llava_direct.json', 'r') as file:
    json_data = json.load(file)

# List to store processed output
list_output_direct = []

# Process each item in the JSON data
for item in json_data:
    dict_direct = deepcopy(item)

    # Generate the new figure path
    direct_fig_path = generate_figure_path(item['figure_path'], item['arxiv_id'], 'direct').replace('\\', '/')

    # Prepare the code with the correct save path and without plt.show()
    direct_code = prepare_code(item["llava_code"], direct_fig_path)

    # Execute the modified code and handle exceptions
    try:
        exec(direct_code, globals()) 
        dict_direct["runnable"] = True
    except Exception as e:
        print(f"An error occurred while executing direct_code for {item['arxiv_id']}: {e}")
        dict_direct["runnable"] = False

    # Add the new keys to the dictionary and append to the list
    dict_direct['output_figure_path'] = direct_fig_path
    list_output_direct.append(dict_direct)

# Write the output to a new JSON file
with open('llava_output_direct.json', 'w') as file:
    json.dump(list_output_direct, file, indent=4)

print(len(list_output_direct))
print("Processing complete, updated JSON saved.")
