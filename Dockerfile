FROM python:3.6.8-alpine

COPY run.py run.py

CMD [ "python", "run.py" ]
