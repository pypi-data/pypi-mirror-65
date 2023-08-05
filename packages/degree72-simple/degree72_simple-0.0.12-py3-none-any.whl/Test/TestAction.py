from Core.JobBase import JobBase
import json
from Test.TestDao import TestDao
from Util.DumperHelper import DumperHelper


class TestAction(JobBase):
    api_key = ''

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)

    def initialize(self):
        self.maxHourlyPageView = 1000000
        self.proxy = [self.PROXY_SQUID_US_3]
        if self.debug():
            self.proxy = [self.NONE_PROXY]
            self.proxy = [self.LOCALHOST]
        self._dao = TestDao(run_id=self.run_id,run_date=self.run_date, log=self.log)
        self.dumper = DumperHelper(schedule_interval='hour')

    def on_run(self):
        try:
            self.log.info("%s has started" % self.__class__.__name__,
                          "jobID:[%s]" % self.job_id)
            self.initialize()
            self.api_key = ''
            self.test()
            self.log.info("%s has finished" % self.__class__.__name__,
                          "jobID:[%s]" % self.job_id)
        except Exception as e:
            self.log.error("Unexpected/Unhandled Error", str(e))

    # def get_popularity(self, place_id):
    #     response = populartimes.get_id(self.api_key, place_id)
    #     # self.
    #     # for each in

    def test(self):
        self.log.error('error test')
        url = 'http://ip-api.com/json'
        # url = 'https://www.baidu.com'
        # page = self.download_page(url, self.init_http_manager(default_header=True), validate_str_list=[''])
        page = self.download_page(url, self.init_http_manager(default_header=True), validate_str_list=[''])
        self.dumper.dump_page(page, file_name='test.json')
    pass

    def test_file_name(self):
        import uuid
        check_dict = {}
        for i in range(0, 100):
            test = uuid.uuid4()


if __name__ == '__main__':
    t = TestAction()
    t.on_run()