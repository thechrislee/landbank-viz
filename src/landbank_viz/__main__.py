""""""
import typer
from .scrape import Scrape
from .plot import PlotCleveland

cli = typer.Typer()


@cli.command()
def scrape_anything(url: str):
    """"""
    scraper = Scrape(url)
    geocodes = scraper.setup()
    plotter = PlotCleveland()
    plotter.plot_to_html(geocodes, "cleveland_map.html")


if __name__ == "__main__":
    exit(cli())
