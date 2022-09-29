"""
bar
"""

from bs4 import BeautifulSoup
import requests
import pathlib
import re
import csv
import gmplot
from .plot import Plot


class Scrape:
    """foo"""

    def __init__(self, url: str) -> None:
        """"""
        self._url = url

    @property
    def url(self) -> str:
        return getattr(
            self, "_url", "https://cuyahogalandbank.org/all-available-properties/"
        )

    @url.setter
    def url(self, new_url: str) -> None:
        self._url = new_url

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
                status = data[6] if data[6] != "" else "NaN"

                address = f"{house_num} {street}"

                if "NaN" not in address and "Not Available" not in status:
                    address = pattern.sub("", address).strip()
                    addresses.append((address, city))
        return addresses

    def get_geocodes(self, addresses: list) -> list:
        """takes a list of addresses and returns the corresponding geocodes"""
        url = "https://geocoding.geo.census.gov/geocoder/locations/addressbatch"
        csv_file = "addresses.csv"
        with open(csv_file, "w") as csvfile:
            csv_writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
            for key, address in enumerate(addresses):
                csv_writer.writerow([key] + [address[0]] + [address[1]] + ["OH"] + [""])

        with open(csv_file, "rb") as payload:
            files = {"addressFile": payload, "benchmark": (None, "4")}

            geocodes = []
            pattern = re.compile(r"\B,\B")
            response = requests.post(url, files=files)
            for line in response.text.splitlines():
                result = pattern.split(line)
                if len(result) == 8:
                    address = result[4]
                    geocode = result[5]
                    geocodes.append((address, geocode))

            return geocodes

    def doit(self) -> list:
        """it does it"""
        html = self.get_html()
        self.bs = BeautifulSoup(html, "html.parser")
        addresses = self.get_addresses()
        geocodes = self.get_geocodes(addresses)
        return geocodes
