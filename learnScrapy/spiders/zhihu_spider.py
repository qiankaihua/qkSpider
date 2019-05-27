import scrapy
import re

import json

class QuotesSpider(scrapy.Spider):
    name = "zhihu"
    start_urls = [
        'https://spec.csdn.net/',
        # 'https://www.zhihu.com/question/22803406',
        # 'https://zhuanlan.zhihu.com/WhyPlus'
        # 'http://ms.uestc.edu.cn/'
        # 'https://zhuanlan.zhihu.com/keepitreal'
    ]

    # url = ''
    # el_class = []
    # el_id = None
    # nxt_url = ''
    # child_class_list = []

    parentCss = ''
    childCss = {}

    # print(class_dict)
    # print(_id)
    # print(url)
    # print(nxt_url)
    # print(child_class_list)
    #
    def __init__(self, arg = None):
        super().__init__()
        self.start_urls = []
        url = ''
        el_class = []
        el_id = None
        # nxt_url = ''
        child_class_list = []
        if arg is not None:
            data = json.loads(arg)
            # nxt_url =  data.get('nxt_url', '')
            url = data.get('url', '')
            el_class = data.get('el_class', [])
            el_id = data.get('el_id', None)
            child_class_list = data.get('child_class_list', [])
        if url != '':
            self.start_urls.append(url)
        # if nxt_url != '':
        # 如果class是空的就用id来判
        if el_class is None or len(el_class) == 0:
            self.parentCss = '#' + str.strip(el_id)
        else:
            class_name = ''
            for c_no in el_class:
                class_name = class_name + '.' + el_class[c_no] + ' '
            self.parentCss = str.strip(class_name)
        for child in child_class_list:
            key = child.get('index', None)
            value = child.get('className', None)
            if key is not None and value is not None:
                self.childCss[key] = format_child_css(value)

    def parse(self, response):
        # print(response.text)
        # for article in response.css('.fl .spec-content-txt'):
        # print('父元素class:',self.parentCss)
        # print('子元素class:', self.childCss)
        for article in response.css(self.parentCss):
            data = {}
            for key in self.childCss:
                # print(key, self.childCss[key])
                data[key] = clean(article.css(self.childCss[key]).extract())
            yield data
            # yield {
            #     'test': clean(article.css('.spec-tittle ').css('a::text').extract())
            # }
        # for article in response.css('body > div.main_content_frame > div > div.products > div'):
        #     yield {
        #         'test': article.css('div.product_right *::text').extract(),
        #         # 'title': article.css('div.product_right > h2::text').get(),
        #         # 'content': article.css('div.product_right > ul > li::text').get(),
        #     }

def clean(items):
    for idx, item in enumerate(items):
        match_obj = re.match(r'^[\t\n ]*$', item)
        if match_obj:
            items[idx] = ''
    return items

def format_child_css(css):
    format_css = str.strip(css)
    if format_css[-1] == '>':
        format_css = format_css[:-1]
    format_css = str.strip(format_css) + '::text'
    return format_css