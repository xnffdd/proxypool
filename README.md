# proxypool

## API instruction
```
{
  "http api": [
    {
      "arguments": [
        {
          "default": 24, 
          "description": "the check time(hours) within now", 
          "name": "check_in_hour", 
          "required": false, 
          "type": "float"
        }, 
        {
          "default": null, 
          "description": "proxy protocol, ('http', 'https')", 
          "name": "protocol", 
          "required": false, 
          "type": "string"
        }, 
        {
          "default": null, 
          "description": "proxy anonymity, ('transparent', 'anonymous', 'high_anonymous')", 
          "name": "anonymity", 
          "required": false, 
          "type": "string"
        }, 
        {
          "default": null, 
          "description": "the response time(seconds) within", 
          "name": "response_time_in_second", 
          "required": false, 
          "type": "float"
        }
      ], 
      "description": "get an usable proxy", 
      "method": "GET", 
      "return": {
        "data": "the return data", 
        "msg": "error message", 
        "ret": "the return code, 0 means success"
      }, 
      "url": "/get"
    }, 
    {
      "arguments": [
        {
          "default": 24, 
          "description": "the check time(hours) within now", 
          "name": "check_in_hour", 
          "required": false, 
          "type": "float"
        }, 
        {
          "default": null, 
          "description": "proxy protocol, ('http', 'https')", 
          "name": "protocol", 
          "required": false, 
          "type": "string"
        }, 
        {
          "default": null, 
          "description": "proxy anonymity, ('transparent', 'anonymous', 'high_anonymous')", 
          "name": "anonymity", 
          "required": false, 
          "type": "string"
        }, 
        {
          "default": null, 
          "description": "the response time(seconds) within", 
          "name": "response_time_in_second", 
          "required": false, 
          "type": "float"
        }
      ], 
      "description": "get all usable proxies", 
      "method": "GET", 
      "return": {
        "data": "the return data", 
        "msg": "error message", 
        "ret": "the return code, 0 means success"
      }, 
      "url": "/get_all"
    }
  ]
}
```

## /get
```
{
  "data": {
    "anonymity": "high_anonymous", 
    "check_time": "2017-12-18 10:49:04", 
    "country": "CN", 
    "export_address": [
      "111.155.116.229"
    ], 
    "from": "西刺代理", 
    "grab_time": "2017-12-18 10:44:15", 
    "host": "111.155.116.229", 
    "port": "8123", 
    "protocol": "http", 
    "response_time": 7.54
  }, 
  "ret": 0
}
```
## /get_all/?anonymity=high_anonymous&response_time_in_second=1
```
{
  "data": [
    {
      "anonymity": "high_anonymous", 
      "check_time": "2017-12-18 16:28:27", 
      "country": "CN", 
      "export_address": [
        "59.110.62.128"
      ], 
      "from": "快代理", 
      "grab_time": "2017-12-14 15:08:39", 
      "host": "59.110.62.128", 
      "port": "8118", 
      "protocol": "http", 
      "response_time": 0.92
    }, 
    {
      "anonymity": "high_anonymous", 
      "check_time": "2017-12-18 10:49:22", 
      "country": "CN", 
      "export_address": [
        "120.27.10.38"
      ], 
      "from": "快代理", 
      "grab_time": "2017-12-14 18:24:11", 
      "host": "120.27.10.38", 
      "port": "8090", 
      "protocol": "http", 
      "response_time": 0.63
    }, 
    {
      "anonymity": "high_anonymous", 
      "check_time": "2017-12-18 10:49:09", 
      "country": "CN", 
      "export_address": [
        "123.118.1.198"
      ], 
      "from": "西刺代理", 
      "grab_time": "2017-12-18 10:44:15", 
      "host": "123.118.1.198", 
      "port": "8118", 
      "protocol": "http", 
      "response_time": 0.8
    }, 
    {
      "anonymity": "high_anonymous", 
      "check_time": "2017-12-18 10:49:04", 
      "country": "CN", 
      "export_address": [
        "59.34.204.60"
      ], 
      "from": "西刺代理", 
      "grab_time": "2017-12-18 10:44:18", 
      "host": "59.34.204.60", 
      "port": "808", 
      "protocol": "http", 
      "response_time": 0.74
    }
  ], 
  "ret": 0
}
```
