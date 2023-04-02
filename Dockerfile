FROM python:3.10-slim-buster
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction --no-ansi
COPY . .
ENTRYPOINT ["python", "./Datapao_IMDB/imdb_scrape.py"]
