'''The MIT License (MIT)

Copyright (c) 2016 Leon Li (leon@apolyse.com)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
associated documentation files (the "Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial
portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.'''

from bs4 import BeautifulSoup
import re, urllib2, time, sys, xlsxwriter, os.path
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool

def get_zips():
    # Get all zips from state and parse out the zip codes
    page = urllib2.urlopen('http://www.zipcodestogo.com/' + sys.argv[1] + '/').read()
    soup = BeautifulSoup(page, 'html.parser')
    zips = []
    for td in soup.findAll('td'):
        try:
            zips.append(int(td.text))
        except: pass
    # Return list of zip codes
    return zips

def work():
    zips = get_zips()
    # iterate through zip codes and get agents for each zip code
    for z in zips:
        try:
            get_agents(z)
        except Exception, e:
            if 'HTTP Error' in str(e) or 'timed out' in str(e):
                work()
            else:
                # write empty .xlsx and move on
                f = str(z) + '.xlsx'
                xbook = xlsxwriter.Workbook(f)
                xsheet = xbook.add_worksheet(str(z))
                xbook.close()

def get_agents(zip_code):
    z = zip_code
    details = []
    print 'getting agents for ' + str(z)
    start = time.time()
    page = 'http://www.zillow.com/agent-finder/?locationText=' + str(z)
    # get agent profile URLs for all 25 pages
    profiles = get_profiles(page)
    newprofiles = []
    for l in profiles:
        newprofiles.extend(l)
    # multi-threaded retrieval of agent info
    pool = ThreadPool(processes = 16)
    details = pool.map(get_agent_info, newprofiles)
    pool.close()
    pool.join()
    # clean details of agent
    for item in details:
        if item == 0:
            details.remove(item)
    print 'appended all for ' + str(z)
    end = time.time()
    print 'time elapsed: ' + str(end-start) + ' seconds'
    # write xlsx file with all the deets
    f = str(z) + '.xlsx'
    xbook = xlsxwriter.Workbook(f)
    xsheet = xbook.add_worksheet(str(z))
    row_index = 0
    for i in range(len(details)):
        if details[i] != 0:
            xsheet.write_row(row_index, 0, details[i])
            row_index += 1
    xbook.close()
    return details

def get_profiles_on_page(page):
    profiles = []
    req = urllib2.Request(page)
    req.add_header('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.107 Safari/537.36')
    soup = BeautifulSoup(urllib2.urlopen(req).read(), 'html.parser')
    # parse each URL and append the profile ones
    for link in soup.findAll('a'):
        try:
            if 'profile/' in link['href'] and '/Reviews' not in link['href']:
                profiles.append('http://www.zillow.com' + str(link['href']))
        except: pass
    return list(set(profiles))

def get_profiles(url):
    all_profiles = []
    url = url.replace('?', '?page=1&')
    urls = []
    for i in range(25):
        newurl = url.replace('page=1', 'page=' + str(i + 1))
        urls.append(newurl)
    # multi-threaded retrieval of profiles
    pool = ThreadPool(processes = 8)
    all_profiles = pool.map(get_profiles_on_page, urls)
    pool.close()
    pool.join()
    return all_profiles

def get_agent_info(profile):
    deets = []
    soup = BeautifulSoup(urllib2.urlopen(profile).read(), 'html.parser')
    for span in soup.findAll('span'):
        try:
            # locate screenname
            if 'screenname' in span['class']:
                deets.append(str(span.text))
        except: pass
    for dl in soup.findAll('dl'):
        try:
            # ascertain if buyer or seller agent, or both
            if 'specialties' in str(dl['class']):
                specialty = ''
                if 'Buyer' in str(dl.text):
                    specialty += 'Buyer '
                if 'Listing' in str(dl.text) or 'Sale' in str(dl.text):
                    specialty += 'Seller'
                deets.append(specialty)
        except: return 0
            
        if 'profile-information' in str(dl['class']):
            # locate company address
            address = dl.find('dd')
            address2 = ''
            company = address.text.replace(', CA', 'CA')
            for span in address.findAll('span'):
                address2 += span.text
                company = company.replace(span.text, '')
                if span == address.findAll('span')[0]:
                    address2 += '\n'
            address2 = address2.replace('CA', ', CA')
            address2 = address2.replace(u'\xa0', '')
            company = company.replace(u'\xa0', '')
            deets.append(company)
            deets.append(address2)
            deets.append(dl.findAll('dd')[1].text.replace('Click to view', ''))
    for a in soup.findAll('a'):
        # go onto their personal website and attempt to find an email
        if 'Website' in a.text:
            try:
                request = urllib2.Request(str(a['href']), headers={"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0"})
                contents = urllib2.urlopen(request, timeout=6).read()
                emails = re.findall(r'[\w\.-]+@[\w\.-]+', contents)
                if len(emails[0]) > 4 and '.' in emails[0]:
                    deets.append(emails[0])
            except: return 0
    if deets[2] == u'Click to view' or len(deets[1]) > 12 or len(deets[1]) < 4 or len(deets) < 6: return 0
    else: return deets

if __name__ == '__main__':
    work()
