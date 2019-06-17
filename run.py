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
from send_email import send_email


if __name__ == '__main__':

    nightly_data = get_nightly_data()

    message_field = get_message_field(nightly_data, ['energy'])

    if len(message_field) > 0:

        now_minus_two = datetime.utcnow() - timedelta(2)
        date = now_minus_two.strftime("%m/%d/%Y")
        subject = 'DOE RFP Alert {0}'.format(date)
        recipients = ['cdurant@armadapower.com']

        send_email('rfpsender@gmail.com', 'Rfpsender1!!',recipients, subject, message_field)

    else:
        print('No new RFP matching criteria')
