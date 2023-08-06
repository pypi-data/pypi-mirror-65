import os


def debug():
    return not (os.getenv('PRODUCTION') == 'TRUE')



