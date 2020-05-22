from kivy.uix.boxlayout import BoxLayout
from .cefbrowser import CEFBrowser


class MapView(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(CEFBrowser(url='https://www.google.com.my/maps'))
