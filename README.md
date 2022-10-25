# Proxy Pool Console

## Feature

Manage all the proxy services.

Monitor proxy services is available or not.

Provide API for proxy pool, make different proxy services chosed evenly.

## Config

Edit src/.env file, add proxy service's ip an port.

## Run with docker

Whole command (copy and paste will run all the command, start proxy pool console directly)
```sh
docker build -t proxy_pool_console:1.0 .
docker run --name proxy_pool_console -p 7891 -d proxy_pool_console:1.0

```

## Rebuild and run

Whole command (copy and paste will run all the command, rebuild and run the proxy pool console directly).
```sh
docker stop proxy_pool_console
docker container rm proxy_pool_console
docker image rm proxy_pool_console:1.0
docker build -t proxy_pool_console:1.0 .
docker run --name proxy_pool_console -p 7891:7891 -d proxy_pool_console:1.0


```

## API

### GET /proxy

### GET /status