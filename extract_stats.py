"""
The script extracts all the links from "https://ssc.wisc.edu/sscc/pubs/stat.htm" targeting specifically
stat related links.
The content of this page was under #RightContentRightCol > div of the page, so I extracted all <a href> tags
with href under that html file.
Few filters were applied because some links directs to non-SSCC sites like "http://support.sas.com".
CSV file is saved as "links_stat.csv"
"""
from bs4 import BeautifulSoup
import urllib.parse as url
import pandas as pd
import requests

STAT_PAGE = "https://ssc.wisc.edu/sscc/pubs/stat.htm"
SSC_NETLOC = "ssc.wisc.edu"             # network location 1
SSC_NETLOC_WWW = "www.ssc.wisc.edu"     # network location 2

# parse html file
req = requests.get(STAT_PAGE)
dom = BeautifulSoup(req.text, 'html.parser')
stat_body = dom.select('#RightContentRightCol > div')[0]
link_tags = stat_body.select('a[href]')

# extract all the links
links = [t.get('href') for t in link_tags]
ssc_links = []

print("***************************************************************************************************************")

# filter and extract only the links under SSCC network location
for link in links:
    _, netloc, _, _, _, = url.urlsplit(link)
    if netloc:
        if netloc == SSC_NETLOC or netloc == SSC_NETLOC_WWW:
            ssc_links.append(link)
        else:
            print(link + " is excluded from migration")
    else:
        ssc_links.append(url.urljoin(STAT_PAGE, link))
ssc_links.sort()

print("***************************************************************************************************************")

# save file
df = pd.DataFrame(data=ssc_links, index=range(len(ssc_links)), columns=['url'])
print(df)
df.to_csv('links_stat.csv')
