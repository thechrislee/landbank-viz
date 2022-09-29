"""
bar
"""

import pathlib
import gmplot
import os


class Plot:
    """foo"""

    def __init__(self, coordinates: list) -> None:

        """"""
        try:
            API_KEY = os.environ["GOOGLE_MAP_API_KEY"]
        except KeyError:
            print(
                "Unable to locate API key in expected environment variable 'GOOGLE_MAP_API_KEY'"
            )

        # cleve_lat = 41.505493
        # cleve_long = -81.681290
        self.coordinates = coordinates

    def create_map(self) -> None:
        """plots the provided coordinates on a map and saves them to an html file"""

        # gmap = gmplot.GoogleMapPlotter(cleve_lat, cleve_long, 13, apikey=self.API_KEY, map_type="hybrid")
        gmap = gmplot.GoogleMapPlotter(
            41.505493, -81.681290, 13, apikey="", map_type="hybrid"
        )

        for line in self.coordinates:
            address = line[0]
            lat = float(line[1].split(",")[1].replace('"', ""))
            long = float(line[1].split(",")[0].replace('"', ""))
            gmap.marker(lat, long, info_window=address)

        gmap.draw("cleveland.html")
