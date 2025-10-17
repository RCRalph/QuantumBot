FROM python:3.13.2-slim

WORKDIR /app

COPY pyproject.toml .
COPY LICENSE .
COPY ./config/languages ./config/languages
COPY ./src ./src

RUN pip install .

CMD ["python", "src/run_bot.py"]
