"""
bar
"""

import bs4
import requests

class Scrape:
    """ foo """
    def __init__(self, url:str) -> None:
        """"""
        self.url = url

    def doit(self):
        """it does it"""
        response = requests.get(self.url)
        self.bs = bs4.BeautifulSoup(response.content)
