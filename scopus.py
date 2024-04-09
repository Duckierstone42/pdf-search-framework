import os
from dotenv import load_dotenv
import requests
load_dotenv()

SCOPUS_URL = "http://api.elsevier.com/content/search/scopus"

#Can later be expanded to return more than just DOI's, but other assosciated metadata. For now it just returns a list of DOIs.
#Also for now just ands together keywords. In the future should brainstorm otherways of searching.
def get_scopus_urls(keywords):
    keyword_string = "KEY(" + " AND ".join(keywords) + ")" 

    params = {"query": keyword_string}

    headers = {"X-ELS-APIKey":os.environ["ELSEVIER_KEY"]
    }
    try:

        request = requests.get(SCOPUS_URL,headers=headers, params=params)
        if request.status_code != 200:
            print(f"Something went wrong with the API")
            return -1
        request= request.json()
        return list(map(lambda entry: entry["prism:doi"],request["search-results"]["entry"]))
    except Exception as e:
        print(f"Failed to get DOI's due to the following error: {e}")
        return -1


if __name__ == "__main__":
    keywords = ["heart","brain"]
    results = get_scopus_urls(keywords)
    if results == -1:
        print(f"Failed to get DOI's from {keywords}")
    else:
        print(f"Succesfully retrieved DOI's. Here are a couple: {results[:10]}")
