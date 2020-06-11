import sys
from urllib.parse import urljoin, urlparse, urlunparse

import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *



class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Map Tool")
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.create_how_to_use())
        self.layout().addWidget(self.create_textbox())
        self.layout().addWidget(self.create_button())

        self.df = pd.read_csv('map.csv')
        self.dom = BeautifulSoup("", 'html.parser')
        self.links = []


    def create_how_to_use(self):
        label = QLabel()
        label.setText(
            """
            How to use:
            \t1. copy paste html source of a document
            \t2. click "Map"
            \t3. when dialog pops up, check if the mapping is done correctly
            \t\t(it mostly auto generates the correct address)
            \t4. click "Update"
            \t5. copy the updated html in the input box and paste it to kb site
            """
        )
        return label


    def create_textbox(self):
        self.text_box = QTextEdit("copy HTML doc here...")
        return self.text_box

    def create_button(self):
        def run_change_dialog(parent):
            self.dom = BeautifulSoup(self.text_box.toPlainText(), 'html.parser')
            self.links = self.dom.find_all('a', href=True)
            dialog = ChangeDialog(parent)
            dialog.exec()
        button = QPushButton("Map")
        button.clicked.connect(lambda: run_change_dialog(self))
        return button


class ChangeDialog(QDialog):
    def __init__(self, parent):
        super().__init__()
        self.parent: MainWidget = parent

        self.setWindowTitle('Links')
        self.setMaximumHeight(800)
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(QLabel("Links within the document\n\tCheck links and make changes accordingly"))
        self.add_link_widgets()
        self.layout().addWidget(self.create_button())

    def add_link_widgets(self):
        scroll_area = QScrollArea()
        scroll_area_widget = QWidget()
        scroll_area_widget.setLayout(QVBoxLayout())
        scroll_area.setWidget(scroll_area_widget)
        scroll_area.setWidgetResizable(True)

        self.line_edit_arr = []
        self.link_arr = []

        links = self.parent.links
        for link in links:
            scroll_area_widget.layout().addWidget(QLabel(link['href'] + "   ->"))
            line_edit = QLineEdit(self._map_to_kb_link(link['href']))
            self.line_edit_arr.append(line_edit)
            self.link_arr.append(link)
            scroll_area_widget.layout().addWidget(line_edit)
        self.layout().addWidget(scroll_area)

    def _map_to_kb_link(self, link: str):
        kb_path = 'https://kb.wisc.edu/sscc/'
        _, netloc, path, param, query, fragment = urlparse(link)

        # address in ssc network
        if netloc == 'www.ssc.wisc.edu' or netloc == 'ssc.wisc.edu':
            target = self.parent.df[self.parent.df['Current URL'].str.contains(path)]
            if not pd.isna(target.iloc[0, 3]):
                doc_id = str(target.iloc[0, 3])
                kb_path = 'sscc/' + doc_id
                kb_link = urlunparse(('https://', 'kb.wisc.edu', kb_path, param, query, fragment))
                # kb_link = urljoin(kb_path, doc_id)
            else:
                # kb_link = 'n/a'
                kb_link = link
        else:
            kb_link = link
        return kb_link

    def create_button(self):
        def update_links(arr):
            for i, link in enumerate(self.parent.links):
                link['href'] = self.line_edit_arr[i].text()
            self.parent.text_box.setText(self.parent.dom.prettify())
            self.close()
            print(self.parent.links)

        button = QPushButton('Update')
        button.clicked.connect(lambda: update_links(self.line_edit_arr))
        return button





# MAP_CSV_PATH = ""

# map_df = pd.read_csv(MAP_CSV_PATH)


def find_links(doc: str):
    """
    This function extracts links within the HTML formatted document given as a argument.
    :param doc: HTML format string
    :return: returns list of links within the document
    """
    dom = BeautifulSoup(doc, 'html.parser')
    hrefs = dom.find_all(href=True)

    # change links, their contents and so on
    print(hrefs[0])
    print(hrefs[0].contents)
    print(hrefs[0]['href'])



app = QApplication(sys.argv)
main_window = MainWidget()
main_window.show()

app.exec_()

