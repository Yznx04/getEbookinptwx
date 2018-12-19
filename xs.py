import requests
import random
from lxml import etree

headers = {
    'user-agent':
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1)'
    ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/'
    '70.0.3538.110 Safari/537.36'
}


def get_proxies(self):
    """
    获取代理IP
    :param self:不需要传入
    :return: 返回一个str类型的值
    """
    proxie_url = 'xxxxxxxxxxxxxxxxxxxxxx'
    IP = requests.get(proxie_url).content.decode()
    init_proxies = 'http://{}'
    proxie_list = {}
    proxie = init_proxies.format(IP)
    proxie_list['http'] = proxie
    return proxie_list


def test_update_proxies_list(proxies_list):
    """
    进行检测并更新代理IP，如果ip不可以就更新
    :param proxies_list:
    :return:无返回
    """
    test_url = 'https://www.baidu.com'
    for proxies in proxies_list:
        test_num = requests.get(test_url, proxies=proxies).status_code
        if test_num != 200:
            proxies_list[proxies_list.index(proxies)] = get_proxies()


def get_response(url, proxies):
    """
    获取请求，其中使用做的处理有：使用代理IP
    :param url:
    """
    response = requests.get(url=url, headers=headers, proxies=proxies)
    response = etree.HTML(response.content.decode('gb18030', 'ignore'))
    return response


def get_url_list(response):
    """
    获取图书首页图书所有章节的URL
    :param response:
    :return: 一个list
    """
    url_list = response.xpath('/html/body/div[4]/div[1]/div[2]/ul/li/a/@href')
    return url_list


def get_name_content(response):
    """
    作用：提取页面的信息，并保存成txt文件
    :param response： response是一个可使用xpath的对象
    return: 无返回
    """
    novel = response.xpath('////text()')
    name = ''.join(novel[2]).split(',')[1]
    contenet = ''.join(novel).split("\xa0\xa0\xa0\xa0")[1:]
    contenet[-1] = contenet[-1].split('\r\n\r\n')[0]
    with open('天下第9.txt', 'a', encoding='utf-8') as f:
        f.write(name)
        f.write('\n')
        for c in contenet:
            f.write('        ' + c)
            f.write('\n')


if __name__ == '__main__':
    book_url = 'https://www.piaotian.com/html/9/9582/index.html'
    init_url = 'https://www.piaotian.com/html/9/9582/{}'
    proxies_list = [{
        'http':'http://42.179.220.149:27289'
    }, {
        'http':'http://218.66.163.250:64487'
    }, {
        'http':'http://36.25.43.222:45307'
    }, {
        'http':'http://111.183.93.252:16469'
    }, {
        'http':'http://61.174.156.29:46501'
    }]
    # Test and update the proxies list
    test_update_proxies_list(proxies_list)
    now_proxies = proxies_list[random.randint(0, 4)]
    response = get_response(url=book_url, proxies=now_proxies)
    url_list = get_url_list(response)
    for url in url_list:
        try:
            requests_url = init_url.format(url)
            get_name_content(get_response(requests_url, proxies=now_proxies))
            print(url_list.index(url), '|', len(url_list))
        except Exception as reason:
            print(reason)
            i = random.randint(1, 4)
            now_proxies = proxies_list[i]
            get_name_content(get_response(requests_url,proxies=now_proxies))
