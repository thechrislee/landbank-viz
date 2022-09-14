"""
bar
"""

import bs4
import requests
import os

class Scrape:
    """ foo """
    def __init__(self, url:str) -> None:
        """"""
        self.url = url

    def get_html(self):
        """write html file locally"""
        if not os.path.exists("html_file"):
            print("---Writing html file locally----")
            response = requests.get(self.url)
            data =  "".join([line for line in response.text])
            with open("html_file", "w") as file:
                for line in data:
                    file.write(line)
        else:
            print("----'html_doc' already exists----")


    def doit(self):
        """it does it"""
        #response = requests.get(self.url)
        self.get_html()
        #self.bs = bs4.BeautifulSoup(response.content)
