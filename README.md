# proxypool

自建免费代理IP池

## 功能

- 自动爬取互联网上公开的免费代理IP（目前已支持西刺代理、快代理、IP181）
- 周期性验证代理IP有效性
- 提供http接口获取可用IP

## 系统架构

![系统架构](https://raw.githubusercontent.com/lsdir/proxypool/master/image/architecture.png)

## HTTP接口

### 1. 获取单个可用IP

##### 基本信息

URL|http://localhost:9999/get
:---|:---
HTTP请求方式|GET
方法返回|JSON

##### 请求参数（bodyParam）

参数名|类型|必填|参数位置|描述|默认值
---|---|---|---|---|---
check_in_hour|float|否|urlParam|代理最后验证时间（小时）以内|24
response_time_in_second|float|否|urlParam|代理响应时间（秒）以内|null
protocol|string|否|urlParam|代理网络协议，http/https|null
anonymity|string|否|urlParam|代理匿名性，transparent/anonymous/high_anonymous|null

##### 请求示例（Python示例）

```
    #!/usr/bin/env python3
    # -*- coding: utf-8 -*-

    import requests

    url = "http://localhost:9999/get"
    querystring = {"anonymity":"high_anonymous","response_time_in_second":"1.5"}
    response = requests.request("GET", url, params=querystring)

    print(response.json())
```

##### JSON返回示例

```
{
    "ret": 0,
    "data": {
        "anonymity": "high_anonymous",
        "check_time": "2017-12-20 13:55:17",
        "country": "CN",
        "export_address": [
            "120.25.253.234"
        ],
        "from": "快代理",
        "grab_time": "2017-12-20 13:54:55",
        "host": "120.25.253.234",
        "port": "8118",
        "protocol": "http",
        "response_time": 1.45
    }
}
```

### 2. 获取全部可用IP

##### 基本信息

URL|http://localhost:9999/get_all
:---|:---
HTTP请求方式|GET
方法返回|JSON

##### 请求参数（bodyParam）

参数名|类型|必填|参数位置|描述|默认值
---|---|---|---|---|---
check_in_hour|float|否|urlParam|代理最后验证时间（小时）以内|24
response_time_in_second|float|否|urlParam|代理响应时间（秒）以内|null
protocol|string|否|urlParam|代理网络协议，http/https|null
anonymity|string|否|urlParam|代理匿名性，transparent/anonymous/high_anonymous|null

##### 请求示例（Python示例）

```
    #!/usr/bin/env python3
    # -*- coding: utf-8 -*-

    import requests

    url = "http://localhost:9999/get_all"
    querystring = {"anonymity":"high_anonymous","response_time_in_second":"1.5","protocol":"https"}
    response = requests.request("GET", url, params=querystring)

    print(response.json())
```

##### JSON返回示例

```
{
    "ret": 0,
    "data": [
        {
            "anonymity": "high_anonymous",
            "check_time": "2017-12-20 14:10:25",
            "country": "CN",
            "export_address": [
                "118.114.77.47"
            ],
            "from": "西刺代理",
            "grab_time": "2017-12-20 14:09:36",
            "host": "118.114.77.47",
            "port": "8080",
            "protocol": "https",
            "response_time": 1.41
        },
        {
            "anonymity": "high_anonymous",
            "check_time": "2017-12-20 13:09:40",
            "country": "CN",
            "export_address": [
                "119.29.178.21"
            ],
            "from": "西刺代理",
            "grab_time": "2017-12-14 16:17:52",
            "host": "119.29.178.21",
            "port": "8118",
            "protocol": "https",
            "response_time": 1.11
        }
    ]
}
```

## 讨论

邮箱：498541859@qq.com
