FROM python:3.6

COPY run.py run.py

CMD [ "python", "run.py" ]
