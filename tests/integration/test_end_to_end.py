"""
Test end to end usage in container
"""
import os
import json

from subprocess import Popen
from shlex import split
from sqlalchemy import create_engine

from scraper.db import Advert, get_session


def test_end_to_end():
    """
    Test usage within container. Simulate the internet with a testing webserver
    serving fixed html and check that the correct data is added to the DB.
    """
    # Simulate the internet!
    cmd = split("docker-compose run --rm start_dependencies_testing_webserver")
    testing_webserver = Popen(cmd)
    testing_webserver.wait()

    # Start pg
    cmd = split("docker-compose run --rm start_dependencies")
    postgres = Popen(cmd)
    postgres.wait()

    # run scraper
    cmd = split("docker-compose up scraper")
    scraper = Popen(
        cmd, env={**os.environ, "URL_TO_SCRAPE": "http://testing_webserver:8080"}
    )
    scraper.wait()

    # Query the adverts table in the DB
    engine = create_engine("postgresql://test:testpass@localhost:5432/heyjobs")
    session = get_session(engine)
    res = session.query(Advert.id, Advert.uid, Advert.title).all()
    session.close()

    # Check we get what we expect in the adverts table
    expected = [
        tuple(row)
        for row in json.load(open("tests/integration/expected_data/expected.json", "r"))
    ]
    assert res == expected

    # bring containers down
    cmd = split("docker-compose down")
    down = Popen(cmd)
    down.wait()
