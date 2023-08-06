import datetime
import os
from .Log import Log
from .HttpManager import HttpManager
from .Proxy import Proxy
from Util.DumperHelper import DumperHelper
from Util.JobHelper import debug


class JobBase:

    def __init__(self, *args, **kwargs):
        self.init_proxy()
        self.run_date = kwargs.get('run_date', datetime.datetime.now())
        self.log = Log(self.__class__.__name__)
        self.maxHourlyPageView = 600
        self.job_id = kwargs.get('job_id')
        self.run_id = kwargs.get('run_id')
        self._proxy_instance = Proxy()
        self.dumper = DumperHelper(**kwargs)

    def init_http_manager(self, timeout=30, default_header=False):

        manager = HttpManager(proxy=self._proxy_instance
                              , default_header=default_header
                              , log=self.log
                              , timeout=timeout
                              , max_hourly_page_view=self.maxHourlyPageView
        )

        return manager

    def download_page(self
                      , url: str
                      , manager: HttpManager
                      , max_retry: int = 10
                      , post_data: str = None
                      , validate_str_list: list = None
                      ):
        retry = 0
        page = ''
        while retry <= max_retry:
            retry += 1
            # When retry big then 1, need be write log
            if retry > 3:
                self.log.info('retry', str(retry))

            resp = manager.download_page(url, post_data=post_data)
            if not resp:
                continue
            page = resp.text

            for each in validate_str_list:
                if page and each in page:
                    return page

        return page

    def debug(self):
        return debug()

    def get_response(self, url
                     , manager
                     , max_retry=10
                     , post_data=None
                     ):
        retry = 0
        while retry <= max_retry:
            retry += 1
            # When retry big then 1, need be write log
            if retry > 3: manager.retry_log(url)

            resp = manager.download_page(url, post_data=post_data)
            if resp:
                return resp

        self.log.error("Retried all failed", "url => %s post_data => %s" % (url, post_data))
        return resp

    def on_run(self, **kwargs):
        pass

    def extract(self, **kwargs):
        return self.on_run()

    @property
    def proxy(self):
        return self._proxy_instance.proxy_pool

    @proxy.setter
    def proxy(self, value):
        self._proxy_instance.proxy_pool = value

    def init_proxy(self):
        self.LOCALHOST = '127.0.0.1:8888'
        self.NONE_PROXY = ''
        self.PROXY_SQUID_US_3 = os.getenv('PROXY_SQUID_US_3', '')
        self.LOCAL_PROXY_P4 = os.getenv('LOCAL_PROXY_P4', '')
        self.LOCAL_PROXY_P5 = os.getenv('LOCAL_PROXY_P5', '')
