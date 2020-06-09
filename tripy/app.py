from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from tripy.article.graph import graph
from tripy.widgets.mapview import MapView


class TripyApp(App):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.btn = Button(text='Plot Line', size_hint_x=None, width=100)
        self.input = TextInput(multiline=False, font_size=18)
        self.map_view = MapView()

        self.graph_view = BoxLayout(orientation='horizontal')
        self.button = BoxLayout(orientation='vertical')
        self.btnMY = Button(text='Malaysia', size_hint_x=None, width=100)
        self.btnCN = Button(text='Beijing', size_hint_x=None, width=100, on_press=self._country_on_click)
        self.btnHK = Button(text='Hong Kong', size_hint_x=None, width=100, on_press=self._country_on_click)
        self.btnID = Button(text='Jakarta', size_hint_x=None, width=100, on_press=self._country_on_click)
        self.btnJP = Button(text='Tokyo', size_hint_x=None, width=100, on_press=self._country_on_click)
        self.btnKR = Button(text='Seoul', size_hint_x=None, width=100, on_press=self._country_on_click)
        self.btnTH = Button(text='Bangkok', size_hint_x=None, width=100, on_press=self._country_on_click)
        self.btnTW = Button(text='Taipei', size_hint_x=None, width=100, on_press=self._country_on_click)

    def build(self) -> Widget:
        root = BoxLayout(orientation='vertical')

        input_row = GridLayout(cols=2, padding=5, spacing=2.5, size_hint_y=None, height=50)
        input_row.add_widget(self.input)
        input_row.add_widget(self.btn)

        root.add_widget(input_row)
        root.add_widget(self.map_view)

        country_button = GridLayout(cols=4, padding=5, spacing=2.5, size_hint_y=None, height=50)
        country_button.add_widget(self.btnCN)
        country_button.add_widget(self.btnHK)
        country_button.add_widget(self.btnID)
        country_button.add_widget(self.btnJP)
        country_button1 = GridLayout(cols=4, padding=5, spacing=2.5, size_hint_y=None, height=50)
        country_button1.add_widget(self.btnKR)
        country_button1.add_widget(self.btnTH)
        country_button1.add_widget(self.btnTW)
        self.button.add_widget(country_button)
        self.button.add_widget(country_button1)
        self.graph_view.add_widget(self.button)
        root.add_widget(self.graph_view)
        
        self.btn.bind(on_press=self._on_click)

        return root

    def _on_click(self, instance) -> None:
        path = self.input.text
        print(path)
        self.map_view.set_path(path)

    def _country_on_click(self, instance):
        graph1= graph(instance.text)
        self.graph_view.clear_widgets()
        graph_canvas = FigureCanvasKivyAgg(graph1.plot_all_graph(0.35))
        self.graph_view.add_widget(self.button)
        self.graph_view.add_widget(graph_canvas)



if __name__ == '__main__':
    app = TripyApp()
    app.run()
