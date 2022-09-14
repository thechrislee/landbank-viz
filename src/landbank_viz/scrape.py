"""
bar
"""

from bs4 import BeautifulSoup
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

    def parse_html(self):
        """parse the html file"""
        rows = self.bs.find_all("tr")
        for row in rows:
            data = []
            cols = row.find_all("td")
            for col in cols:
                data.append(col.text.strip())
            print(len(data))
            print(data)
            print("-----------------------")
            #print(f"address: {address}")
        

    def doit(self):
        """it does it"""
        #response = requests.get(self.url)
        self.get_html()
        with open("html_file") as file:
            html_file = "".join([line for line in file])

        #print(html_file)
        self.bs = BeautifulSoup(html_file, "html.parser")
        self.parse_html()
