import requests
from lxml import etree
from urllib.parse import urljoin

start_url = "http://www.365essay.com/linqingxuan/"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36"
}

def get_request(request_url):
    """
    这个函数为了获取一个页面的所有信息
    param request_url:
    return:返回一个html的类，方便后面处理
    """
    response = requests.get(url=request_url, headers=headers)
    response_str = response.content.decode('gb2312')
    html = etree.HTML(response_str)
    return html

def get_url_list(html):
    """
    处理详情页，获取网页的信息
    :param 传入html:
    :return: 返回一个urllist
    """
    url_list = html.xpath("//a/@href")[1:]
    return url_list

def get_content(html):
    """
    传入html对象，提取详情页
    :param html:
    :return 返回一个list，每一篇文章一个list，包含名字和内容:
    """
    book = []
    name = "".join(html.xpath("///text()")).split()[0]
    content = ''.join("".join(html.xpath("///text()")).split()[8:-10])
    book.append(name)
    book.append(content)
    return book

def pare(book):
    """
    保存书籍
    :param book:
    :return:无返回
    """
    name = book[0]
    content = book[1]
    with open("林清玄散文1.txt", "a", encoding="utf-8") as f:
        f.write(name)
        f.write("\n")
        f.write(content)


if __name__ == "__main__":
    html = get_request(start_url)
    url_list = get_url_list(html)
    # print(url_list)
    for url in url_list:
        requests_url = urljoin(start_url, url)
        content_html = get_request(requests_url)
        book = get_content(content_html)
        pare(book)