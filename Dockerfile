FROM python:3.10-slim-buster

LABEL maintainer="Benjamin Montgomery <ben@montynet.io>" \
      version="0.0.1"

WORKDIR /notifier

RUN adduser --no-create-home --disabled-password --disabled-login notifier

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY --chown=notifier:notifier . .

ENV PYTHONPATH=/notifier/notifier

USER notifier

CMD ["python3", "notifier-server.py"]
