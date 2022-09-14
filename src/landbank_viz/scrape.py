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
        addresses = []
        for row in rows:
            cols = row.find_all("td")
            data = [col.text.strip() for col in cols]
            if len(data) == 7:
                house_num = data[1] if data[1] != "" else "NaN"
                street = data[2] if data[2] != "" else "NaN"
                city = data[3] if data[3] != "" else "NaN"
                address = f"{house_num} {street} {city}"
                addresses.append(address)
          
        for address in addresses:
            print(address)
        
        

    def doit(self):
        """it does it"""
        #response = requests.get(self.url)
        self.get_html()
        with open("html_file") as file:
            html_file = "".join([line for line in file])

        #print(html_file)
        self.bs = BeautifulSoup(html_file, "html.parser")
        self.parse_html()
