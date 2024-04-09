import os
from dotenv import load_dotenv
import re
load_dotenv()
import requests
email  = os.environ["EMAIL"]
DOI_TO_PMID_URL = f"https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?tool=LLM_DATA_MINING&email={email}&format=json&versions=no&idtype=doi"
PMID_TO_FULL_TEXT_URL = "https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/pmcoa.cgi/BioC_json"


def get_pub_med(DOI, filename= None):
    if filename == None:
        filename = re.sub(r'[^a-zA-Z0-9]', '', DOI) #Just makes the DOI the name without the special characters
    #Call two URLS, one to get PMID then one to download given pmid.
    try:
        records = requests.get(DOI_TO_PMID_URL + f"&ids={doi}")
        if records.status_code != 200:
            print(f"Failed to find DOI {DOI}")
            return -1
        records = records.json()
        pmid = records["records"][0]["pmid"]
        result = requests.get(PMID_TO_FULL_TEXT_URL + f"/{pmid}/unicode")
        result = result.json()
        passages = result[0]["documents"][0]["passages"]
        text = list(map(lambda passage: passage["text"],passages))
        full_text = " ".join(text)
        with open(f"downloads/{filename}.txt","w",encoding="utf-8") as f:
            f.write(full_text)
        return 1
    except Exception as e:
        print(f"Exception raised: {e}")
        return -1


if __name__ == "__main__":
    doi = "10.1371/journal.pone.0000217"
    result = get_pub_med(doi)
    if (result == -1):
        print(f"Failed to download {doi}")
    else:
        print(f"Succesfully downloaded {doi}")
