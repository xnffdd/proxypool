# proxypool

API help
'''
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
'''
