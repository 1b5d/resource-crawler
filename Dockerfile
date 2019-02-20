FROM python:2.7.15-stretch

COPY . /app
RUN cd app && pip install -r requirements.txt
ENTRYPOINT python app/main.py