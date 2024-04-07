# Landing generator

Generate landing pages with email collection in minutes.

![Screenshot of an example landing page](/screenshot.png)

## Introduction

The goal of this project is to provide a simple way to generate landing pages
with email collection. The landing pages are generated from a template and the
configuration file.

Several pages can be defined, by just providing their texts and other settings
in the configuration file. The pages are then rendered from the template during
the Docker container startup.

The email collection is done with a simple form that sends the email to the
backend, which stores it in a CSV file for each site.

Both the frontend and the backend are served by the same container, just with
one process per worker.

## Run it

First, set up the configuration with:

```shell
mkdir -p ./conf
cp config.example.yaml ./conf/config.yaml
# edit the config file to add or change the default landing pages
```


### Docker

```shell
docker run -it --rm \
  -p 8000:80 \
  --name landing_generator \
  -v ./conf/:/app/conf/:ro \
  -v ./data/:/app/data/ \
  -e ADMIN_SECRET=secret \
  ghcr.io/m0wer/landing_generator:master
```

### Docker compose

```shell
cp .env.example .env
# edit the .env file
docker compose up -d --build
```
