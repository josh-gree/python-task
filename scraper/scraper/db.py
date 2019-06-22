from sqlalchemy import Column, String, Integer, UniqueConstraint, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.engine.base import Engine
from sqlalchemy.ext.declarative.api import DeclarativeMeta


Base = declarative_base()


class Advert(Base):
    """
    Table for storing advert information
    """

    __tablename__ = "adverts"

    id = Column(Integer, primary_key=True)
    uid = Column(String)
    title = Column(String)

    __table_args__ = (UniqueConstraint("uid", "title", name="uid_title_uc"),)

    @classmethod
    def commit_new(cls, uid: str, title: str, session: Session) -> None:
        """Commits a new advert to the adverts table
  
        Arguments:
            uid {str} -- uid of the advert
            title {str} -- title of the advert
            session {Session} -- sqlalcmhy session to a DB with this table
        """
        row = cls(uid=uid, title=title)
        session.add(row)
        session.commit()


def create_model(model: DeclarativeMeta, conn_str: str) -> Engine:
    """Creates a model in the DB specified by conn_str
    
    Arguments:
        model {DeclarativeMeta} -- sqlalchmy model definition
        conn_str {str} -- db connection string
    
    Returns:
        None
    """

    engine = create_engine(conn_str)
    Base.metadata.create_all(bind=engine, tables=[model.__table__])
    return engine


def get_session(engine: Engine) -> Session:
    """Get a sqlalchmy session to the DB specified 
    by engine.
    
    Arguments:
        engine {Engine} - sqlalchmy engine to DB
    
    Returns:
        Session -- A sqlalchmy session
    """
    session_factory = sessionmaker(bind=engine)
    ses = session_factory()
    return ses
