FROM python:3.11-alpine

RUN adduser -D wikipedia
WORKDIR /home/wikipedia

COPY requirements.txt requirements.txt
RUN python3 -m venv venv
RUN pip3 --disable-pip-version-check --no-cache-dir install -r requirements.txt

COPY app app
COPY migrations migrations
COPY wikipedia.py run.py boot.sh ./

RUN chmod +x boot.sh
ENV FLASK_APP run.py
RUN chown -R wikipedia:wikipedia ./

USER wikipedia

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]