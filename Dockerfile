FROM python:3.11-alpine

RUN adduser -D wikipedia
WORKDIR /home/wikipedia

COPY requirements.txt requirements.txt
# RUN pip3 --disable-pip-version-check --no-cache-dir install -r requirements.txt

RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 python3 -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps

RUN pip install Flask==2.2.2

COPY app app
COPY migrations migrations
COPY wikipedia.py run.py boot.sh ./

RUN chmod +x boot.sh
ENV FLASK_APP=run.py
ENV FLASK_RUN_HOST=0.0.0.0
RUN chown -R wikipedia:wikipedia ./

USER wikipedia

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]