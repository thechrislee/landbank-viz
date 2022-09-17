"""
bar
"""

from datetime import date, datetime
from urllib3.util import parse_url

from bs4 import BeautifulSoup
from loguru import logger

import pathlib
import requests


class BaseScraper:
    """foo"""

    _cache_dir = "/tmp"

    def __init__(self, url: str) -> None:
        """"""
        self.url = url

    def __str__(self) -> str:

        return f"{self.__class__.__name__} -> {self.url}"

    @property
    def cache_name(self) -> str:
        try:
            return self._cache_name
        except AttributeError:
            pass

        filename = pathlib.Path(parse_url(self.url).path).name
        today = date.today()
        timestamp = int(datetime(today.year, today.month, today.day).timestamp())
        self._cache_name = f"{self._cache_dir}/{filename}-{timestamp}.html"
        return self._cache_name

    @property
    def html(self) -> str:
        """The HTML content retrieved from this instance's URL."""
        try:
            return self._html
        except AttributeError:
            pass

        cached_html = pathlib.Path(self.cache_name)

        if cached_html.exists():
            self._html = cached_html.read_text()
            return self._html

        response = requests.get(self.url)
        cached_html.write_text(response.text)
        self._html = response.text
        return self._html

    @property
    def beautiful_soup(self) -> BeautifulSoup:
        """A BeautifulSoup html.parser instance configured with the html for this url."""
        try:
            return self._beautiful_soup
        except AttributeError:
            pass
        self._beautiful_soup = BeautifulSoup(self.html, "html.parser")
        return self._beautiful_soup


class AvailableScraper(BaseScraper):
    _base_url = "https://cuyahogalandbank.org/all-available-properties/"

    def __init__(self, url: str = None) -> None:
        url = url or self._base_url
        super().__init__(url)

    @property
    def parcels(self) -> list[dict[str, str]]:
        """List of parcels parsed from the contents of the url."""
        try:
            return self._parcels
        except AttributeError:
            pass

        rows = self.beautiful_soup.find_all("tr")
        self._parcels = []
        for row in rows:
            cols = [col.text.strip() for col in row.find_all("td")]
            try:
                pid, unit, street, city, ward, date, status = cols
            except ValueError as error:
                logger.debug(f"{error} Unable decode scraped data {cols}")
                continue

            item = {
                "parcel_id": pid,
                "unit": unit,
                "street": street,
                "city": city,
                "ward": ward,
                "date": date,
                "status": status,
            }
            self._parcels.append(item)

        return self._parcels


class ParcelIdScraper(BaseScraper):

    _query_url = "https://cuyahogalandbank.org/property-detail/?parcel_id="

    def __init__(self, parcel_id: str, query_url: str = None) -> None:
        query_url = query_url or self._query_url
        self.parcel_id = parcel_id
        super().__init__(query_url + parcel_id)

    @property
    def cache_name(self) -> str:
        try:
            return self._cache_name
        except AttributeError:
            pass

        filename = pathlib.Path(parse_url(self.url).path).name
        today = date.today()
        timestamp = int(datetime(today.year, today.month, today.day).timestamp())
        self._cache_name = (
            f"{self._cache_dir}/{filename}-{self.parcel_id}-{timestamp}.html"
        )
        return self._cache_name

    @property
    def address(self) -> str:
        try:
            return self._address
        except AttributeError:
            pass

        div = self.beautiful_soup.find("div", {"class": "parcel-detail-header"})

        if div:
            tt = str.maketrans({"\t": " ", "\n": " ", ",": " "})
            self._address = div.findChild().string.strip().translate(tt)
        else:
            self._address = "Unknown"

        return self._address

    @property
    def details(self) -> dict:
        try:
            return self._details
        except AttributeError:
            pass

        try:
            self._details = {"address": self.address}
        except ValueError:
            return {}

        grid = self.beautiful_soup.find("div", {"class": "property-details grid"})

        if not grid:
            return {}

        labels = [
            l.string.strip()
            for l in grid.find_all("p", {"class": "parcel-detail-label"})
        ]

        values = [
            v.string.strip()
            for v in grid.find_all("p", {"class": "parcel-detail-value"})
        ]

        self._details.update({label: value for label, value in zip(labels, values)})

        return self._details
