"""
"""

import json

from dataclasses import dataclass
from functools import lru_cache


import requests

from loguru import logger


class NoMatchForAddress(Exception):
    pass


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
        response = requests.get(cls._url)
        response.raise_for_status()
        result = json.loads(response.content)
        try:
            benchmark_data = result["benchmarks"]
        except KeyError:
            raise ValueError(f"malformed response {result}") from None

        return [cls(**data) for data in benchmark_data]

    @classmethod
    def default(cls) -> "Benchmark":
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
    def coordinates_for_address(
        cls, address: str, benchmark: Benchmark = None, format: str = "json"
    ) -> tuple[float, float]:
        """Match the address to a known latitude/longitude."""

        benchmark = benchmark or Benchmark.default()

        params = {"address": address, "benchmark": benchmark.name, "format": format}

        logger.info(f"geocoding {address} @ {cls._address_url} {params}")

        response = requests.get(cls._address_url, params=params)

        response.raise_for_status()

        result = json.loads(response.content)

        try:
            return tuple(result["result"]["addressMatches"][0]["coordinates"].values())
        except KeyError as error:
            logger.error(f"{address} {error} {result}")
            raise ValueError(f"{address} response data {error} {result}") from None
        except IndexError as error:
            logger.error(f"{address} {error} {result}")
            raise NoMatchForAddress(address) from None

    @classmethod
    def coordinates_for_addresses(
        cls,
        addresses: list[str],
        benchmark: Benchmark = None,
        format: str = "json",
    ) -> list[tuple[float, float]]:

        """Match the addresses to a known latitudes/longitudes."""

        benchmark = benchmark or Benchmark.default()

        params = {"benchmark": benchmark.name, "format": format}

        bulk = []
        for uid, address in enumerate(addresses):
            try:
                zipcode, state, city, *street = reverse(
                    address.replace(", ", "").split()
                )
            except Exception as error:
                logger.debug(f"unable to decode address {address} {error}")
                continue

        # EJO params gets updated here with zipcode, state, city, street

        response = requests.get(cls._bulk_url, params=params)

        response.raise_for_status()

        result = json.loads(response.content)

        print(result)
