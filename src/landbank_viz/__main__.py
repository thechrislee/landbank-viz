""""""
import typer

from loguru import logger

from .geocode import CensusGeocode
from .parcel import Parcel

cli = typer.Typer()


@cli.command()
def scrape_anything(url: str = None):
    """"""

    url = url or "https://cuyahogalandbank.org/all-available-properties/"

    parcels = [parcel for parcel in Parcel.inventory(url) if parcel.is_available]

    geocoder = CensusGeocode()

    results = geocoder.lookup_addresses([p.address for p in parcels])

    for entry in results:
        if not entry.is_match:
            logger.info(f"Not a match: {entry}")
            continue
        logger.info(f"Match {entry.parsed} {entry.coordinates}")


if __name__ == "__main__":
    exit(cli())
