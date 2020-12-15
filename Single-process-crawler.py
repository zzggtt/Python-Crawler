# -*- coding:utf-8 -*-
import re
import requests
import time

# 爬取链接正则：
link_re = re.compile(r'<a[^>]+href\s*=\s*["\']([^"\']+)["\'][^>]*>', re.I)

# 百度spider user-agent:
headers = {
    "user-agent" : "Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)"
}

def fetch(url, encoding='utf-8'):
    print(f"正在下载:{url}")
    try:
        r = requests.get(url, headers=headers, timeout=10)
    except requests.RequestException as err:
        html = None
        print(err)
    else:
        r.encoding = encoding
        html = r.text
    return html

def extract_link(html, save):
    all_links = link_re.findall(html)
    for link in all_links:
        if not link.startswith('https://ask.seowhy.com'):
            continue
        save.write(f'{link}\n')
        save.flush()

def main():
    files = open('seowhy.txt', 'a+', encoding='utf-8')
    files.seek(0) #因为追加模式光标从末尾开始，需要手动移到开始位置，否则读取不到
    links = {l.strip() for l in files}
    seens = set()
    for link in links:
        if link in seens:
            continue
        html = fetch(link)
        if html is None: # 如果下载失败就跳过
            continue
        seens.add(link)
        extract_link(html, files)

if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time()
    print(f"总共耗时:{end - start}")
