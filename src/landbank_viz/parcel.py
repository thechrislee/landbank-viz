"""Landbank Parcel Descriptions
"""

from dataclasses import dataclass

from loguru import logger

from .geocode import CensusGeocode
from .scrape import AvailableScraper, ParcelIdScraper


@dataclass
class Parcel:
    parcel_id: str
    unit: str
    street: str
    city: str
    ward: str
    date: str
    status: str

    @classmethod
    def available(cls, url: str) -> list["Parcel"]:
        return [cls(**info) for info in AvailableScraper(url).parcels]

    @property
    def address(self) -> str:
        try:
            return self._address
        except AttributeError:
            pass

        self._address = ParcelIdScraper(self.parcel_id).address

        return self._address

    @property
    def coordinates(self) -> tuple[float, float]:
        try:
            return self._coordinates
        except AttributeError:
            pass
        try:
            self._coordinates: tuple[
                float, float
            ] = CensusGeocode.coordinates_for_address(self.address)
        except Exception as error:
            logger.error(f"{self.address} {error}")
            self._coordinates = "Not Available"
        return self._coordinates
