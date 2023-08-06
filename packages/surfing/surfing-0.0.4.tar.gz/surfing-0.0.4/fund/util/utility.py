from datetime import datetime
import sys
import os
from collections import defaultdict
import datetime
import numpy as np
import time
import json
import hashlib
import requests
from urllib.parse import urlencode

class Utility(object):

    @staticmethod
    def get_n_float(num, n):
        """
        只保留小数点后n位，不进行四舍五入
        :param num:
        :param n:
        :return:
        """
        base = pow(10, n)
        return int(num * base) / base
