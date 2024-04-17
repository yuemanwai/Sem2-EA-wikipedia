ARG VARIANT=3-bullseye
FROM mcr.microsoft.com/vscode/devcontainers/python:0-${VARIANT}

ENV PYTHONUNBUFFERED 1

COPY requirements.txt /tmp/pip-tmp/
RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
   && rm -rf /tmp/pip-tmp

COPY app app
COPY migrations migrations
COPY wikipedia.py run.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP run.py

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]