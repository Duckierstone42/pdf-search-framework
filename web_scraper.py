import re
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
import time
import os

DOI_URL = "http://doi.org/"
#Last case, if no API's work, simply use a headless chrome_browser. 
#Headless chromebrowsers take time and must be recycled, so one must be passed in, and returned by this function.
def get_pdf_scraping(DOI,driver,filename=None):
    if filename == None:
        filename = re.sub(r'[^a-zA-Z0-9]', '', DOI) #Just makes the DOI the name without the special characters
    doi_url = DOI_URL + DOI
    #First need to get the URLL via DOI redirct.    
    #I need a driver to both find the URL link 
    pdf_link = get_pdf_link(doi_url)
    if (pdf_link == -1):
        return -1
    #Need to install into a temp directory for web_scraping, due to the manner it is run in can't be sure if it actually
    #got downloaded or not.
    driver.get(pdf_link)
    #Define a unique temp directory


def create_driver(download_directory):
    options = webdriver.ChromeOptions()
    #Folder download_location determined here.    
    profile = {"plugins.plugins_list": [{"enabled": False,
                                         "name": "Chrome PDF Viewer"}],
               "download.default_directory": download_directory,
               "download.extensions_to_open": "",
               "plugins.always_open_pdf_externally": True}
    
    options.add_experimental_option("prefs", profile)
    options.add_argument("--headless")
    options.add_argument('--log-level=3')
    driver = webdriver.Chrome(options=options)
    return driver

#This function/last-case is very slow, luckily we should only be calling this as a last resort.
def get_pdf_link(doi,driver):

    URL = "http://doi.org/" + doi
    driver.get(URL)
    # Find all links on the page
    tries = 3
    for _ in range(tries):
        try:
            # Find all links on the page
            links = driver.find_elements(By.TAG_NAME, 'a')
            break
        except StaleElementReferenceException:
            pass
    else:
        print("Failed to retrieve links after {} tries".format(tries))
        return -1

    # Filter out links that point to PDF files
    pdf_links = []
    for link in links:
        try:
            href = link.get_attribute('href')
            if href and "pdf" in href:
                pdf_links.append(href)
        except StaleElementReferenceException:
            pass

    # Print the PDF links
    if len(pdf_links) == 0:
        return -1
    else:
        return pdf_links[0]


if __name__ == "__main__":
    download_directory = os.path.join(os.getcwd(),"downloads")
    driver = create_driver(download_directory) #Where it automatically downloads pdf.
    doi = "10.1186/s12871-024-02492-y"
    result = get_pdf_link(doi,driver)
    if (result == -1):
        print(f"Failed to download {doi}")
    else:
        print(f"Succesfully downloaded {doi}")
        print(result)

