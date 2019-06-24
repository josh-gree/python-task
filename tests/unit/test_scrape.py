"""
Tests for scraping logic
"""
from typing import Callable

import pytest

from bs4 import BeautifulSoup
from scraper.utils import parse_html
from scraper.scraper import scrape, get_data, HTMLStructureChanged


@pytest.fixture()
def parsed_html() -> Callable:
    """Fixture that returns a function that reads a .html file
    and returns a bs4 parsed object.

    Returns:
        [Callable] -- function that returns parsed html from a file
    """

    def parsed_html_(path: str) -> BeautifulSoup:
        """Function that reads a .html file and returns a parsed
        bs4 object

        Arguments:
            path {str} -- The path to the .html file

        Returns:
            BeautifulSoup -- The parsed bs4 object
        """
        with open(path, "r") as html_file:
            html = html_file.read()

        return parse_html(html)

    return parsed_html_


# pylint: disable=redefined-outer-name
def test_parse_good(parsed_html):
    """
    Test that scrape function returns expected value when given
    well structured html
    """

    parsed = parsed_html("tests/unit/html/good.html")
    container_selector = "#ad-container"
    title_selector = "#title"

    got = scrape(parsed, container_selector, title_selector)
    assert sorted(got, key=lambda x: x["uid"]) == sorted(
        [{"uid": "1", "title": "A"}, {"uid": "2", "title": "B"}], key=lambda x: x["uid"]
    )


# pylint: disable=redefined-outer-name
def test_parse_no_ad_container(parsed_html):
    """
    Test that scrape function raises error when no ad container present
    """

    parsed = parsed_html("tests/unit/html/no_ad_container.html")
    container_selector = "#ad-container"
    title_selector = "#title"

    with pytest.raises(
        HTMLStructureChanged, match="There is not exactly one advert container!"
    ):
        scrape(parsed, container_selector, title_selector)


# pylint: disable=redefined-outer-name
def test_parse_multiple_ad_containers(parsed_html):
    """
    Test that scrape function raises error when multiple ad containers present
    """

    parsed = parsed_html("tests/unit/html/multiple_ad_containers.html")
    container_selector = "#ad-container"
    title_selector = "#title"

    with pytest.raises(
        HTMLStructureChanged, match="There is not exactly one advert container!"
    ):
        scrape(parsed, container_selector, title_selector)


# pylint: disable=redefined-outer-name
def test_parse_no_a_tags(parsed_html):
    """
    Test that scrape function raises error when ad containers has no a tags
    """

    parsed = parsed_html("tests/unit/html/no_a_tags.html")
    container_selector = "#ad-container"
    title_selector = "#title"

    with pytest.raises(
        HTMLStructureChanged, match="The advert container has no a tags!"
    ):
        scrape(parsed, container_selector, title_selector)


# pylint: disable=redefined-outer-name
def test_parse_a_tags_have_no_data(parsed_html):
    """
    Test that scrape function raises error none of the a tags contain all of
    required data.
    """

    parsed = parsed_html("tests/unit/html/a_tags_have_no_data.html")
    container_selector = "#ad-container"
    title_selector = "#title"

    with pytest.raises(
        HTMLStructureChanged,
        match="Unable to extract uid and title from any of the a tags!",
    ):
        scrape(parsed, container_selector, title_selector)


# pylint: disable=redefined-outer-name
def test_get_data_good_a_tag(parsed_html):
    """
    Test that we are able to extract both uid and title from an
    example of a good a tag
    """
    parsed = parsed_html("tests/unit/html/good_a_tag.html")
    a_tag = parsed.select("a")[0]
    title_selector = "#title"

    got = get_data(a_tag, title_selector)
    assert got == {"uid": "1", "title": "A"}


# pylint: disable=redefined-outer-name
def test_get_data_no_title(parsed_html):
    """
    Test that we get None if no title present in the
    a tag
    """
    parsed = parsed_html("tests/unit/html/a_tag_no_title.html")
    a_tag = parsed.select("a")[0]
    title_selector = "#title"

    got = get_data(a_tag, title_selector)
    assert got is None


# pylint: disable=redefined-outer-name
def test_get_data_no_uid(parsed_html):
    """
    Test that we get None if no uid present in the
    a tag
    """
    parsed = parsed_html("tests/unit/html/a_tag_no_uid.html")
    a_tag = parsed.select("a")[0]
    title_selector = "#title"

    got = get_data(a_tag, title_selector)
    assert got is None
