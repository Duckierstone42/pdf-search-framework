from wiley import get_wiley 
from crossref import get_metadata 
from pub_med import get_pub_med
from science_direct import get_science_direct
from web_scraper import get_pdf_scraping, create_driver
import os
import re
#This file downloads the doi's by calling all the functions defined in the other seperate files

directory = {"Elsevier BV": get_science_direct,"Wiley":get_wiley}
#Pub Med contains articles from various publishers, so I will just try it directly then web_scrape.
def download_doi(DOI,filename=None):
    driver = None
    if filename == None:
        filename = re.sub(r'[^a-zA-Z0-9]', '', DOI) #Just makes the DOI the name without the special characters
    metadata = get_metadata(DOI)
    if (metadata == -1):
        return -1
    print(metadata["publisher"])
    if metadata["publisher"] in directory:
        result = directory[metadata["publisher"]](DOI,filename)
        if (result == -1):
            return -1
    else:
        #Try pub_med API. 
        result = get_pub_med(DOI,filename)
        if (result == -1):
            #I should also try to integrate general web-scraping API (as a last measure), but thats for later.
            download_directory = os.path.join(os.getcwd(),"downloads")
    #Create temp directory here?.
            if not driver:
                driver = create_driver(download_directory) 
            result = get_pdf_scraping(DOI,driver,download_directory)
            return result
        #Integrate web-scraping component here. For now, give it its own temp directory.
    return 0
if __name__ == "__main__":
    doi = "10.1016/0925-8388(92)90625-J" 
    result = download_doi(doi)
    if (result == -1):
        print(f"Failed to download {doi}")
    else:
        print(f"Succesfully downloaded {doi}")