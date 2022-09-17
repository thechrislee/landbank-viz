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
        return [
            cls(**info)
            for info in AvailableScraper(url).parcels
            if not "not available" in info["status"].lower()
        ]

    @property
    def oneline_address(self) -> str:
        try:
            return self._address
        except AttributeError:
            pass

        # self._address = ParcelIdScraper(self.parcel_id).address
        self._address = " ".join([self.unit, self.street, self.city, "OH"])

        return self._address

    @property
    def address(self) -> dict:
        try:
            return self._address
        except AttributeError:
            pass

        self._address: dict[str, str] = {
            "id": self.parcel_id,
            "street": f"{self.unit} {self.street}",
            "city": self.city,
            "state": "OH",
            "zip": "",
        }

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
            ] = CensusGeocode.coordinates_for_address(self.oneline_address)
        except Exception as error:
            logger.error(f"{self.address} {error}")
            self._coordinates = "Not Available"
        return self._coordinates

    def __str__(self) -> str:

        return f"{self.parcel_id} {self.oneline_address} {self.coordinates}"