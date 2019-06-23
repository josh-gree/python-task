from scraper.utils import get_uid


def test_get_uid():
    """
    Test that we get correct part of the url for the uid
    """
    url = "http://www.example.come/one/two/three?x=23&y=56"
    got = get_uid(url)

    assert got == "three"
