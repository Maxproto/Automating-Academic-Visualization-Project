import requests
from bs4 import BeautifulSoup
import os
import zipfile
import io
import tarfile

def download_arxiv_source(arxiv_id, output_folder):
    """
    Downloads the source code of a paper from arXiv given its ID.

    Args:
    arxiv_id (str): The arXiv ID of the paper.
    output_folder (str): The folder where the source code will be saved.
    """
    # Construct the URL for the arXiv source
    url = f"https://arxiv.org/e-print/{arxiv_id}"

    # Download the source tarball or zip file
    response = requests.get(url)
    response.raise_for_status()  # Ensure the request was successful

    # Check the content type to determine if it's a tarball or a zip file
    if response.headers['content-type'] == 'application/x-eprint-tar':
        # Handle extraction for tarball
        with tarfile.open(fileobj=io.BytesIO(response.content), mode='r:gz') as tar:
            tar.extractall(output_folder)
    elif response.headers['content-type'] == 'application/x-eprint':
        # Handle extraction for zip file
        with zipfile.ZipFile(io.BytesIO(response.content)) as z:
            z.extractall(output_folder)

# Define the URL to fetch papers from NeurIPS 2023
url = 'https://arxiv.org/search/?searchtype=all&query=NeurIPS+2023&abstracts=show&size=200&order=-announced_date_first&start=600'

# Fetch the content of the website
response = requests.get(url)
response.raise_for_status()  # Raise an exception for HTTP errors

# Parse the content using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Find all links in the page
arxiv_links = soup.find_all('a', href=True)

# Extract the arXiv IDs from the links
arxiv_ids = [
    link['href'].split('/')[-1] for link in arxiv_links
    if 'arxiv.org/abs/' in link['href']
]

print(f"Found {len(arxiv_ids)} arXiv IDs.")

# Define the output folder for downloaded sources
output_folder = "neurips"

# Download the source for each arXiv ID
for arxiv_id in arxiv_ids:
    download_path = os.path.join(output_folder, arxiv_id)
    
    # Skip certain IDs or if the folder already exists
    if os.path.exists(download_path):
        print(f"Skipping {arxiv_id} (already exists or excluded).")
        continue
    
    # Download the source and save in the specified folder
    print(f"Downloading source for {arxiv_id}")
    download_arxiv_source(arxiv_id, download_path)
