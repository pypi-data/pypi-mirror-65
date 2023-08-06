"""
basehttpx
"""
import traceback

import httpx

from re_common.baselibrary.utils.core.mlamada import closeResult
from re_common.baselibrary.utils.core.requests_core import USER_AGENT, set_proxy_httpx


class BaseHttpx(object):
    def __init__(self, logger=None):
        if logger == None:
            from re_common.baselibrary import MLogger
            logger = MLogger().streamlogger
        self.logger = logger
        self.proxies = None
        self.headers = {}
        self.sn = None

    def creat_sn(self, proxy=None, headers=None, verify=True, **kwargs):
        if proxy:
            self.proxies = set_proxy_httpx(proxy)
            kwargs["proxies"] = self.proxies
        if headers:
            kwargs["headers"] = headers
        if headers == "default":
            kwargs["headers"]['User-Agent'] = USER_AGENT
        kwargs["verify"] = verify
        self.sn = httpx.Client(**kwargs)
        return self.sn

    def base_sn_httpx(self, url, sn, endstring="", marks=[], **kwargs):

        r = None
        exMsg = None
        try:
            r = sn.get(url=url, **kwargs)
        except:
            exMsg = '* ' + traceback.format_exc()
            self.logger.error(exMsg)
        finally:
            closeResult(r)

        if exMsg:
            self.logger.info("判断到except，请求出项错误{}".format(exMsg))
            return False, "httpx", r

        if r.status_code != 200:
            self.logger.warning('r.status_code:' + str(r.status_code))
            return False, "code", r

        if endstring:
            """
            请求有可能是html或者json等，如果有需要判断html结束的才启动这个选项
            """
            html = r.text.strip()
            if not html.endswith(endstring):
                self.logger.info("not endswith {}".format(endstring))
                return False, "endString", r

        if marks:
            """
           验证请求是否成功  通过一个特征字符串或者html的标签来查找 保证下载的页面是我需要的页面
           而不是错误页面
           特征值有可能没有是网页出现问题  有可能是请求不完全 这个依照情况而定
            """
            html = r.text.strip()
            for mark in marks:
                if html.find(mark) == -1:
                    self.logger.info('not found {}'.format(mark))
                    return False, "Feature err", r
                else:
                    self.logger.info("found mark is {}".format(mark))

        return True, "", r

    def base_sn_post_httpx(self, url, sn, data=None, endstring="", marks=[], **kwargs):
        r = None
        exMsg = None
        try:
            r = sn.post(url=url, data=data, **kwargs)
        except:
            exMsg = '* ' + traceback.format_exc()
            self.logger.error(exMsg)
        finally:
            closeResult(r)

        if exMsg:
            self.logger.info("判断到except，请求出项错误{}".format(exMsg))
            return False, "httpx", r

        if r.status_code != 200:
            self.logger.warning('r.status_code:' + str(r.status_code))
            return False, "code", r

        if endstring:
            """
            请求有可能是html或者json等，如果有需要判断html结束的才启动这个选项
            """
            html = r.text.strip()
            if not html.endswith(endstring):
                self.logger.info("not endswith {}".format(endstring))
                return False, "endString", r

        if marks:
            """
           验证请求是否成功  通过一个特征字符串或者html的标签来查找 保证下载的页面是我需要的页面
           而不是错误页面
           特征值有可能没有是网页出现问题  有可能是请求不完全 这个依照情况而定
            """
            html = r.text.strip()
            for mark in marks:
                if html.find(mark) == -1:
                    self.logger.info('not found {}'.format(mark))
                    return False, "Feature err", r
                else:
                    self.logger.info("found mark is {}".format(mark))

        return True, "", r

    def httpx_get(self, url, params=None):
        """
         params = {'key1': 'value1', 'key2': 'value2'}
         r = httpx.get('https://httpbin.org/get', params=params)
         r.url
         params = {'key1': 'value1', 'key2': ['value2', 'value3']}
         r.status_code
         r.headers['content-type']
         r.encoding
         r.encoding = 'ISO-8859-1'
         r.content
         r.text
         r.json()
         /////////////////
         from PIL import Image
         from io import BytesIO
         i = Image.open(BytesIO(r.content))

        :param url:
        :return: r
        """
        if params:
            return httpx.get(url, params=params)
        return httpx.get(url)

    def httpx_post(self, url, data):
        """
        >>> r = httpx.put('https://httpbin.org/put', data={'key': 'value'})
        >>> r = httpx.delete('https://httpbin.org/delete')
        >>> r = httpx.head('https://httpbin.org/get')
        >>> r = httpx.options('https://httpbin.org/get')
        data={'key': 'value'}
        :param url:
        :param data:
        :return:
        """
        r = httpx.post(url, data=data)
        return r

    # def httpx_asyncclient(self, url):
    #     """
    #     Python 3.8+ with
    #     :param url:
    #     :return:
    #     """
    #     async with httpx.AsyncClient() as client:
    #         r = await
    #         client.get('https://www.example.org/')
    #     return r
