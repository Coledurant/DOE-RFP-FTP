from bs4 import BeautifulSoup
import requests
import warnings
import urllib.request
from contextlib import closing
import shutil
import re
from collections import Counter
import os
import json
import sys
from datetime import datetime, timedelta
import logging
warnings.filterwarnings("ignore", category=UserWarning, module='bs4')

logger = logging.getLogger(__name__)

from fbo_ftp_scraper import *


if __name__ == '__main__':

    nightly_data = get_nightly_data()

    read_data(nightly_data)
