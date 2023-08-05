import os
import datetime
from time import time
from uuid import uuid4
import json
import inspect
from Util.JobHelper import debug
import tarfile


class DumperHelper:
    def __init__(self, **kwargs):
        now_dt = datetime.datetime.now()
        if kwargs.get('schedule_interval') == 'hour':
            date_folder = now_dt.strftime('%Y-%m-%d-%H')
        elif kwargs.get('schedule_interval') == 'minute':
            date_folder = now_dt.strftime('%Y-%m-%d-%H-%M')
        else:
            date_folder = now_dt.strftime('%Y-%m-%d')

        self.category = kwargs.get('category', '')

        if kwargs.get('file_folder'):
            self.file_folder = kwargs.get('file_folder')
        elif debug():
            self.file_folder = os.path.join(os.path.dirname(inspect.stack()[3][1]), 'Dump', date_folder, self.category)
        else:
            stack = inspect.stack()
            os.path.join(os.path.expanduser('~'), 'PageDump', os.path.basename(os.path.dirname(stack[3][1])),
                         date_folder, self.category)

        if not os.path.exists(self.file_folder):
            os.makedirs(self.file_folder)

    def dump_page(self, page: str, file_name=None, **kwargs):
        if not file_name:
            file_name = self.get_file_name()
        file = os.path.join(self.file_folder, file_name)
        with open(file, 'w', encoding='utf-8') as fh:
            fh.write(page)

    def dump_dict(self, item, file_name=None, **kwargs):
        if not file_name:
            file_name = self.get_file_name()
        file = os.path.join(self.file_folder, file_name)
        with open(file, 'w', encoding='utf-8') as fh:
            json.dump(item, fh)

    @staticmethod
    def get_file_name():
        return str(int(time())) + '_' + str(uuid4())

    @staticmethod
    def make_tarfile(output_filename, source_dir):
        with tarfile.open(output_filename, "w:gz") as tar:
            tar.add(source_dir, arcname=os.path.basename(source_dir))

if __name__ == '__main__':
    t = DumperHelper()
    result = t.get_file_name()
    print(result)

