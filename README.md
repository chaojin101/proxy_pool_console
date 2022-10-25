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

**GET /proxy**

:return str

return a useful proxy "ip:port"

if none useful proxy, it will return "None of one proxy ip works"

**GET /status**

:return json format str

"active": active ip's amount
"fail_ip": all failed ip with error message
"total": total register proxy ip

example:

{
    "Active": 4,
    "Fail_IP": [{
        "error message": "Timeout",
        "ip": "55.55.55.55:7890"
    }],
    "total": 5
}