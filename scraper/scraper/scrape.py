"""
Main entypoint for running scraper - when module scraper is installed the main
function can be called by running `scrape`
"""
import os
from sqlalchemy.exc import IntegrityError
from scraper.db import Advert, create_model, get_session
from scraper.scraper import scrape, HTMLStructureChanged
from scraper.utils import get_html, parse_html


def main():
    """Main entrypoint for scraper. Creates needed tables and extracts
    data from website and stores in DB.
    """
    try:
        db_user = os.environ["DB_USER"]
        db_pw = os.environ["DB_PW"]
        db_host = os.environ["DB_HOST"]
        db_port = os.environ["DB_PORT"]
        db_name = os.environ["DB_NAME"]
    except KeyError:
        print(
            "connection env vars not all set - all of DB_USER,DB_PW,DB_HOST,DB_PORT and DB_NAME needed."
        )

    conn_str = f"postgres://{db_user}:{db_pw}@{db_host}:{db_port}/{db_name}"
    engine = create_model(Advert, conn_str)
    session = get_session(engine)

    try:
        url = os.environ["URL_TO_SCRAPE"]
        container_selector = os.environ["CONTAINER_SELECTOR"]
        title_selector = os.environ["TITLE_SELECTOR"]
    except KeyError:
        print(
            "scraping env vars not all set - all of URL_TO_SCRAPE,CONTAINER_SELECTOR and TITLE_SELECTOR needed."
        )

    # We try to scrape the data here - if it fails because the structure of
    # the page has changed or the page is not reachable we will get an exception
    # and exit.
    try:
        html = get_html(url)
    except ConnectionError as e:
        raise e

    parsed_html = parse_html(html)

    try:
        adverts = scrape(parsed_html, container_selector, title_selector)
    except HTMLStructureChanged as e:
        raise e

    for advert in adverts:
        # For each advert we have scraped try to add to the DB. We will
        # get an IntegrityError if we try to add a duplicate and then will
        # move on to next advert. This allows for running this same script
        # multiple times and only adding new data to db.
        try:
            Advert.commit_new(**advert, session=session)
        except IntegrityError:
            # need a new session
            session = get_session(engine)
            print("duplicate")
