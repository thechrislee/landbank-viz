""""""
import typer

from loguru import logger

from .parcel import Parcel

cli = typer.Typer()


@cli.command()
def scrape_anything(url: str = None):
    """"""

    url = url or "https://cuyahogalandbank.org/all-available-properties/"

    parcels = Parcel.available(url)

    for parcel in parcels:
        print(parcel)


if __name__ == "__main__":
    exit(cli())
