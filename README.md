# HeyJobs Python Assessment Task

## Overview

The aim of this task is to extract information from job adverts on the heyjobs website (https://www.heyjobs.co/en/jobs-in-berlin) and to store the information in a postgres DB.

## Assumptions

Scraping data from a website, not under your control, is inherently hard to make robust. Any solution should have clear assumptions about the structure of the page and should fail quickly and obviously if these assumptions no longer hold. In this case I am making the following assumptions;

1. There exists an element on the page with `id=job-search-container` which contains all the adverts.
2. This element consists of a collection of `<a>` tags each of which contain the information required (some of which are not adverts but navigation controls).
3. Each `<a>` tag that is an advert will have two peices of data the `uid` and the `title`.
4. The `uid` will be contained in the `href` of the `<a>` tag.
5. The `title` is the text of an element with `class=job-card-title`

The main logic that deals with the extraction of this data and failing when these assumptions no longer hold can be found in `scraper/scraper/scraper:scrape` and `scraper/scraper/scraper:get_data`. If the stuructre of the page fails to meet the assumptions above a custom exception (`HTMLStructureChanged`) will be raised causing the main entrypoint to fail.

## Packaging

The code for scraping and storing the data is all packaged as a python module that is installed in the container, along with it's dependencies, using pipenv. I generally think this is good practice but perhaps a little over the top for this situation...

## Database

I have made use of sqlalchmy to construct a DB model for storing the extracted data (`scraper/scraper/db:Advert`). The main entrypoint creates the necessry table in the DB when it begins - if the table already exists then it will not be recreated. I have enforced a compound unique constraint on `uid` and `title` columns so that the scraping process can be rerun and only new adverts will be added to the DB. I am making use of an auto-increminting id as the tables primary key.

## Testing

### Unit

### Integration
