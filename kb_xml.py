from bs4 import BeautifulSoup
import urllib.parse as url
import os
import pandas as pd
import requests


def set_xml_document(kb_title='.', kb_keywords='.',
                     kb_summary='.', kb_body='.',
                     kb_int_notes='', img_base_url=''):
    """
    all the default values for parameters are .
    return value will be the string of correct format inside <kb_document> and </kb_document>
    """
    # start xml document file
    # some tag might need to type convert to str like kb_body
    xml_document = '<kb_document>\n'
    xml_document = xml_document + '<kb_title>' + kb_title + '</kb_title>\n'
    xml_document = xml_document + '<kb_keywords>' + kb_keywords + '</kb_keywords>\n'
    xml_document = xml_document + '<kb_summary>' + kb_summary + '</kb_summary>\n'
    xml_document = xml_document + '<kb_body>\n' + str(kb_body) + '\n</kb_body>\n'
    # xml_document = xml_document + '<kb_int_notes>' + kb_int_notes + '</kb_int_notes>\n'
    xml_document = xml_document + '<img_base_url>' + img_base_url + '</img_base_url>\n'
    xml_document = xml_document + '</kb_document>\n'

    return xml_document


links_df = pd.read_csv('links_pub.csv')

links = links_df['Current URL']
links = links.to_list()
titles = links_df['Title']
titles = titles.to_list()

# start xml_documents
xml_documents = '<?xml version="1.0"?>\n<kb_documents>\n'

# inputs here, batch length, batch id
links_from = int(input("from what index to start: "))
links_num = int(input("how many links to batch: "))
batch_id = input("batch id: ")
log_text = ''
for i in range(links_from, links_from + links_num):
    try:

        req = requests.get(links[i])
        dom = BeautifulSoup(req.text, 'html.parser')
        kb_body = dom.select('#RightContent')[0]
        print(kb_body)

        # decompose revised date
        # assume if there is revised date, only last one should be deleted
        revised_date = kb_body.select('.reviseDate')
        if len(revised_date):
            revised_date[-1].decompose()

        # decompose doc title
        # assume there is only one h1 or none
        dom_title = kb_body.select('h1')
        if len(dom_title):
            dom_title[0].decompose()

        # update image url path -> giving it absolute path
        link = links[i]
        images = kb_body.select('img')
        images_base_url = []
        if len(images):
            for image in images:
                image['src'] = url.urljoin(link, image['src'])
                images_base_url.append(image['src'])

        # update links -> absolute link
        hrefs = kb_body.find_all(href=True)
        if len(hrefs):
            for href in hrefs:
                # check.xml for fragment (#abc)
                parse_result = url.urlparse(href['href'])
                # if path string is not empty
                if parse_result[2]:
                    href['href'] = url.urljoin(link, href['href'])
        hrefs = kb_body.find_all(href=True)

        kb_body = BeautifulSoup(str(kb_body), 'html.parser')
        kb_body.find('div').unwrap()
        kb_body.smooth()
        kb_body = str(kb_body)

        # this kb_body will still contain tag for html <body></body>
        # let me know if this needs to be deleted
        kb_title = titles[i]

        # img_base_url
        img_base_url = ', '.join(images_base_url)

        xml_document = set_xml_document(kb_title=kb_title, kb_body=kb_body, img_base_url=img_base_url)
        xml_documents = xml_documents + xml_document

        # record batch id for the link
        links_df['Batch'][i] = batch_id

        # log
        log_text += str(i) + ': ' + links[i] + '\tsuccess\r'
    except Exception as e:
        log_text += 'ERROR - ' + str(e) + ' ' + str(i) + ': ' + links[i] + '\tfail\r'


# end xml_documents
xml_documents = xml_documents + '</kb_documents>'

log_file = open('log.txt', 'a')
log_file.write(log_text)
log_file.close()

# print(xml_documents)
file = open(os.path.join('xml_files/', batch_id), 'w')
file.write(xml_documents)
file.close()

links_df.to_csv('links_pub.csv', index=False)
