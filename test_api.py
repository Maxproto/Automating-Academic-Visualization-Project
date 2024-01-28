import base64
import requests
import re

def extract_python_code(text):
    """
    Extracts Python code blocks from the provided text.
    Code blocks are expected to be fenced by ```.

    Args:
    text (str): The text containing the code blocks.

    Returns:
    str: Concatenated Python code extracted from the text.
    """
    # Regular expression to find code blocks
    code_blocks = re.findall(r'```python(.*?)```', text, re.DOTALL)

    # Concatenate all the found code blocks separated by a newline
    concatenated_code = '\n'.join(code.strip() for code in code_blocks)
    return concatenated_code

def encode_image(image_path):
    """
    Encodes the image at the specified path to a base64 string.

    Args:
    image_path (str): Path to the image file.

    Returns:
    str: Base64 encoded string of the image.
    """
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# OpenAI API Key (Replace with your actual API key)
api_key = "YOUR_API_KEY"

# Path to your image
image_path = "neurips_figures/2307.04204/linear_depth2_width256_scale3.png"
caption = "$\\alpha=10$"
prompt = "This is a data visualization figure from an academic paper with the caption of " + caption + "\nPlease write Python code using matplotlib to draw the exact same plot as this one and save it as a png file with 300dpi."

# Encoding the image to base64
base64_image = encode_image(image_path)

# Setting up the headers for the API request
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

# Payload for the API request
payload = {
    "model": "gpt-4-vision-preview",
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": prompt
          },
          {
            "type": "image_url",
            "image_url": {
              "url": f"data:image/jpeg;base64,{base64_image}"
            }
          }
        ]
      }
    ],
    "max_tokens": 1024
}

# Making the API request and capturing the response
response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

# Parsing the response
dict_response = response.json()
print(dict_response)
