# -*- coding: utf-8 -*-
"""
Created on Sun Aug 30 12:11:34 2015

@author: Mengxiang Chen
"""

import urllib.request
 
url = "http://www.baidu.com/"
headers = ('User-Agent','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')
 
opener = urllib.request.build_opener()
opener.addheaders = [headers]
data = opener.open(url).read()
 
print(data)
