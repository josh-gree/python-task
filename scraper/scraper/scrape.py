import os
from scraper.db import Advert, create_model, get_session


def main():
    try:
        db_user = os.environ["DB_USER"]
        db_pw = os.environ["DB_PW"]
        db_host = os.environ["DB_HOST"]
        db_port = os.environ["DB_PORT"]
        db_name = os.environ["DB_NAME"]
    except KeyError:
        print(
            "connection env vars not all set - all of DB_USER,DB_PW,DB_HOST,DB_PORT and DB_NAME needed."
        )

    conn_str = f"postgres://{db_user}:{db_pw}@{db_host}:{db_port}/{db_name}"
    engine = create_model(Advert, conn_str)
    session = get_session(engine)
