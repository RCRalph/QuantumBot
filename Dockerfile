FROM python:3.13.2-slim AS base

WORKDIR /app

COPY pyproject.toml .
COPY LICENSE .
COPY ./config/languages ./config/languages
COPY ./src ./src

RUN pip install .

FROM base AS bot

CMD ["python", "src/run_bot.py"]

FROM base AS announcement

CMD ["python", "src/run_announcement.py"]
