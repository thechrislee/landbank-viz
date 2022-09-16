"""
bar
"""

from bs4 import BeautifulSoup
import requests
import pathlib
import re
import csv


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

        pattern = re.compile(
            r"""
            \(.+?\)                                # Match parentheses
            |                                      # logical OR
            (\bAve\b|\bRd\b|\bSt\b|\bLn\b|\bCt\b)  # Match abbreviations
            """,
            re.VERBOSE,
        )

        rows = self.bs.find_all("tr")
        addresses = []
        for row in rows:
            cols = row.find_all("td")
            data = [col.text.strip() for col in cols]
            if len(data) == 7:
                house_num = data[1] if data[1] != "" else "NaN"
                street = data[2] if data[2] != "" else "NaN"
                city = data[3] if data[3] != "" else "NaN"

                address = f"{house_num} {street}"

                if "NaN" not in address:
                    address = pattern.sub("", address).strip()
                    addresses.append((address, city))
        return addresses

    def get_geocodes(self, addresses: list) -> list:
        """takes a list of addresses and returns the corresponding geocodes"""
        csvfile = "addresses.csv"
        with open(csvfile, "w") as csvfile:
            csv_writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
            for key, address in enumerate(addresses):
                csv_writer.writerow([key] + [address[0]] + [address[1]] + ["OH"] + [""])

    def doit(self):
        """it does it"""
        html = self.get_html()
        self.bs = BeautifulSoup(html, "html.parser")
        addresses = self.get_addresses()
        self.get_geocodes(addresses)
