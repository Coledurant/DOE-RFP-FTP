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

from fob_ftp import download_files

if __name__ == '__main__':

    download_files()
