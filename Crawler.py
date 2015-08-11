
import datetime
import time
import sys
import os

import requests

reload(sys)
sys.setdefaultencoding('utf8')

class Crawler(object):
    def __init__(self):
        pass

    def get_page(self, url):
        return requests.get(url).text
