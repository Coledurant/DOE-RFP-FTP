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
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter, column_index_from_string
warnings.filterwarnings("ignore", category=UserWarning, module='bs4')

logger = logging.getLogger(__name__)

from send_email import send_email
from fbo_ftp_scraper import *
from scrapers import *

try:
    import configparser
except ImportError:
    import ConfigParser as configparser



if __name__ == '__main__':

    history()

    print('\n')
    print('--------------------------')
    print('     Running scrapers')
    print('--------------------------')

    conf = configparser.ConfigParser()
    config_file = os.path.join(os.path.dirname(__file__), "config.ini")
    conf.read(config_file)

    nightly_data_date = conf.get('FBO', 'nightly_data_date')
    if nightly_data_date == 'None':
        nightly_data_date = None
    else:pass

    notice_types_config = conf.get('FBO', 'notice_types')[:-1]
    notice_types = phrases_config.split(',')


    naics_config = conf.get('FBO', 'naics')[:-1]
    naics = naics_config.split(',')

    agencies_config = conf.get('FBO', 'agencies')[:-1]
    agencies = agencies_config.split(',')

    check_for_phrases_config = conf.get('FBO', 'check_for_phrases')
    check_for_phrases = bool(check_for_phrases_config.split(',')[0])

    check_for_agency_config = conf.get('FBO', 'check_for_agency')
    check_for_agency = bool(check_for_agency_config.split(',')[0])

    curr = os.getcwd()
    daily_message_dir = os.path.join(curr, 'data', 'FBO', 'daily_message')

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
        hasdata = True

    else:

        message_field = 'No new RFP matching criteria'
        hasdata = False

    if not os.path.exists(daily_message_dir):
        os.mkdir(daily_message_dir)
        history('created_dir', dir_location = daily_message_dir.split('RFPFinder')[1])
    os.chdir(daily_message_dir)
    with open("daily_message.txt", "w") as text_file:

        now_minus_two = datetime.utcnow() - timedelta(2)
        date = now_minus_two.strftime("%m/%d/%Y")
        text_file.write(date)

    with open("daily_message.txt", "a") as text_file:
        text_file.write('\n')
        text_file.write(message_field)

    history('fbo_daily_message', hasdata = hasdata)
    os.chdir(curr)

    print('   - FBO FTP finished')
    if not hasdata:
        print('      - No new RFP matching criteria')



    # SCRAPERS
    main()
