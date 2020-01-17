from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import pandas as pd

df = pd.read_csv('links_pub.csv')
links_size = df.index.size
links = df['Current URL'].tolist()
titles = df['Title'].tolist()

doc_numbers = []




driver = webdriver.Chrome()
driver.get('https://kb.wisc.edu/kbAdmin')
netID = input("id: ")
password = input("password: ")
netID_elem = driver.find_element_by_id('j_username')
password_elem = driver.find_element_by_id('j_password')
netID_elem.send_keys(netID)
password_elem.send_keys(password + Keys.ENTER)

try:
    wait = WebDriverWait(driver, 60).until(EC.title_is('Home: KB Admin Tools'), 'you took more than 60 seconds to log in')
finally:
    driver.quit
input("continue?")



documents_tab = driver.find_element_by_css_selector("a[class='tab Documents']")
documents_tab.click()

for x in range(0, 2):
# recursion starts here
    new_doc = driver.find_element_by_link_text('New Doc')
    new_doc.click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'title')))
    new_doc_title = driver.find_element_by_id('title')
    new_doc_title.send_keys(titles[x])
    new_doc_keywords = driver.find_element_by_id('keywords')
    new_doc_keywords.send_keys(".")
    new_doc_summary = driver.find_element_by_id('summary')
    new_doc_summary.send_keys(".")

    iframe = driver.find_element_by_tag_name('iframe')
    driver.switch_to.frame(iframe)
    iframe_body = driver.find_element_by_xpath('/html/body')
    iframe_body.send_keys('.')
    driver.switch_to.default_content()

    owner_group_admin = driver.find_element_by_id('write5')
    owner_group_admin.click()

    submit = driver.find_elements_by_name('draft[save]')
    submit[1].click()

# parse number from statement
    statement_elem = driver.find_element_by_class_name('edit-button-normal')
    statement = statement_elem.get_property('innerHTML')
    doc_number = [int(s) for s in statement.split() if s.isdigit()]
    doc_number = doc_number[0]

    doc_numbers.append(doc_number)

# append doc_numbers to df columns







