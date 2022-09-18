""""""
import typer

from loguru import logger

from .geocode import CensusGeocode
from .parcel import Parcel

cli = typer.Typer()


@cli.command()
def scrape_anything(
    url: str = typer.Argument(
        "https://cuyahogalandbank.org/all-available-properties/", show_default=True
    ),
    debug: bool = typer.Option(False, "--debug", "-D", help="Turn on debugging output"),
):
    """Queries the Cuyahoga Land Bank for available properties and prints a
    list of property addresses and corresponding latitude/longitude coordinates.
    """

    (logger.enable if debug else logger.disable)("landbank_viz")

    parcels = [parcel for parcel in Parcel.inventory(url) if parcel.is_available]

    results = CensusGeocode.lookup_addresses([p.address for p in parcels])

    for entry in results:
        if not entry.is_match:
            logger.info(f"Not a match: {entry}")
            continue
        print(entry.parsed, entry.coordinates)


if __name__ == "__main__":
    exit(cli())
