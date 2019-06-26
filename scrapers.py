from bs4 import BeautifulSoup
import requests
import warnings
import urllib.request
from urllib.request import urlopen
from contextlib import closing
import shutil
import re
from collections import Counter
import os
import json
import sys
from datetime import datetime, timedelta
import logging
import PyPDF2
warnings.filterwarnings("ignore", category=UserWarning, module='bs4')

logger = logging.getLogger(__name__)

try:
    import configparser
except ImportError:
    import ConfigParser as configparser

###############################################################################
###############################################################################
###############################################################################

conf = configparser.ConfigParser()
config_file = os.path.join(os.path.dirname(__file__), "config.ini")
conf.read(config_file)
phrases_config = conf.get('all', 'phrases')
phrases = phrases_config.split(',')

curr_dir = os.getcwd()
data_dir = os.path.join(curr_dir, 'data')
puerto_rico_government_pdf_dir = os.path.join(data_dir, 'puerto_rico_government_pdfs')

# Puerto Rico Government
###############################################################################

def download_pdf(download_url, document_name):
    response = urlopen(download_url)
    if document_name[-4:] != ".pdf":
        raise ValueError('document_name {0} did not end in .pdf'.format(document_name))
    else:pass
    file = open(document_name, 'wb')
    file.write(response.read())
    file.close()


def puerto_rico_government(url = conf.get('all', 'puerto_rico_government_url')):

    '''
    Scrapes http://www.p3.pr.gov/prepa-transformation.html for new PREPA RFPs
    Downloads PDFs from RFP links and attemps to read them
    Parameters:
        url (str): Defaults (and should not be changed) to the url above, and
                    gets that url from the config file
    Returns:
        ---
    '''

    pdf_link = 'http://www.p3.pr.gov/'

    html = requests.get(url).content
    soup = BeautifulSoup(html, 'lxml')

    rfp_links = soup.findAll('li', attrs={'class':'T-tulos-para-Comunicados-Noticias LinkStyle-Table'})
    pdf_links = [link for link in [str(pdf_link + link.find('a')['href']) for link in rfp_links] if link[-4:] == '.pdf']

    if os.path.exists(puerto_rico_government_pdf_dir):
        os.chdir(puerto_rico_government_pdf_dir)
    else:
        os.mkdir(puerto_rico_government_pdf_dir)
        os.chdir(puerto_rico_government_pdf_dir)

    downloaded_files = os.listdir()
    try:
        for link in pdf_links:
            fname = link.split('/assets/')[1]
            if fname not in downloaded_files:
                download_pdf(link, fname)
            else:

                # This file has already been downloaded
                pass
    except Exception as e:
        print(e)
    finally:
        os.chdir(curr_dir)





###############################################################################
###############################################################################
###############################################################################

if __name__ == '__main__':

    puerto_rico_government()
