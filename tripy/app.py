from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.scrollview import ScrollView
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from tripy.article.article import SENTIMENT
from tripy.article.graph import graph
from tripy.algorithms.nn import NearestNeighbourSolver
from tripy.algorithms.tsp import DpTspSolver
import tripy.geo.distance as distance
from tripy.geo.locations import NAME_BY_INDEX, INDEX_BY_NAME
from tripy.widgets.mapview import MapView


class TripyApp(App):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        # self.btn = Button(text='Plot Line', size_hint_x=None, width=100)
        # self.input = TextInput(multiline=False, font_size=18)
        self.map_view = MapView()
        self.start_button = Button(text="Starting Point", size_hint_y=None, height=40)
        self.scroll = ScrollView(size_hint=(None, 1), width=500)
        self.option_button = Button(text="Options", size_hint_y=None, height=40)
        self.graph_view = BoxLayout(orientation='vertical', size_hint_x=None, width=1000)
        self.graph_view.bind(minimum_width=self.graph_view.setter('width'))
        self.scroll.add_widget(self.graph_view)
        self.scroll.do_scroll_x=True
        self.scroll.do_scroll_y=False
        self.button = BoxLayout(orientation='vertical')
        # self.btnMY = Button(text='Malaysia', size_hint_x=None, width=100)
        # self.btnCN = Button(text='Beijing', size_hint_x=None, width=100, on_press=self._country_on_click)
        # self.btnHK = Button(text='Hong Kong', size_hint_x=None, width=100, on_press=self._country_on_click)
        # self.btnID = Button(text='Jakarta', size_hint_x=None, width=100, on_press=self._country_on_click)
        # self.btnJP = Button(text='Tokyo', size_hint_x=None, width=100, on_press=self._country_on_click)
        # self.btnKR = Button(text='Seoul', size_hint_x=None, width=100, on_press=self._country_on_click)
        # self.btnTH = Button(text='Bangkok', size_hint_x=None, width=100, on_press=self._country_on_click)
        # self.btnTW = Button(text='Taipei', size_hint_x=None, width=100, on_press=self._country_on_click)

    def build(self) -> Widget:
        root = BoxLayout(orientation='horizontal')
        left_top = GridLayout(cols=1, rows=3, padding=5, spacing=2.5, size_hint_x=None, width=500, height=200)
        left_bot = GridLayout(cols=1, rows=3, padding=5,spacing=2.5, size_hint_x=None, width=500, height=800)
        left = GridLayout(cols=1, rows=2, padding=5,spacing=2.5, size_hint_x=None, width=500)

        # input_row = GridLayout(cols=2, padding=5, spacing=2.5, size_hint_y=None, height=50)
        # input_row.add_widget(self.input)
        # input_row.add_widget(self.btn)

        # root.add_widget(input_row)
        # root.add_widget(self.map_view)

        dropdown1 = DropDown()
        for key in NAME_BY_INDEX:
            btn = Button(text=NAME_BY_INDEX[key], size_hint_y=None, height=40)
            btn.bind(on_release=lambda btn: dropdown1.select(btn.text)) 
            dropdown1.add_widget(btn)

        self.start_button.bind(on_release=dropdown1.open)
        dropdown1.bind(on_select=lambda instance, x: setattr(self.start_button, 'text', x)) 

        dropdown2 = DropDown()
        btn = Button(text="Least Distance travelled", size_hint_y=None, height=40)
        btn.bind(on_release=lambda btn: dropdown2.select(btn.text)) 
        dropdown2.add_widget(btn)
        btn = Button(text="Better Investment", size_hint_y=None, height=40)
        btn.bind(on_release=lambda btn: dropdown2.select(btn.text)) 
        dropdown2.add_widget(btn)
        
        self.option_button.bind(on_release=dropdown2.open)
        dropdown2.bind(on_select=lambda instance, x: setattr(self.option_button, 'text', x))

        route_button = Button(text="Find Route", size_hint_y=None, height=40, on_press=self._on_click)
        left_top.add_widget(self.start_button)
        left_top.add_widget(self.option_button)
        left_top.add_widget(route_button)

        dropdown3 = DropDown()
        for key in NAME_BY_INDEX:
            btn = Button(text=NAME_BY_INDEX[key], size_hint_y=None, height=40, on_press=self._country_on_click)
            btn.bind(on_release=lambda btn: dropdown3.select(btn.text)) 
            dropdown3.add_widget(btn)
        country_button = Button(text="Country", size_hint_y=None, height=40, size_hint_x=None, width=500)
        country_button.bind(on_release=dropdown3.open)
        dropdown3.bind(on_select=lambda instance, x: setattr(country_button, 'text', x)) 

        left_bot.add_widget(country_button)
        left_bot.add_widget(self.scroll)

        left.add_widget(left_top)
        left.add_widget(left_bot)

        root.add_widget(left)
        root.add_widget(self.map_view)

        # country_button = GridLayout(cols=4, padding=5, spacing=2.5, size_hint_y=None, height=50)
        # country_button.add_widget(self.btnCN)
        # country_button.add_widget(self.btnHK)
        # country_button.add_widget(self.btnID)
        # country_button.add_widget(self.btnJP)
        # country_button1 = GridLayout(cols=3, padding=5, spacing=2.5, size_hint_y=None, height=50)
        # country_button1.add_widget(self.btnKR)
        # country_button1.add_widget(self.btnTH)
        # country_button1.add_widget(self.btnTW)
        # self.button.add_widget(country_button)
        # self.button.add_widget(country_button1)
        # self.graph_view.add_widget(self.button)
        # root.add_widget(self.graph_view)
        
        # self.btn.bind(on_press=self._on_click)

        return root

    def _on_click(self, instance) -> None:
        path = ""
        if self.option_button.text == "Least Distance travelled":
            m = distance.adjacency_matrix()
            solver = DpTspSolver(m, start=INDEX_BY_NAME[self.start_button.text])
            route = solver.best_route()
            for i in route:
                path += NAME_BY_INDEX[i] + ","

        elif self.option_button.text == "Better Investment":
            m = distance.adjacency_matrix()
            scores = SENTIMENT
            solver = NearestNeighbourSolver(m, scores, start=INDEX_BY_NAME[self.start_button.text])
            route = solver.best_route()
            for i in route:
                path += NAME_BY_INDEX[i] + ","


        print(path)
        self.map_view.set_path(path)

    def _country_on_click(self, instance):
        graph1= graph(instance.text)
        self.graph_view.clear_widgets()
        graph_canvas = FigureCanvasKivyAgg(graph1.plot_all_graph(0.35))
        self.graph_view.add_widget(graph_canvas)



if __name__ == '__main__':
    app = TripyApp()
    app.run()
