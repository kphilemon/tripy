from kivy.uix.boxlayout import BoxLayout
from .cefbrowser import CEFBrowser


class MapView(BoxLayout):
    # Markers are plotted on the eight cities: Kuala Lumpur, Jakarta, Bangkok, Taipei, Hong Kong, Tokyo, Beijing,  Seoul
    _BASE_URL = r'file:///assets/map.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.browser = CEFBrowser(url=MapView._BASE_URL)
        self.add_widget(self.browser)

    # plot polyline on the map in ascending order based on the list of location names
    # valid location names are the eight cities mentioned above
    # case and space sensitive, invalid location names will be ignored and skip to the next valid location name
    # to plot a path from Jakarta to Bangkok to Tokyo, simply pass in ['Jakarta', 'Bangkok', 'Tokyo']
    def set_path(self, locations):
        url = MapView._BASE_URL + '?path=' + ','.join(locations)
        print('Setting path:', url)
        self.browser.navigate(url)
