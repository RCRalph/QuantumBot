FROM python:3.13.2-slim

WORKDIR /app

COPY . .

RUN pip install .

CMD ["python", "src/main.py"]
