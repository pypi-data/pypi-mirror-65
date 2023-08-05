class Proxy:
    using_proxy = None

    def __init__(self, proxy_point=''):
        self.proxy_poing = proxy_point
        if proxy_point:
            self.using_proxy = {"https": "https://" + proxy_point, 'http': "http://" + proxy_point }








