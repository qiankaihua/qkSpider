# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

from selenium import webdriver
from scrapy.http import HtmlResponse
import time
from selenium.webdriver.chrome.options import Options

class JavaScriptMiddleware(object):

  def process_request(self, request, spider):
    print("PhantomJS is starting...")
    driver = webdriver.PhantomJS(
        executable_path="./phantomjs",
        service_args=["--ssl-protocol=any", "--ignore-ssl-errors=true", "--load-images=false", "--disk-cache=true"]
    ) #指定使用的浏览器
    # driver = webdriver.Firefox()
    driver.get(request.url)
    time.sleep(3)
    # js = "var q=document.documentElement.scrollTop=10000"
    # driver.execute_script(js) #可执行js，模仿用户操作。此处为将页面拉至最底端。
    # time.sleep(3)
    body = driver.page_source
    print ("访问"+request.url)
    return HtmlResponse(driver.current_url, body=body, encoding='utf-8', request=request)

class ChromeSpiderMiddleware(object):

    def __init__(self):
        option = Options()
        option.add_argument('--headless')
        self.driver = webdriver.Chrome(executable_path="./chromedriver",
                                       chrome_options=option)

    def process_request(self, request, spider):
        self.driver.get(request.url)
        print("页面开始渲染......")
        self.driver.execute_script("scroll(0, 1000);")
        time.sleep(5)
        rendered_body = self.driver.page_source
        print("页面完成渲染......")
        return HtmlResponse(request.url, body=rendered_body, encoding="utf-8")

    def spider_closed(self, spider, reason):
        print('驱动关闭')
        self.driver.close()


class LearnscrapySpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class LearnscrapyDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
