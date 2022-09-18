"""
"""

import csv

from dataclasses import dataclass
from functools import lru_cache
from io import StringIO
from typing import Any

import requests

from loguru import logger


@dataclass
class BulkGeocodeResponse:
    id: str
    address: str
    match: str
    matchtype: str
    parsed: str
    latlong: str
    tigerlineid: str
    side: str

    @classmethod
    def fields(cls) -> list[str]:
        return list(cls.__dataclass_fields__.keys())

    @property
    def is_match(self) -> bool:
        return self.match.lower() == "match"

    @property
    def is_exact(self) -> bool:
        return self.matchtype.lower() == "exact"

    @property
    def coordinates(self) -> tuple[float, float]:
        try:
            return self._coordinates
        except AttributeError:
            pass
        self._coordinates = tuple(map(float, self.latlong.split(",")))
        return self._coordinates

    @property
    def latitude(self) -> float:
        return self.coordinates[0]

    @property
    def longitude(self) -> float:
        return self.coordinates[1]


@dataclass
class Benchmark:
    """A US Census Geocoder Benchmark"""

    id: str
    benchmarkName: str
    benchmarkDescription: str
    isDefault: bool
    _url: str = "https://geocoding.geo.census.gov/geocoder/benchmarks"

    @classmethod
    @lru_cache
    def benchmarks(cls) -> list["Benchmark"]:
        """Returns a list of Benchmark instances initialized with online data."""
        response = requests.get(cls._url)
        response.raise_for_status()
        result = response.json()
        try:
            benchmark_data = result["benchmarks"]
        except KeyError:
            raise ValueError(f"malformed response {result}") from None

        return [cls(**data) for data in benchmark_data]

    @classmethod
    def default(cls) -> "Benchmark":
        """Returns the current default Benchmark."""
        for benchmark in cls.benchmarks():
            if benchmark.isDefault:
                return benchmark
        raise ValueError("No default benchmark found")

    @property
    def name(self) -> str:
        return self.benchmarkName


class CensusGeocode:

    """US Census Geocode Service"""

    _bulk_url: str = "https://geocoding.geo.census.gov/geocoder/locations/addressbatch"
    _address_url: str = (
        "https://geocoding.geo.census.gov/geocoder/locations/onelineaddress"
    )

    @classmethod
    def lookup_address(
        cls, address: str, benchmark: Benchmark = None
    ) -> dict[str, Any]:
        """Lookup entry for the given address."""

        benchmark = benchmark or Benchmark.default()

        params = {"address": address, "benchmark": benchmark.name, "format": "json"}

        logger.info(f"geocoding {address} @ {cls._address_url} {params}")

        response = requests.get(cls._address_url, params=params)

        response.raise_for_status()

        return response.json()

    @classmethod
    def lookup_addresses(
        cls,
        addresses: list[str],
        benchmark: Benchmark = None,
        format: str = "json",
    ) -> list[dict[str, str]]:

        """Perform a bulk lookup for the addresses given."""

        addresses_csv = StringIO(
            "\n".join([f"{uid},{address},," for uid, address in enumerate(addresses)])
        )

        # EJO the .csv suffix attached to the filename is required by
        #     the API to determine the input file type, rather than
        #     using the given MIME type.  Including the MIME type in
        #     case they decide to use it in the future.

        files = {
            "addressFile": ("addresses.csv", addresses_csv, "text/csv"),
        }

        benchmark = benchmark or Benchmark.default()

        data = {
            "benchmark": benchmark.name,
        }

        response = requests.post(cls._bulk_url, data=data, files=files)

        try:
            response.raise_for_status()
        except Exception as error:
            logger.debug("writing response to 'response.html'")
            open("response.html", "w").write(response.text)
            logger.debug("writing addresses to 'addresses.csv'")
            open("addressess.csv", "w").write(addresses_csv.getvalue())
            raise

        rdr = csv.DictReader(
            StringIO(response.text),
            fieldnames=BulkGeocodeResponse.fields(),
        )

        return [BulkGeocodeResponse(**row) for row in rdr]
