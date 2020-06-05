import os

from kivy.uix.boxlayout import BoxLayout
from tripy.widgets.cefbrowser import CEFBrowser


# Markers are plotted on the eight cities: Kuala Lumpur, Jakarta, Bangkok, Taipei, Hong Kong, Tokyo, Beijing,  Seoul
class MapView(BoxLayout):

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        if os.getcwd().endswith(r'\tripy\tripy'):
            self.base_url = r'file:///assets/map.html'
        else:
            self.base_url = r'file:///tripy/assets/map.html'

        self.browser = CEFBrowser(url=self.base_url)
        self.add_widget(self.browser)

    # plot polyline on the map in ascending order based on the list of location names
    # valid location names are the eight cities mentioned above (case and space insensitive)
    # invalid location names will be ignored and skip to the next valid location name
    # to plot a path from Jakarta to Bangkok to Tokyo, simply pass in a string 'Jakarta, Bangkok, Tokyo'
    def set_path(self, path: str) -> None:
        url = f'{self.base_url}?path={path}'
        print('Setting path:', url)
        self.browser.navigate(url)
