FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

COPY ./requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY ./app/ /app/
COPY ./template/ /app/template/
WORKDIR /app/

VOLUME /app/data
VOLUME /app/conf
