"""
util functions used in scraper
"""
from urllib.parse import urlparse
from requests import get
from bs4 import BeautifulSoup


def get_uid(url: str) -> str:
    """Extract uid of advert (last part of the path) from url

    Arguments:
        url {str} -- The url from which to extract the uid

    Returns:
        str -- The uid of the advert
    """
    parsed_url = urlparse(url)
    path = parsed_url.path
    uid = path.split("/")[-1]

    return uid


# Not testing these trust they do what they should
# only really using library functions...
def get_html(url: str) -> str:  # pragma: no cover
    """Function to make request to URL and return the
    text of the response

    Arguments:
        url {str} -- The url to make the request to

    Returns:
        str --  The text of the response
    """
    response = get(url)
    return response.text


def parse_html(html: str) -> BeautifulSoup:  # pragma: no cover
    """Function that returns a bs4 parsed html object

    Arguments:
        html {str} -- The html string to parse

    Returns:
        BeautifulSoup -- bs4 parsed html object
    """
    parsed_html = BeautifulSoup(html, features="html.parser")
    return parsed_html
