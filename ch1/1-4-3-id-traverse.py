#-*- coding:utf-8 -*-

import urllib2
import chardet
import re

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


import itertools

def traverse_id():
    # maximum number of consecutive download errors allowed
    max_errors = 5
    # current number of consecutive download errors
    num_errors = 0

    for page in itertools.count(1):
        url = 'http://example.webscraping.com/view/%d' % page
        html = download(url)
        if html is None:
            # received an error trying to download this webpage
            num_errors += 1
            if num_errors == max_errors:
                # reached maximum number if
                # consecutive errors so exit
                break
        else:
            # success - can scrape the result
            # ...
            num_errors = 0

traverse_id()