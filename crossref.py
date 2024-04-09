import os
from dotenv import load_dotenv
import requests
load_dotenv()

CROSSREFAPI = "https://api.crossref.org/works/"

#Should simply call the API and return the corresponding metadata as a JSON for easy use
#Potentially restruct API to recursively look into the other articles each relevant article cites, as they may be relevant.
def get_metadata(DOI):
    try:
        metadata = requests.get(CROSSREFAPI + DOI)
        if (metadata.status_code != 200):
                print(f"Crossref failed to find the DOI {DOI}")
                return -1
        metadata = metadata.json()
        return_dict= {}
        return_dict["publisher"] = metadata["message"]["publisher"]
        return_dict["abstract"] = metadata["message"]["abstract"]
        return_dict["authors"] = [author["given"] for author in metadata["message"]["author"]]
        return_dict["citation_count"] = metadata["message"]["reference-count"]
        return return_dict
    except Exception as e:
        print(f"Error occured: {e}")
        return -1

if __name__ == "__main__":
     doi = "10.1186/s12967-024-05098-7"
     metadata = get_metadata(doi)
     if (metadata == -1):
          print(f"Failed to retrieve metadata for {doi}")
     else:
          print(f"Succesfully retrieved metadata: {metadata}")