FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

RUN groupadd --gid 1000 appuser \
    && useradd --uid 1000 --gid appuser --shell /bin/bash --no-create-home appuser

COPY ./requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY ./app/ /app/
COPY ./template/ /app/template/
WORKDIR /app/

RUN mkdir conf/ data/ static_pages/
RUN chown -R appuser:appuser /app/conf /app/data /app/static_pages

USER appuser

VOLUME /app/data
VOLUME /app/conf
