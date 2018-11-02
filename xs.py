import requests
from lxml import etree
from urllib.parse import urljoin

start_url = "https://www.piaotian.com/html/0/251/"
headers = {
    "User-Agent":
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 ("
    "KHTML,like Gecko) Chrome/70.0.3538.77 Safari/537.36"
}


def get_requests(url):
    """这个函数专门用来获取请求的,返回一个HTML格式的"""
    resp = requests.get(url=url, headers=headers).content.decode("gbk")
    html = etree.HTML(resp)
    return html


def get_url(html):
    """获取首页的所有章节的URL，方便后面爬取"""
    url_list = html.xpath("/html/body/div[4]/div[1]/div[2]/ul/li/a/@href")[4:]
    return url_list


def get_content(html):
    book = []
    name = "".join(html.xpath("/html/body/h1//text()"))
    content = "".join(
        ("".join(html.xpath("/html/body//text()")).split()[25:-23]))
    book.append(name)
    book.append(content)
    return book


def paere(book):
    book_str = ''.join(book)
    with open("十方天士.txt", 'a', encoding="utf-8") as f:
        f.write(book_str)


if __name__ == '__main__':
    index_html = get_requests(start_url)
    url_list = get_url(index_html)
    for url in url_list:
        requests_url = urljoin(start_url, url)
        book_html = get_requests(requests_url)
        book_content = get_content(book_html)
        paere(book_content)
