"""
Tests for DB model
"""
import pytest

from sqlalchemy import create_engine, inspect
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

from scraper.db import Base, Advert, create_model


@pytest.fixture(scope="function")
def session():
    """
    Fixture for creating in memory sqlite db with
    adverts table - yields a connection to this DB
    and then cleans up.
    """
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    sess = Session()
    yield sess
    sess.close()
    Base.metadata.drop_all(bind=engine)


def test_create_model():
    """
    Test that we are able to create the Advert model against
    a clean DB.
    """
    uri = "sqlite:///:memory:"

    engine = create_model(Advert, uri)
    insp = inspect(engine)

    tables = insp.get_table_names()

    assert len(tables) == 1
    assert tables[0] == Advert.__tablename__


# pylint: disable=redefined-outer-name
def test_commit_new(session):
    """
    Test that we are able to add a single row to
    the adverts table.
    """
    uid = "12345"
    title = "A Title"
    Advert.commit_new(uid=uid, title=title, session=session)

    res = session.query(Advert).first()

    assert res.id == 1
    assert res.uid == uid
    assert res.title == title


# pylint: disable=redefined-outer-name
def test_commit_same_row_twice_raises_exception(session):
    """
    Test that unique constraint on uid,title works as expected
    """
    uid = "12345"
    title = "A Title"

    Advert.commit_new(uid=uid, title=title, session=session)
    with pytest.raises(IntegrityError):
        Advert.commit_new(uid=uid, title=title, session=session)
