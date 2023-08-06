# -*- coding: utf-8 -*-
from lxmlHtml import Element


def test_base():
    text = """
    <div>
        <span></span>
        <span></span>
        <span></span>
    </div>
    """
    element = Element.fragment_fromstring(text)

    # add some attribute
    first_span = element.cssselect('span')[0]
    print(first_span)

    first_span.set('width', '200px')
    first_span.styles.set('font-size', '20px')
    first_span.styles.set('max-width', '200px')
    first_span.classes.add('red')
    first_span.classes.add('green')

    # remove element
    element.xpath_first('//span[2]').drop_tag()

    # # get children
    print(element.getchildren())

    # # add element
    last_span = element.xpath_first("//span[last()]")
    print(last_span)

    ele = element.makeelement("p")
    c = element.makecomment("p")
    last_span.append(ele)
    last_span.append(c)

    # serialize
    print(element.tostring(pretty_print=True))
    """
    <div>
        <span width="200px" style="font-size: 20px; max-width: 200px;" class="red green"></span>
        
        <span><p></p>
<!--p--></span>
    </div>
    """


def test_func():
    import requests

    url = 'https://www.runoob.com/'
    response = requests.get(url)
    response.encoding = response.apparent_encoding
    text = """
    
    """
    print("ok")
    # text = "<div href='http://www.baidu.com' class='d sxx'><span>span<p>span</p></span></div>")
    tree = Element.document_fromstring(response.text, base_url=url)

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
    print(tree.urljoin("sdfasdf/1.html"))


if __name__ == '__main__':
    test_base()
    test_func()
