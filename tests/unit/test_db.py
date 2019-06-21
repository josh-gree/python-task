import pytest

from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

from scraper.db import Base, Advert


@pytest.fixture(scope="function")
def session():
    """
    Fixture for creating in memory sqlite db with 
    adverts table - yields a connection to this DB 
    and then cleans up.  
    """
    engine = create_engine("sqlite:///:memory:", echo=True)
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)


def test_commit_new(session):
    """
    Test that we are able to add a single row to 
    adverts table.
    """
    uid = "12345"
    title = "A Title"
    Advert.commit_new(uid=uid, title=title, session=session)

    res = session.query(Advert).first()

    assert res.id == 1
    assert res.uid == uid
    assert res.title == title


def test_commit_same_row_twice_raises_exception(session):
    """
    Test that unique constraint on uid,title works as expected
    """
    uid = "12345"
    title = "A Title"

    Advert.commit_new(uid=uid, title=title, session=session)
    with pytest.raises(IntegrityError):
        Advert.commit_new(uid=uid, title=title, session=session)
