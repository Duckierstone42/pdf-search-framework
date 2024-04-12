from scopus import get_scopus_dois
from web_of_science import get_wos_dois
from download_doi import download_doi
import random
def get_pdfs_from_keywords(keywords):
    pass
    
    dois = set(get_scopus_dois(keywords))
    #dois = dois.union(set(get_wos_dois(keywords))) #Ensure potentially overlapping DOI's are removed
    dois = list(dois)
    #Randomize dois to ensure that we don't download from one publisher for a period of time.
    random.shuffle(dois)
    #For now just doing iteratively, can probably speed it up in the future by using multithreading
    total_downloaded = len(dois)
    for doi in dois:
        total_downloaded += download_doi(doi)
    print(f"Succesfully downloaded {total_downloaded} out of {len(dois)} using only 3 apis")






if __name__ == "__main__":
    keywords = ["machine,nlp"]
    result = get_pdfs_from_keywords(keywords)
    #Result is the percentage of papers it was able to download