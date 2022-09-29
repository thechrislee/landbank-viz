""""""
import typer
from .scrape import Scrape
from .plot import Plot

cli = typer.Typer()


@cli.command()
def scrape_anything(url: str):
    """"""
    scraper = Scrape(url)
    geocodes = scraper.doit()
    # print(scraper.bs)
    plot = Plot(geocodes)
    plot.create_map()


if __name__ == "__main__":
    exit(cli())
