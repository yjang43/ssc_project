from bs4 import BeautifulSoup
import pandas as pd
import requests

def set_xml_document(kb_title='.', kb_keywords='.',
                     kb_summary='.', kb_body='.',
                     kb_int_notes='.', img_base_url = '.'):
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
    xml_document = xml_document + '<kb_int_notes>' + kb_int_notes + '</kb_int_notes>\n'
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


#
#
# inputs here, batch length, batch id
#
links_from = int(input("from what index to start: "))
links_num = int(input("how many links to batch: "))
batch_id = input("batch id: ")
log_text = ''

for i in range(links_from, links_from + links_num):
    req = requests.get(links[i])
    dom = BeautifulSoup(req.text, 'html.parser')
    kb_body = dom.select('#RightContent')[0]
    # this kb_body will still contain tag for html <body></body>
    # let me know if this needs to be deleted
    kb_title = titles[i]
    if kb_title:
        log_text += str(i) + ': ' + links[i] + '\tsuccess\r'
    else:
        log_text += 'ERROR - ' + str(i) + ': ' + links[i] + '\tfail\r'

    xml_document = set_xml_document(kb_title=kb_title, kb_body=kb_body)
    xml_documents = xml_documents + xml_document

    # record batch id for the link
    links_df['Batch'][i] = batch_id


# end xml_documents
xml_documents = xml_documents + '</kb_documents>'

log_file = open('log.txt', 'a')
log_file.write(log_text)
log_file.close()

print(xml_documents)
file = open(batch_id, 'w')
file.write(xml_documents)
file.close()


links_df.to_csv('links_pub.csv')
