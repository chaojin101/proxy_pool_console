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

## Usage

### REST API

**GET /proxy**

request example:

```sh
http://localhost:7891/proxy
```

return: string

return a random useful proxy "ip:port" if proxy pool has useful proxies else empty string.

response example:

```sh
55.55.55.55:7890
```

**GET /token**

request example:

```sh
http://localhost:7891/token
```

:return string

return a token, used to request /proxy?token={token}

response example:

```sh
hg9qhuh89oq4hf4iehoqh4
```

**GET /proxy?token={token}**

request example:

```
http://localhost:7891/proxy?token={token}
```

:return string

return a random useful proxy "ip:port" if proxy pool has useful proxies else empty string.

it will use token to return useful proxies evenly.

response example:

```
55.55.55.55:7890
```

**GET /status**

request example:

```
http://localhost:7891/status
```

:return json format string

"active": active ip's amount

"fail_proxies": all failed ip with error message

"total": total register proxy ip

response example:

```json
{
    "active": 4,
    "fail_proxies": [{
        "error message": "Timeout",
        "ip": "55.55.55.55:7890",
        "test_time": "2022-10-30 00:00:00"
    }],
    "total": 5
}
```