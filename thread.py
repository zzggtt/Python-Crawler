# -*- coding:utf-8 -*-
from threading import Thread
from urllib.parse import urljoin
import requests
import re

class Spider(Thread):
    def __init__(self, url, encoding='utf-8'):
        super().__init__()
        self.__url = url
        self.__encoding = encoding
        self.__headers = {
            "user-agent": "Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)"
        }
        self.__titile_re = re.compile(r'<title>(.*?)</title>', re.I|re.S)
        self.__links_re = re.compile(r'<a[^>]+href\s*=\s*["\']([^"\';#]+)["\'][^>]*>', re.I)
        self.title = ''
        self.links = set()

    def run(self):
        html = self.__download()
        self.title = self.__get_Title(html)
        self.links = self.__get_Links(html)


    def __download(self):
        try:
            r = requests.get(self.__url, headers=self.__headers, timeout=5)
        except requests.RequestException as err:
            html = None
            print(f'download{self.__url}error:{err}!')
        else:
            r.encoding = self.__encoding
            html = r.text
        return html

    def __get_Title(self, html):
        # 判断html是否为字符串:
        if not isinstance(html, str):
            return
        return ''.join(self.__titile_re.findall(html))

    def __get_Links(self, html):
        links = self.__links_re.findall(html)
        return {urljoin(self.__url, link) for link in links}


if __name__ == '__main__':
    url = 'https://github.com/hackxc/Pyhacker'
    t = Spider(url)
    t.start()
    t.join()
    biaoti = t.title
    lianjie = t.links
    print(biaoti)
    print(lianjie)
