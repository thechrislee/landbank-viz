"""
bar
"""

import pathlib
import gmplot
import os


class Plot:
    """foo"""

    def __init__(self, center: tuple[float, float]) -> None:

        """"""
        # cleve_lat = 41.505493
        # cleve_long = -81.681290
        #self.center = center

    @property
    def api_key(self) -> str:
        """"""
        try:
            return self._api_key
        except AttributeError:
            pass
        try:
            self._api_key = os.environ["GOOGLE_MAP_API_KEY"]
        except KeyError:
            print("Unable to find, 'GOOGLE_MAP_API_KEY'")
            raise

        return self._api_key

    def plot_to_html(self, coordinates: list, filename: str) -> None:
        """plots the provided coordinates on a map and saves them to an html file"""

        gmap = gmplot.GoogleMapPlotter(self.latitude, self.longitude, 13, apikey=self.api_key, map_type="hybrid")

        for line in coordinates:
            address = line[0]
            lat = float(line[1].split(",")[1].replace('"', ""))
            long = float(line[1].split(",")[0].replace('"', ""))
            gmap.marker(lat, long, info_window=address)

        gmap.draw(filename)

class PlotCleveland(Plot):
    """
    """
    latitude = 41.505493
    longitude = -81.681290

    def __init__(self) -> None:
        super().__init__((self.latitude, self.longitude))
