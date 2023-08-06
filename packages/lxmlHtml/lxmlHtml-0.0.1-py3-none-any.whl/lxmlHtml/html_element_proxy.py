# -*- coding: utf-8 -*-
import re
from urllib.parse import urljoin

from lxml import html, etree
from lxmlHtml.styles import Styles
from lxmlHtml.link import Link


class HtmlElementSerialize(object):
    """
    HtmlElement 代理类 序列化，属性操作相关
    """

    def __init__(self, element):
        self.root = element

    # 序列化，反序列化
    def __str__(self):
        return self.to_sting()

    def __repr__(self):
        return self.__str__()

    @classmethod
    def make_element(cls, tag, attrib=None, text='', tail='', *args, **kwargs):
        element = html.HtmlElement(tag, attrib, *args, **kwargs)
        element.text = text
        element.tail = tail
        return cls(element)

    @classmethod
    def make_comment(cls, *args, **kwargs):
        return html.HtmlComment(*args, **kwargs)

    @classmethod
    def from_fragment(cls, text, create_parent=False, base_url=None, parser=None, **kw):
        return cls(html.fragment_fromstring(text, create_parent, base_url, parser, **kw))

    @classmethod
    def from_document(cls, text, parser=None, ensure_head_body=False, **kw):
        return cls(html.document_fromstring(text, parser, ensure_head_body, **kw))

    def to_sting(self, pretty_print=False, include_meta_content_type=False,
                 encoding="unicode", method="html", with_tail=True, doctype=None):
        return html.tostring(self.root, pretty_print, include_meta_content_type,
                             encoding, method, with_tail, doctype)

    def url_join(self, href):
        return urljoin(self.root.base_url, href)

    def open_in_browser(self, encoding='utf-8'):
        html.open_in_browser(self.root, encoding)

    # 属性操作
    def get_attribute(self, key, default=None):
        return self.root.get(key, default)

    def set_attribute(self, key, value):
        self.root.set(key, value)

    def pop_attribute(self, key, default=None):
        return self.root.attrib.pop(key, default)

    def clear_attribute(self):
        self.root.attrib.clear()

    def has_attribute(self, key):
        return self.root.attrib.has_key(key)

    def get_attribute_keys(self):
        return self.root.keys()

    def get_attribute_values(self):
        return self.root.values()

    def get_attribute_items(self):
        return self.root.items()

    # 属性
    @property
    def attributes(self):
        return self.root.attrib

    @property
    def base(self):
        return self.root.base

    @property
    def tag(self):
        return self.root.tag

    @property
    def tail(self):
        return self.root.tail

    @property
    def text(self):
        return self.root.text

    @property
    def base_url(self):
        return self.root.base_url

    @property
    def body(self):
        return self.root.body

    @property
    def classes(self):
        """set"""
        return self.root.classes

    @property
    def styles(self):
        """orderDict"""
        return Styles(self.root.attrib)

    @property
    def forms(self):
        return self.root.forms

    @property
    def head(self):
        return self.root.head

    @property
    def label(self):
        return self.root.label


class HtmlElementProxy(HtmlElementSerialize):
    """
    HtmlElement 代理类 节点操作相关

    _Element https://lxml.de/api/lxml.etree._Element-class.html
    ElementBase https://lxml.de/api/lxml.etree.ElementBase-class.html
    HtmlMixin https://lxml.de/api/lxml.html.HtmlMixin-class.html
    HtmlElement https://lxml.de/api/lxml.html.HtmlElement-class.html

    """

    # 节点操作
    def add_next(self, element):
        self.root.addnext(element)

    def add_previous(self, element):
        self.root.addprevious(element)

    def get_next(self):
        return self.root.getnext()

    def get_previous(self):
        return self.root.getPrevious()

    def append(self, element):
        self.root.append(element)

    def insert(self, index, element):
        self.root.insert(index, element)

    def clear(self, keep_tail=False):
        self.root.clear(keep_tail)

    def remove(self, element):
        self.root.remove(element)

    def replace(self, old_element, new_element):
        self.root.replace(old_element, new_element)

    def extend(self, elements):
        self.root.extend(elements)

    def find(self, path, namespaces=None):
        return self.root.find(path, namespaces)

    def find_all(self, path, namespaces=None):
        return self.root.findall(path, namespaces)

    def find_text(self, path, default=None, namespaces=None):
        return self.root.findtext(path, default, namespaces)

    def get_children(self):
        return self.root.getchildren()

    def get_parent(self):
        return self.root.getparent()

    def get_root_tree(self):
        return self.root.getroottree(self)

    def index(self, child, start=None, stop=None):
        return self.root.index(self, child, start, stop)

    # 选择器
    def css(self, query, **kwargs):
        lst = []
        for element in self.root.cssselect(query, **kwargs):
            if isinstance(element, html.HtmlElement):
                lst.append(HtmlElementProxy(element))
            else:
                lst.append(element)
        return lst

    def re(self, pattern, flags=0):
        return re.findall(pattern, self.to_sting(), flags=flags)

    def re_first(self, pattern, default=None, flags=0):
        result = self.re(pattern, flags)
        if result:
            return result[0]
        else:
            return default

    def css_first(self, query, default=None, **kwargs):
        result = self.css(query, **kwargs)
        if result:
            return result[0]
        else:
            return default

    def xpath(self, query, **kwargs):
        lst = []
        for element in self.root.xpath(query, **kwargs):
            if isinstance(element, html.HtmlElement):
                lst.append(HtmlElementProxy(element))
            else:
                lst.append(element)
        return lst

    def xpath_first(self, query, default=None, **kwargs):
        result = self.xpath(query, **kwargs)
        if result:
            return result[0]
        else:
            return default

    # 扩展方法
    def drop_tag(self):
        """移除标签，不移除子节点"""
        return self.root.drop_tag()

    def drop_tree(self):
        """移除标签，移除子节点"""
        return self.root.drop_tree()

    def text_content(self):
        return self.root.text_content()

    def find_class(self, class_name):
        return self.root.find_class(class_name)

    def find_rel_links(self, rel):
        return self.root.find_rel_links(rel)

    def get_element_by_id(self, id, *default):
        return self.root.get_element_by_id(id, *default)

    def iter_links(self):
        for element, attribute, link, pos in self.root.iterlinks():
            yield Link(element, attribute, link, pos)

    def make_links_absolute(self, base_url=None, resolve_base_href=True, handle_failures=None):
        return self.root.make_links_absolute(base_url, resolve_base_href, handle_failures)

    def resolve_base_href(self, handle_failures=None):
        return self.root.resolve_base_href(handle_failures)

    def rewrite_links(self, link_repl_func, resolve_base_href=True, base_href=None):
        """newLink link_repl_func(oldLink) """
        return self.root.rewrite_links(link_repl_func, resolve_base_href, base_href)

    def strip_attributes(self, *attribute_names):
        etree.strip_attributes(self.root, *attribute_names)

    def strip_elements(self, *tag_names, with_tail=True):
        etree.strip_elements(self.root, *tag_names, with_tail=with_tail)

    def strip_tags(self, *tag_names):
        etree.strip_tags(self.root, *tag_names)

    def iter(self, tag=None, *tags):
        for element in self.root.iter(tag=tag, *tags):
            yield HtmlElementProxy(element)

    def iter_ancestors(self, tag=None, *tags):
        for element in self.root.iterancestors(tag=tag, *tags):
            yield HtmlElementProxy(element)

    def iter_children(self, tag=None, reversed=False, *tags):
        for element in self.root.iterchildren(tag=tag, reversed=reversed, *tags):
            yield HtmlElementProxy(element)

    def iter_descendants(self, tag=None, *tags):
        for element in self.root.iterdescendants(tag=tag, *tags):
            yield HtmlElementProxy(element)

    def iter_find(self, path, namespaces=None):
        for element in self.root.iterfind(path, namespaces):
            yield HtmlElementProxy(element)

    def iter_siblings(self, tag=None, preceding=False, *tags):
        for element in self.root.itersiblings(tag=tag, preceding=preceding, *tags):
            yield HtmlElementProxy(element)

    def iter_text(self, tag=None, with_tail=True, *tags):
        for text in self.root.itertext(tag=tag, with_tail=with_tail, *tags):
            yield text

    # 常用扩展
    def get_title(self, query='//title/text()'):
        return self.xpath_first(query)

    def get_description(self, query='//meta[@name="description"]/@content'):
        return self.xpath_first(query)

    def get_keywords(self, query='//meta[@name="keywords"]/@content'):
        return self.xpath_first(query)


Element = HtmlElementProxy
