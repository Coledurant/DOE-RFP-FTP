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

import shutil
import urllib.request as request
from contextlib import closing


def download_files():

    curr_dir = os.getcwd()

    root_ftp_url = 'ftp://ftp.fbo.gov/'

    DAY = timedelta(1)
    local_tz = get_localzone()
    now = datetime.now(local_tz)
    day_ago = local_tz.normalize(now - DAY)
    naive = now.replace(tzinfo=None) - DAY
    yesterday = local_tz.localize(naive, is_dst=None).strftime('%Y%m%d')

    model_name = 'FBOFeed' + yesterday
    model_files_url = root_ftp_url + model_name

    ftp_files_dir = os.path.join(curr_dir + '/' + 'ftp_files')

    if os.path.exists(ftp_files_dir):
        os.chdir(ftp_files_dir)
    else:
        os.mkdir(ftp_files_dir)
        os.chdir(ftp_files_dir)

    with closing(request.urlopen(model_files_url)) as r:
        with open(model_name, 'wb') as f:
            shutil.copyfileobj(r, f)



download_files()
