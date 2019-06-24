# HeyJobs Python Assessment Task

[![CircleCI](https://circleci.com/gh/josh-gree/python-task/tree/master.svg?style=svg)](https://circleci.com/gh/josh-gree/python-task/tree/master)

## Overview

The aim of this task is to extract information from job adverts on the heyjobs website (https://www.heyjobs.co/en/jobs-in-berlin) and to store the information in a postgres DB.

### Local setup

I make use of pipenv and pyenv for managing isolated python enviroments. To use this code locally it will be neccesery to have `python=3.6.8` and to have pipenv installed (`pip install pipenv`). To create the python env you can then run;

```bash
pipenv install --dev # this installs dev and prod dependencies
```

## Assumptions

Scraping data from a website, not under your control, is inherently hard to make robust. Any solution should have clear assumptions about the structure of the page and should fail quickly and obviously if these assumptions no longer hold. In this case I am making the following assumptions;

1. There exists an element on the page with `id=job-search-container` which contains all the adverts.
2. This element consists of a collection of `<a>` tags each of which contain the information required (some of which are not adverts but navigation controls).
3. The `uid` will be contained in the `href` of the `<a>` tag.
4. The `title` is the text of an element with `class=job-card-title`
5. If either `uid` or `title` are missing then do not treat `<a>` tag as an advert. This could probably be a looser assumption such that we allow for adverts to have one but not both missing.

The main logic that deals with the extraction of this data and failing when these assumptions no longer hold can be found in `scraper/scraper/scraper:scrape` and `scraper/scraper/scraper:get_data`. If the stuructre of the page fails to meet the assumptions above a custom exception (`HTMLStructureChanged`) will be raised causing the main entrypoint to fail.

## Packaging

The code for scraping and storing the data is all packaged as a python module that is installed in the container, along with it's dependencies, using pipenv. I generally think this is good practice but perhaps a little over the top for this situation...

## Database

I have made use of sqlalchmy to construct a DB model for storing the extracted data (`scraper/scraper/db:Advert`). The main entrypoint creates the necessry table in the DB when it begins - if the table already exists then it will not be recreated. I have enforced a compound unique constraint on `uid` and `title` columns so that the scraping process can be rerun and only new adverts will be added to the DB. I am making use of an auto-increminting id as the tables primary key.

## Testing

Tests are run on circleCI.

Tests cover most of the functions other than `scraper/scraper/utils:get_html`, `scraper/scraper/utils:parse_html` and `scraper/scraper/db:get_session` since these are very simple and would really just be re-testing library code. The entrypoint `scraper/scraper/main:main` is not unit tested but is tested in the end-to-end integration test within the container.

Integreation tests run against a testing webserver rather than the actual internet. I have copied the html for the target page on 23/06/19 and serve this in lieu of accesing the actual internet.

To run the tests locally;

```bash
pipenv run pytest tests/
```

## Misc

- code is linted using `pylint`
- code is formated using `black`
- all functions are type annotated

## NB

I did most of the coding for this exercise from the UK and the URL specified redirects to `https://www.heyjobs.co/en-gb/jobs-in-Berlin` whilst here - this page is empty and so this caused me some trouble!
