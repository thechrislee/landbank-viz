"""Landbank Parcel Descriptions
"""

from dataclasses import dataclass

from loguru import logger


from .scrape import AvailableScraper


@dataclass
class Parcel:
    parcel_id: str
    number: str
    street: str
    city: str
    ward: str
    date: str
    status: str

    @classmethod
    def inventory(cls, url: str) -> list["Parcel"]:
        return [cls(**info) for info in AvailableScraper(url).parcels]

    def __str__(self) -> str:
        return f"{self.parcel_id} {self.address}"

    @property
    def is_available(self) -> bool:
        return "not available" not in self.status.lower()

    @property
    def address(self) -> str:
        """The street address for this parcel."""

        return f"{self.number} {self.street}, {self.city}"
