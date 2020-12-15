# -*- coding:utf-8 -*-
import re
import requests
import time
from multiprocessing import Pool

# 爬取链接正则：
link_re = re.compile(r'<a[^>]+href\s*=\s*["\']([^"\']+)["\'][^>]*>', re.I)

# user-agent:
headers = {
    "user-agent" : "Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)"
}

# 抓取页面：
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

# 抓取页面中的链接：
def extract_link(html, save):
    all_links = link_re.findall(html)
    count = 0
    for link in all_links:
        if not link.startswith('https://ask.seowhy.com'):
            continue
        count += 1
    print(f'find {count} links')
        # save.write(f'{link}\n')
        # save.flush()

def run(link, files=None):
    html = fetch(link)
    if html is None:  # 如果下载失败就跳过
        return
    extract_link(html, files)


def main():
    files = open('test.txt', 'r', encoding='utf-8')
    # files.seek(0) # 因为追加模式光标从末尾开始，需要手动移到开始位置，否则读取不到
    links = {l.strip() for l in files}
    seens = set()
    process_list = []

    # 创建进程池
    pool = Pool(20) #创建一个20size的进程池
    # 创建并开始多进程:
    for link in links:
        if link in seens:
            continue
        seens.add(link)
        # 添加进进程池（异步）
        pool.apply_async(run, args=(link,))
        # p = Process(target=run, args=(link,))
        # p.start()
        # process_list.append(p)
    pool.close()
    pool.join()
    # 等待进程执行完毕后结束:
    # for p in process_list:
    #     p.join()


if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time()
    print(f"总共耗时:{end - start}")
