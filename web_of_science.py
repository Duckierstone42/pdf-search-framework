import os
from dotenv import load_dotenv
import requests
load_dotenv()
#WARNING: This API is being replaced, make sure to replace with WOS-lite if you get that API key
WOS_LITE_URL = "https://wos-api.clarivate.com/api/woslite"

def get_wos_dois(keywords):
    #Note it appears that the keywords are anded together, so perhaps seperate API calls should occur if I wish to OR them
    headers = {"X-ApiKey": os.environ["CLARIVATE_KEY"]}
    query = "TS=(" + ",".join(keywords)+")"
    params = {"databaseId": "WOK", "count": "100","firstRecord":"1","usrQuery":query}

    results = requests.get(WOS_LITE_URL,headers=headers,params=params)
    if (results.status_code != 200):
        print("Something went wrong with the WOS API request")
        return -1
    #Quite a few entries don't have a DOI assosciated with them, so I will just skip those for now.
    results =results.json()
    data = results["Data"]
    DOIs = []
    for datum in data:
        if "Other" in datum and "Identifier.Doi" in datum["Other"]:
            DOIs.append(datum["Other"]["Identifier.Doi"][0])
    return DOIs


if __name__ == "__main__":
    keywords = ["superconductor","temperature"]
    results = get_wos_dois(keywords)
    if (results == -1):
        print(f"Failed to get DOI's for {keywords}")
    else:
        print(f"Succesfully retrieved {len(results)} DOI's, here are a couple of them: {results[:5]}")