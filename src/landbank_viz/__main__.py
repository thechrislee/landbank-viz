""""""
import typer
from .scrape import Scrape

cli = typer.Typer()


@cli.command()
def scrape_anything(url: str):
    """"""
    scraper = Scrape(url)
    scraper.doit()
    # print(scraper.bs)


if __name__ == "__main__":
    exit(cli())
