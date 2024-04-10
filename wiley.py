import os
from dotenv import load_dotenv
import re
import requests
load_dotenv()

CROSSREFAPI = "https://api.crossref.org/works/"

def get_wiley(DOI,filename,scrape_url=None):
    #Should try to pass in download link from crossref api,
    print("Downloading from wiley...")
    if scrape_url == None:
        #Call crossref api to determine the download url.
        try:
            metadata = requests.get(CROSSREFAPI+DOI)
            if (metadata.status_code != 200):
                print(f"Crossref failed to find the DOI {DOI}")
                return -1
            metadata = metadata.json()
            if metadata["message"]["publisher"] != "Wiley":
                print("Incorrect publisher, only Wiley acceptable here.")
                return -1
            links = metadata["message"]["link"]
            for link in links:
                if link["intended-application"] == "text-mining":
                    scrape_url = link["URL"]

            if (scrape_url == None):
                print("No corresponding scraping url exists")
                return -1

        except Exception as e:
            print(f"Error Occured: {e}")
            return -1

        headers = {"Wiley-TDM-Client-Token":os.environ["WILEY_KEY"]}
        request = requests.get(scrape_url,headers=headers)
        if (request.status_code == 200):
            with open(f"downloads/{filename}.pdf","wb") as f:
                f.write(request.content)
        else:
            print("API failed to fetch")
            return -1

if __name__ == "__main__":
    doi = "10.1002%2Fcbic.201300351"

    result = get_wiley(doi)
    if (result == -1):
        print(f"Failed to download {doi}")
    else:
        print(f"Succesfully downloaded {doi}")