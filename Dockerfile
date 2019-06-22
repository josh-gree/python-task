FROM python:3.6.8-slim

WORKDIR /app

COPY Pipfile* /app/
COPY ./scraper /app/scraper

RUN pip install --no-cache-dir pipenv && pipenv install --clear --deploy

CMD ["pipenv", "run", "scrape"]