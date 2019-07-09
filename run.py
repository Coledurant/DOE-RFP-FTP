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

from send_email import send_email
from fbo_ftp_scraper import *
from scrapers import *



if __name__ == '__main__':

    history()

    curr = os.getcwd()
    daily_message_dir = os.path.join(curr, 'data', 'FBO', 'daily_message')

    print('\n')
    # FBO FTP SCRAPER
    nightly_data = get_nightly_data()
    message_field = get_message_field(nightly_data)
    if len(message_field) > 0:
        now_minus_two = datetime.utcnow() - timedelta(2)
        date = now_minus_two.strftime("%m/%d/%Y")
        subject = 'DOE RFP Alert {0}'.format(date)
        recipients = ['cdurant@armadapower.com']

        # Run scrapers now and add any other emails to this one?

        send_email('rfpsender@gmail.com', 'Rfpsender1!!', recipients, subject, message_field)

    else:

        message_field = 'No new RFP matching criteria'

    if not os.path.exists(daily_message_dir):
        os.mkdir(daily_message_dir)
    os.chdir(daily_message_dir)
    with open("daily_message.txt", "w") as text_file:

        now_minus_two = datetime.utcnow() - timedelta(2)
        date = now_minus_two.strftime("%m/%d/%Y")
        text_file.write(date)

    with open("daily_message.txt", "a") as text_file:
        text_file.write('\n')
        text_file.write(message_field)
    os.chdir(curr)



    print('------------------------')
    print('Running scrapers')
    print('------------------------')
    print('   - FBO FTP finished')
    # SCRAPERS
    main()
