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
from send_email import send_email
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

###############################################################################
###############################################################################
###############################################################################

# ROOT DIRS
curr_dir = os.getcwd()
data_dir = os.path.join(curr_dir, 'data')
if not os.path.exists(data_dir):
    os.mkdir(data_dir)
else:pass

# AEP DIRS
aep_dir = os.path.join(data_dir, 'AEP')
if not os.path.exists(aep_dir):
    os.mkdir(aep_dir)
else:pass
aep_ohio_dir = os.path.join(aep_dir, 'AEP Ohio')
aep_texas_dir = os.path.join(aep_dir, 'AEP Texas')
appalachian_power_dir = os.path.join(aep_dir, 'Appalachian Power')
indiana_michigan_dir = os.path.join(aep_dir, 'Indiana Michigan')
kentucky_power_dir = os.path.join(aep_dir, 'Kentucky Power')
public_service_company_of_oklahoma_dir = os.path.join(aep_dir, 'Public Service Company of Oklahoma')
southwestern_electric_power_company_dir = os.path.join(aep_dir, 'Southwestern Electric Power Company')

# Puerto Rico Government DIRS
puerto_rico_government_dir = os.path.join(data_dir, 'Puerto Rico Government')
if not os.path.exists(puerto_rico_government_dir):
    os.mkdir(puerto_rico_government_dir)
else:pass
puerto_rico_government_pdf_dir = os.path.join(puerto_rico_government_dir, 'puerto_rico_government_pdfs')

###############################################################################
###############################################################################
###############################################################################
# All
###############################################################################

def download_pdf(download_url, document_name):

    '''
    Downloads a pdf at the download_url location and saves it as document_name
    as lonf as document_name ends if .pdf
    Parameters:
        download_url (str): URL link for the pdf to download
        document_name (str): Name to save the downloaded pdf under (must end in .pdf)
    Returns:
        None - Just downloads the pdf
    '''
    response = urlopen(download_url)
    if document_name[-4:] != ".pdf":
        raise ValueError('document_name {0} did not end in .pdf'.format(document_name))
    else:pass
    file = open(document_name, 'wb')
    file.write(response.read())
    file.close()

def check_if_new(rfp):

    '''
    Not sure how to make this work for all yet
    '''

    return None

# AEP
###############################################################################

def extract_important_dates(soup):

    '''
    Parses soup html for important dates for aep sites
    Parameters:
        soup (bs4.BeautifulSoup): soup for parsing
    Returns:
        datetype_date_dict (dict): date title, date dict of all important dates
    '''
    datetype_date_dict = {}

    pars = soup.findAll('p')
    for p in pars:
        if len(p.findAll('span', attrs={'class':'bold'})) > 0:
            two_lines = p.text.replace(u'\xa0', u' ').split('\n')
            for line in [line for line in two_lines if len(line) > 0]:

                date_type, date = line.split(':  ')
                datetype_date_dict[date_type] = date

    if len(datetype_date_dict) > 0:

        # Was able to find important dates
        return datetype_date_dict

    else:

        # Keep looking
        for p in pars:
            if len(p.findAll('b')) > 0:
                dates_text = p.text
                dates_list = [s.replace('\r', '') for s in dates_text.split('\n') if len(s) > 0]
                datetype_date_dict = {s.split(': ')[0]:s.split(': ')[1] for s in dates_list}
                break
            else:pass

        return datetype_date_dict

def extract_correspondence_email(soup):

    '''
    AEP RFPs may have a correspondence email listed towards the bottom of their
    webpage, this will find those
    Parameters:
        soup (bs4.BeautifulSoup): soup for parsing
    Returns:
        correspondence_email (str): a string consisting of either an email, or None
    '''

    links = soup.findAll('a')
    try:
        correspondence_email = [link for link in [link for link in links if link.has_attr('href')] if 'mailto' in link['href'] and link.text != 'contact us'][0].text
    except:
        correspondence_email = 'None'

    return correspondence_email

def extract_rfp_desc(soup):

    '''
    Will get the first few <p> tags as long as they are incrementing by 1 in the list
    This should be redone soon...
    Parameters:
        soup (bs4.BeautifulSoup): soup for parsing
    Returns:
        new_desc (str): descripton listed on RFPs website formatted by paragraph
    '''

    content = soup.find('span', attrs={'id':'cphContentMain_GlobalUserControl1'})
    ps = [p for p in content.findAll('p')]
    new_ps = [p for p in ps if not p.find('b')]
    if len(ps) == len(new_ps):
        new_ps = [p for p in ps if not p.find('span')]
    else:pass
    shouldbe = 0
    desc = []
    for inum, p in enumerate(ps):
        if p in new_ps:
            num = inum
        else:pass
        if num != shouldbe:
            break
        else:
            desc.append(p)
        shouldbe += 1
    dstrs = [d.text for d in desc]
    new_desc = '\n \n'.join(dstrs)
    return new_desc

def aep_scrape(area_dir, url):

    '''
    Scrapes a single aep area webpage for rfps listed and saved all available information in that
    areas folder in the data dir
    Parameters:
        area_dir (var): the path to the areas folder
        url (str): URL to the areas webpage to scrape for RFPs
    Returns:

    '''

    if not os.path.exists(area_dir):
        os.mkdir(area_dir)
    else:pass

    html = requests.get(url).content
    soup = BeautifulSoup(html, 'lxml')
    pars = soup.findAll('p')
    if len([p for p in pars if 'There are currently no RFPs being offered.' in p]) > 0:pass
    else:
        rfp_offers = soup.findAll('strong')

        for rfp in rfp_offers:
            try:
                a = str(rfp.find('a')['href'])
                rfp_url = str(url.split('default.aspx')[0] + a)

                rfp_html = requests.get(rfp_url).content
                rfp_soup = BeautifulSoup(rfp_html, 'lxml')

                rfp_name = rfp_soup.find('h1').text

                pdf_list_elements = rfp_soup.findAll('li', attrs={'class':'pdf'})

                # Dict of pdf title and pdf link
                pdfs_dict = {element.text:url.split('.com')[0] + '.com' + element.find('a')['href'] for element in pdf_list_elements}
                rfp_dir = os.path.join(area_dir, rfp_name)
                if not os.path.exists(rfp_dir):
                    os.mkdir(rfp_dir)
                    new_rfp = True
                else:
                    new_rfp = False

                os.chdir(rfp_dir)

                downloaded_files = os.listdir()

                for pdf_name, pdf_url in pdfs_dict.items():
                    if '(' in pdf_name:
                        pdf_name = pdf_name.split('(')[0]
                    else:pass
                    pdf_name = pdf_name.replace(' ', '_') + '.pdf'

                    if not pdf_name in downloaded_files:
                        try:
                            download_pdf(pdf_url, pdf_name)
                        except Exception as e:pass
                    else:pass

                datetype_date_dict = extract_important_dates(rfp_soup)
                correspondence_email = extract_correspondence_email(rfp_soup)
                rfp_desc = extract_rfp_desc(rfp_soup)

                dates_string = ''
                for datetype, date in datetype_date_dict.items():
                    apstr = "     {0}: {1}".format(datetype, date) + "\n"
                    dates_string += apstr

                rfp_str = 'RFP Title: ' + rfp_name + '\n' + \
                'Correspondence Email: ' + correspondence_email + '\n' + \
                'Important Dates:' + '\n' + '\n' + \
                dates_string + '\n' + '\n' + \
                'Description:' + '\n' + \
                rfp_desc

                rfp_name_txt = rfp_name.replace(' ',  '_') + '.txt'
                with open(rfp_name_txt, 'w') as w:
                    w.write(rfp_str)
                    w.close()

                os.chdir(curr_dir)

                # Send an email out if this is a new RFP, move all emails to one place later
                if new_rfp:
                    subject = 'New AEP RFP Found'
                    recipients = ['cdurant@armadapower.com']
                    send_email('rfpsender@gmail.com', 'Rfpsender1!!',recipients, subject, rfp_str)
                else:pass

            except TypeError:pass

def aep():
    path_url_dict = {
        aep_ohio_dir:conf.get('aep', 'aep_ohio_url'),
        aep_texas_dir:conf.get('aep', 'aep_texas_url'),
        appalachian_power_dir:conf.get('aep', 'appalachian_power_url'),
        indiana_michigan_dir:conf.get('aep', 'indiana_michigan_url'),
        kentucky_power_dir:conf.get('aep', 'kentucky_power_url'),
        public_service_company_of_oklahoma_dir:conf.get('aep', 'public_service_company_of_oklahoma_url'),
        southwestern_electric_power_company_dir:conf.get('aep', 'southwestern_electric_power_company_url')
    }

    for area_dir, url in path_url_dict.items():
        aep_scrape(area_dir, url)

# Puerto Rico Government
###############################################################################

def puerto_rico_government(url = conf.get('puerto_rico_government', 'puerto_rico_government_url')):

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

# Main
###############################################################################
def main():

    aep()
    puerto_rico_government()

###############################################################################
###############################################################################
###############################################################################

if __name__ == '__main__':

    main()
