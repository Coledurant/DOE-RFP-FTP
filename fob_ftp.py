import urllib3
import datetime as dt
from ftplib import FTP
import requests
from bs4 import BeautifulSoup as bs
from tqdm import tqdm
import time
import re
import os
from datetime import datetime, timedelta
from tzlocal import get_localzone



def download_files():
    root_ftp_url = 'ftp://ftp.fbo.gov/'

    DAY = timedelta(1)
    local_tz = get_localzone()
    now = datetime.now(local_tz)
    day_ago = local_tz.normalize(now - DAY)
    naive = now.replace(tzinfo=None) - DAY
    yesterday = local_tz.localize(naive, is_dst=None).strftime('%Y%m%d')

    model_name = 'FBOFeed' + yesterday
    model_files_url = root_ftp_url + model_name

    #downloading part
    http = urllib3.PoolManager()
    r = http.request('GET', root_ftp_url)
    if r.status != 200:
        raise ValueError("The url the model files can't be loaded")
    else:
        soup = bs(r.data, 'html.parser')

    print(soup)

download_files()
