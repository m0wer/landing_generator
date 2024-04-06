# Landing generator

Generate landing pages wih email collection in minutes.

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
