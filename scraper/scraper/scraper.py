"""
Functions for extracting data from website
"""

from typing import List, Union, Dict
from bs4 import BeautifulSoup
from bs4.element import Tag

from scraper.utils import get_uid


class HTMLStructureChanged(Exception):
    """Custom Exception rasied when html structure no longer
    matches our assumptions.
    """


def scrape(
    parsed_html: BeautifulSoup, container_selector: str, title_selector: str
) -> List[Dict[str, str]]:
    """This function extracts the uid and title from each advert on the page.
    If the structure of the page has changed, no longer meets our assumptions,
    then raises an exception that will kill the entrypoint.

    Arguments:
        parsed_html {BeautifulSoup} -- bs4 parsed html object
        container_selector {str} -- css selector for the advert container
        title_selector {str} -- css selector for the title within the advert

    Raises:
        HTMLStructureChanged: Exception raised if page structure has changed

    Returns:
        List[Dict[str, str]] -- list of dicts containing uid, title for each advert
    """
    # get the container for the adverts
    container = parsed_html.select(container_selector)
    if len(container) != 1:
        raise HTMLStructureChanged("There is not exactly one advert container!")

    container = container[0]

    # get the a tags from the container
    a_tags = container.select("a")
    if a_tags == []:
        raise HTMLStructureChanged("The advert container has no a tags!")

    advert_data = [get_data(a_tag, title_selector) for a_tag in a_tags]

    # filter out the None values - this deals with the none advert a tags (used
    # for pagination)
    advert_data = [advert_datum for advert_datum in advert_data if advert_datum]

    # if we get no data back then something has gone wrong
    if advert_data == []:
        raise HTMLStructureChanged(
            "Unable to extract uid and title from any of the a tags!"
        )

    return advert_data


def get_data(a_tag: Tag, title_selector: str) -> Union[Dict[str, str], None]:
    """Extract uid and title from the a tag. If we fail to get either of
    these we return None.

    Arguments:
        a_tag {Tag} -- The a tag from which we want to extract uid and title
        title_selector {str} -- css selector of advert title within the a tag

    Returns:
        Union[Dict[str, str], None] -- dict with uid and title of advert or None
        if either is missing
    """

    href = a_tag.attrs.get("href", None)
    if not href:
        return None
    uid = get_uid(href)

    title = a_tag.select(title_selector)
    if len(title) != 1:
        return None
    title = title[0].text.strip()

    return {"uid": uid, "title": title}
