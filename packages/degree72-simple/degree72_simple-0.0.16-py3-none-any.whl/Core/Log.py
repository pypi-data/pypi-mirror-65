import inspect
import logging
import os


class StructuredMessage(object):
    """docstring for StructuredMessage"""

    def __init__(self, subject, detail):
        super(StructuredMessage, self).__init__()
        self.subject = subject
        self.detail = detail

    def __str__(self):
        return '{}  {}'.format(self.subject, self.detail)


class Log(object):
    def __init__(self, log_name):
        self.log_name = log_name
        self.logger = self.init_log()
        self._ = StructuredMessage

    def init_log(self):
        logger = logging.Logger(self.log_name)
        logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        log_folder = os.path.join(os.path.dirname(inspect.stack()[3][1]), 'Log')
        if not os.path.exists(log_folder):
            os.mkdir(log_folder)
        fh = logging.FileHandler(os.path.join(log_folder, self.log_name + '.log'))

        fh.setFormatter(formatter)
        # todo add json part of log later, for elk search
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        logger.addHandler(fh)
        logger.addHandler(ch)
        return logger

    def info(self, subject, detail=''):
        self.log_dynamic_information()
        self.logger.info(self._(subject, detail))

    def error(self, subject, detail=''):
        self.log_dynamic_information()
        self.logger.error(self._(subject, detail))

    def warn(self, subject, detail=''):
        self.log_dynamic_information()
        self.logger.warn(self._(subject, detail))

    def log_dynamic_information(self):
        parent = inspect.stack()[2]
        frame, file, line, method, _, _ = parent
        source_file = file.split(r"/")[-1]
        print('{} - {} - {}'.format(source_file, line, method))
