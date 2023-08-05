import numpy as np
import pandas as pd

from Util.MongoHelper import MongoHelper
from Core.Log import Log


class QaBase:
    file = None  # file to check
    qa_db = None
    collection_qa = None

    def __init__(self, **kwargs):
        self.mongo_hook = kwargs.get('mongo_hook')
        self.log = kwargs.get('log', Log(self.__class__.__name__))

    def check(self, **kwargs):
        if self.mongo_hook:
            self.qa_db = self.mongo_hook.get_conn()['QaReport']
        else:
            self.qa_db = MongoHelper().connect(**kwargs)['QaReport']
        self.collection_qa = self.qa_db[self.__class__.__name__]

    def check_data_from_file(self, **kwargs):
        pass

    def get_history_qa_result(self, qa_type: str, record_count=10):
        qas = []
        for each in self.collection_qa.find({'qa_type': qa_type}):
            each.pop('_id')
            each.pop('qa_type')
            qas.append(pd.DataFrame(each))

        qa_history = pd.concat(qas).sort_index(ascending=False).head(record_count)
        return qa_history

    def check_qa_result(self, qa_now: pd.DataFrame, qa_type: str, **kwargs):
        qa_history = self.get_history_qa_result(qa_type)

        for col in qa_history:
            try:
                data_history = qa_history[col]
                std = data_history.std()
                mean = data_history.mean()
                if mean is np.nan:
                    self.log.info('Col in Nan %s ' % col)
                    continue
                if col in qa_now.columns:
                    data_this_run = qa_now[col].values[0]
                else:
                    self.log.error('''PAY ATTENTION !!!! We don't have column {} in this run'''.format(col))
                    continue

                if mean - 3 * std <= data_this_run <= mean + 3 * std:
                    pass
                else:
                    self.log.error(
                        "Column %s not qualified\n mean %s std %s data this run %s" % (
                            str(col), str(mean), str(std), str(data_this_run)))
                    self.log.error("increase/decrease ratio is %s" % str((data_this_run - mean) / mean))
            except Exception as e:
                self.log.error("failed to process col %s except: %s" % (str(col), str(e)))

    def save_qa_result(self, qa_result: pd.DataFrame, qa_type: str):
        qa_result_dict = qa_result.to_dict()
        qa_result_dict['qa_type'] = qa_type
        self.collection_qa.insert_one(qa_result_dict)


    @staticmethod
    def read_data_from_file(file) -> pd.DataFrame :
        '''
        user pandas to read data from file
        :param file:
        :return: pandas data frame
        '''
        if str(file).split('.')[-1] == 'csv':
            df = pd.read_csv(file)
        else:
            raise ValueError('Unknown file type', file)
        return df

    def read_data_from_mysql(self, **kwargs):
        pass


if __name__ == '__main__':
    t = QaBase()
    t.check(file=r"C:\Users\Administrator\Downloads\canabis_qa_test\ca_cannabis_store_2019-11-21.csv", calc_history=True)