"""
util functions used in scraper
"""

from requests import get
from bs4 import BeautifulSoup


def get_html(url: str) -> str:  # pragma: no cover
    """Function to make request to URL and return the
    text of the response
    
    Returns:
        [str] -- The text of the response
    """
    response = get(url)
    return response.text


def parse_html(html: str) -> BeautifulSoup:  # pragma: no cover
    """Function that returns a bs4 parsed html object
    
    Returns:
        [str] -- The html string to parse
    """
    parsed_html = BeautifulSoup(html, features="html.parser")
    return parsed_html
