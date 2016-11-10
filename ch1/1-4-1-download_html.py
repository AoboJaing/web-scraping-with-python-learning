#-*- coding:utf-8 -*-

import urllib2
import chardet

def download(url, user_agent='wswp', num_retries=2):
    print 'Downloading: ', url
    headers = {'User-agent' : user_agent}
    request = urllib2.Request(url, headers=headers)

    try:
        html = urllib2.urlopen(request).read()
        charset = chardet.detect(html)['encoding']
        if charset == 'GB2312' or charset == 'gb2312':
            html = html.decode('GBK').encode('GB18030')
        else:
            html = html.decode(charset).encode('GB18030')
    except urllib2.URLError as e:
        print 'Download error', e.reason
        html = None
        if num_retries > 0:
            if num_retries > 0:
                if hasattr(e, 'code') and 500 <= e.code < 600:
                    # recursively retry 5xx HTTP errors
                    return download(url, user_agent, num_retries-1)
    return html

html = download('http://www.dytt8.net/')
# html = download('http://blog.csdn.net/github_35160620/article/details/52203682')
print html
