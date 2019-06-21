from sqlalchemy import Column, String, Integer, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import Session


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
