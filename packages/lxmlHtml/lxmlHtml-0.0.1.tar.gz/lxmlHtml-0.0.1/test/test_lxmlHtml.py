# -*- coding: utf-8 -*-
from lxmlHtml import Element
import pytest


def test_func():
    import requests

    url = 'https://www.runoob.com/'
    response = requests.get(url)
    response.encoding = response.apparent_encoding
    text = """
    <p style="text-align: left;"><span style="color: rgb(136, 136, 136);font-size: 14px;text-align: justify;">8月8日，由品途集团主办的</span><strong style="color: rgb(136, 136, 136);font-size: 14px;text-align: justify;">2018&nbsp;NBI&nbsp;夏季创新峰会</strong><span style="color: rgb(136, 136, 136);font-size: 14px;text-align: justify;">在北京四季酒店举行，</span><strong style="color: rgb(136, 136, 136);font-size: 14px;text-align: justify;">汉能投资董事长兼CEO陈宏博士</strong><span style="color: rgb(136, 136, 136);font-size: 14px;text-align: justify;">作为人工智能专场的特邀嘉宾出席，并以</span><strong style="color: rgb(136, 136, 136);font-size: 14px;text-align: justify;">“人工智能中场战事”</strong><span style="color: rgb(136, 136, 136);font-size: 14px;text-align: justify;">为主题进行演讲，与现场观众共同分享了关于未来AI投资的新趋势与新机会。</span></p>
    """
    print("ok")
    # text = "<div href='http://www.baidu.com' class='d sxx'><span>span<p>span</p></span></div>")
    tree = Element.from_document(response.text, base_url=url)

    # print(tree)
    # tree.strip_elements('span')
    # re.findall('dfsdf\d+')
    # print(tree.xpath("//span"))
    tree.styles.set('xxx', 'value22')
    # print(tree)

    tree.styles.set('xxx1', 'value')
    # print(tree)

    tree.styles.pop('xxx1', 'value')
    # print(tree)

    # print(tree.styles.get('xxx'))
    print(tree.get_title())
    print(tree.get_description())
    print(tree.get_keywords())
    print(tree.url_join("sdfasdf/1.html"))


if __name__ == '__main__':
    test_func()
