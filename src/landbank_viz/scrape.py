"""
bar
"""

from bs4 import BeautifulSoup
import requests
import pathlib
import re


class Scrape:
    """foo"""

    def __init__(self, url: str) -> None:
        """"""
        self.url = url

    def get_html(self) -> str:
        """write html file locally"""
        html_file = pathlib.Path("html_file")

        if html_file.exists():
            return html_file.read_text()

        print("---Writing html file locally----")
        response = requests.get(self.url)
        html_file.write_text(response.text)
        return response.text

    def get_addresses(self) -> list:
        """parse the html file and return a list of addresses"""
        pattern = re.compile(r"\(.+?\)")
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
                if "NaN" not in address:
                    addresses.append(pattern.sub("", address))
        return addresses

    def doit(self):
        """it does it"""
        html = self.get_html()
        self.bs = BeautifulSoup(html, "html.parser")
        addresses = self.get_addresses()
        for address in addresses:
            print(address)
