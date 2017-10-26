# IP地址取自国内髙匿代理IP网站：http://www.xicidaili.com/nn/
# 仅仅爬取首页IP地址就足够一般使用

from bs4 import BeautifulSoup
import requests
import threading


def get_ip_list(url, headers):
    web_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(web_data.text, 'lxml')
    ips = soup.find_all('tr')
    ip_list = []
    for i in range(1, len(ips)):
        ip_info = ips[i]
        tds = ip_info.find_all('td')
        ip_list.append('http://' + tds[1].text + ':' + tds[2].text)
    return ip_list


def test(i, ip_list, pr, url):
    p = {"http": ip_list[i]}
    try:
        html = requests.get(url, proxies=p)
    except Exception as e:
        pass
    print(i)
    pr.append(p)


def thre():
    url = 'http://www.xicidaili.com/nn/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; U; Android 2.3.6; en-us; Nexus S Build/GRK39F) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1'
    }
    ip_list = get_ip_list(url, headers)
    url = "https://m.weibo.cn/?&jumpfrom=weibocom"
    proxies = []
    # 多线程验证
    threads = []
    for i in range(len(ip_list)):
        thread = threading.Thread(target=test, args=[i, ip_list, proxies, url])
        threads.append(thread)
        thread.start()
    # 阻塞主进程，等待所有子线程结束
    for thread in threads:
        thread.join()
    return proxies

if __name__ == '__main__':
    p = thre()
    print(p)
