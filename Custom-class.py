# -*- coding:utf-8 -*-
from multiprocessing import Process
import requests
import logging

# 配置日志等级:
logging.basicConfig(level=logging.INFO)

# 自定义类继承Process
class MySpider(Process):

    def __init__(self, urls):
        super().__init__()
        self.urls = urls
        self._headers = {
            "user-agent" : "Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)"
        }

    # 重写run():
    def run(self):
        while self.urls:
            url = self.urls.pop(0)
            html = self.download(url)
            if html is None:
                continue
            logging.info(f"get html's length:{len(html)}")

    # 抓取页面:
    def download(self, url, retries=3):
        try:
            r = requests.get(url, headers=self._headers, timeout=10)
        except requests.Timeout:
            html = None
            if retries > 0:
                return self.download(url, retries-1)
        except requests.RequestException as err:
            html = None
            logging.error(f'download {url} error:{err}!')
        else:
            r.encoding = 'utf-8'
            html = r.text
        return html


if __name__ == '__main__':
    with open("test.txt") as f:
        links = [l.strip() for l in f]
    s  = MySpider(links)
    s.start()
    s.join()

