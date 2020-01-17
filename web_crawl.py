import numpy as np
from bs4 import BeautifulSoup
import requests
import re
from  urllib.parse import urljoin
import collections as col

cur_url = input("put url: ")

cur_url = 'https://ssc.wisc.edu'
req = requests.get(cur_url)

dom = BeautifulSoup(req.text, 'html.parser')
hrefs = dom.find_all('a', href=True)
links = [urljoin(cur_url, a['href']) for a in hrefs]
#print((links))

filter_url = 'https://ssc.wisc.edu'
filter_url2 = '.htm'
filter_url3 = '.zip'
filter_url4 = '.pdf'
filter_url5 = '/DWE/'
filter_url6 = '/book/'
filter_url7 = '.exe'
whole_links = set()
# queue that feeds until recursively called links are already there
links_feeder = col.deque([])

def url_feed(url:str):
    try:
        print("inside")
        req = requests.get(url)
        dom = BeautifulSoup(req.text, 'html.parser')
        hrefs = dom.find_all('a', href=True)
        url = urljoin(cur_url, url)
        links = [urljoin(cur_url, a['href']) for a in hrefs]
        if not whole_links.__contains__(url):
            print("url joined: " + url)
            whole_links.add(url)
            print("url added: " + url)
            print("links added to feeder: " + str(links.__len__()))
            for l in links:
                # if link is in whole_urls, filter
                # filter outside initial cur_url, such as www.wisc.edu
                if (l.find(filter_url) != -1
                        and not whole_links.__contains__(l)
                        # and l.find(filter_url2, -5) != -1
                        # and l.find(filter_url4, -5) == -1
                        # and l.find(filter_url5) == -1
                        # and l.find(filter_url6) == -1
                        and l.find(filter_url7) == -1
                        and l.find(filter_url3) == -1):
                    print("url: " + l)
                    links_feeder.append(l)
                    print("ADDED feeder length: " + str(links_feeder.__len__()))
    except TimeoutError:
        print("Timeout Error but continue")
    if links_feeder.__len__() > 0:
        next_url = links_feeder.popleft()
        print("REMOVED feeder length: " + str(links_feeder.__len__()))
        print("next to chekc" + next_url)
        url_feed(next_url)
    return
def url_get_title(urls):
    title_list = []

    for url in urls:
        try:
            req = requests.get(url)
            dom = BeautifulSoup(req.text, 'html.parser')
            title = dom.title.get_text()
            while (title.__contains__('  ')
                    or title.__contains__('\t')
                    or title.__contains__('\r')
                    or title.__contains__('\n')):
                title = title.replace('  ', ' ')
                title = title.replace('\t', '')
                title = title.replace('\r', '')
                title = title.replace('\n', ' ')
            title_list.append(title)
            print("url: " + url)
            print(title)

        except TimeoutError:
            print("Timeout Error but continu")
            title_list.append('Nan')
    return title_list



# execution
url_feed(cur_url)
url_list = list(whole_links)
url_list.sort()
title_list = url_get_title(url_list)
a = np.array([url_list, title_list])
a = a.transpose()
np.savetxt('links.csv', a, '%s', delimiter=',')
