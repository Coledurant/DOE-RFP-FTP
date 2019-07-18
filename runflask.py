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

from functools import reduce

from run import run

from flask import Flask, render_template, request, send_file
app = Flask(__name__)

###############################################################################
###############################################################################
###############################################################################

BASE_DIR = os.getcwd()
DATA_DIR = os.path.join(BASE_DIR, 'data')
if not os.path.exists(DATA_DIR):
    os.mkdir(DATA_DIR)

def get_directory_structure(rootdir):
    """
    Creates a nested dictionary that represents the folder structure of rootdir
    """
    dir = {}
    rootdir = rootdir.rstrip(os.sep)
    start = rootdir.rfind(os.sep) + 1
    for path, dirs, files in os.walk(rootdir):
        folders = path[start:].split(os.sep)
        subdir = dict.fromkeys(files)
        parent = reduce(dict.get, folders[:-1], dir)
        parent[folders[-1]] = subdir
    return dir


###############################################################################
###############################################################################
###############################################################################

@app.route("/", methods=['POST','GET'])
def index():

    if request.method == 'POST':
        print("Running")
        run()

    data_dir_structure = data_dir_structure = get_directory_structure(DATA_DIR)
    data_dir_structure = data_dir_structure.get('data')

    return render_template('index.html', data_dir_structure = data_dir_structure, data_url = DATA_DIR, data_dir_len = len(data_dir_structure))

@app.route('/download/<path:filepath>')
def downloadFile(filepath):
    #For windows you need to use drive name [ex: F:/Example.pdf]
    path = "{}/{}".format(DATA_DIR, filepath)
    return send_file(path, as_attachment=True)







if __name__ == "__main__":


    app.run()
