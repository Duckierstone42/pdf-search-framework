# General Structure

## API file

-I should have each api in its own file, with a specified return value and a main function that works.
-They should all be downloaded into pdfs or txt files for now, that doesn't have to be standardized for now
-Should return like a -1 if it fails to work
-For now just download into the working directory, I can deal with the details later on

## Download API

-I should have a general function that given a doi searches it up on crossref and then tries to download using API. If
any of the API's fail it should go straight to the last method of download via headless selenium browse.r
-Then have like a dictinary that maps it to all the API journals that exist, else the headless selenium browser.
-Make sure the dict uses the proper names used by the crossref API so that they match

-As a last resort this function should also be able to search for it and download via webscraping headless selenium browsers.

## Environment Variables

Define an EMAIL, WILEY_KEY, and ELSEVIER_KEY in a .env folder. The WILEY_KEY and ELSEVIER_KEY represent API keys from
those respective publishers.

Also, you may need to create a downloads folder before running any of the individual functions
