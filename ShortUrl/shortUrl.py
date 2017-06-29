'''
Shorten URL v1.5

Github: https://github.com/hzlzh/Alfred-Workflows
Author: hzlzh (hzlzh.dev@gmail.com)
Twitter: @hzlzh
Blog: https://zlz.im/Alfred-Workflows/
'''

from __future__ import print_function
import urllib
import urllib2
import json
import sys
import re

def getLink(type,service,url):

    if (('http' in url) == False):
        url = 'http://'+url

    if type == 'goo.gl':
        terms = urllib.quote_plus(url.strip())
        data = json.dumps({"longUrl": url})
        clen = len(data)
        req = urllib2.Request(service,data,{'Content-Type': 'application/json', 'Content-Length': clen})
        f = urllib2.urlopen(req)
        data = f.read()
        output = json.loads(data)["id"]
    elif type == 'git.io':
        match = re.search('^(https?:\/\/)?(gist\.)?github.com', url)
        if match:
            terms = urllib.quote_plus(url.strip())
            data = urllib2.urlopen(url=service, data='url=' + terms)
            output = dict(data.info())['location']
        else:
            output = 'URL must be from github.com'
    else:
        try:
            terms = urllib.quote_plus(url.strip())
            url = service + terms
            data = urllib2.urlopen(url).read()
        except Exception, e:
            print('')
        if type == 'bit.ly':
            result = json.loads(data)
            if(result["status_code"] == 500):
                output = result["status_txt"]
            else:
                output = result["data"]["url"]
        elif type == 'j.mp':
            result = json.loads(data)
            if(result["status_code"] == 500):
                output = result["status_txt"]
            else:
                output = result["data"]["url"]
        elif type == 't.cn':
            result = json.loads(data)
            if('error_code' in result.keys()):
                output = result["error"]
            else:
                output = result["urls"][0]["url_short"]
        elif type == 'is.gd':
            result = json.loads(data)
            if('errorcode' in result.keys()):
                output = result["errormessage"]
            else:
                output = result["shorturl"]
        elif type == 'v.gd':
            result = json.loads(data)
            if('errorcode' in result.keys()):
                output = result["errormessage"]
            else:
                output = result["shorturl"]
    return output

temp = '{query}'
response = json.loads(temp)

type = response['type']
service = response['api_url']



last_output = getLink(type,service,url)

if ('http' in last_output):
    print(last_output, end='')
else:
    print('Error: '+ last_output, end='')
