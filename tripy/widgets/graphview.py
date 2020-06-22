import os
from kivy.uix.boxlayout import BoxLayout
from tripy.widgets.cefbrowser import CEFBrowser

class GraphView(BoxLayout):

    def __init__(self, url, **kwargs) -> None:
        super().__init__(**kwargs)
        self._base_url = "file://"+os.getcwd()
        if self._base_url.endswith(f'{os.sep}tripy{os.sep}tripy'):
            self._base_url += f'{os.sep}assets{os.sep}datas{os.sep}'
        else:
            self._base_url += f'{os.sep}tripy{os.sep}assets{os.sep}datas{os.sep}'

        self.browser = CEFBrowser()
        self.add_widget(self.browser)

    def show_graph(self, url: str):
    	url = f'{self._base_url}{url}'
    	self.browser.navigate(url)