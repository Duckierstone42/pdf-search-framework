import os
from dotenv import load_dotenv
import requests
import re
load_dotenv()
SCIENCE_DIRECT_URL = "https://api.elsevier.com/content/article/doi/"

def get_science_direct(DOI,filename):
    print("Downloading from science direct...")
    #We can't use   the DOI as a filename, since it contains illegal characters.
    specific_url = SCIENCE_DIRECT_URL + DOI
    headers = {
        "Accept": "application/pdf",
        "X-ELS-APIKey": os.environ["ELSEVIER_KEY"]
    }
    response = requests.get(specific_url, headers=headers)
    if response.status_code == 200:
        with open(f"downloads/{filename}.pdf","wb") as f:
            f.write(response.content)

    else:
        return -1


if __name__ == "__main__":
    doi = "10.1016/0925-8388(92)90625-J"
    result = get_science_direct(doi)
    if (result == -1):
        print(f"Failed to download {doi}")
    else:
        print(f"Succesfully downloaded {doi}")