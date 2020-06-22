from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.scrollview import ScrollView
from kivy.config import Config
#from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from tripy.article.article import SENTIMENT
from tripy.article.graph import Graph, Probability_distribution, Sentiment_graph
from tripy.algorithms.nn import NearestNeighbourSolver, ModifiedNearestNeighbourSolver
from tripy.algorithms.tsp import DpTspSolver
import tripy.geo.distance as distance
from tripy.geo.locations import NAME_BY_INDEX, INDEX_BY_NAME
from tripy.widgets.mapview import MapView
from tripy.widgets.graphview import GraphView
from threading import Thread



class TripyApp(App):
    def __init__(self, **kwargs) -> None:
        Config.set('graphics','width', 1600)
        Config.set('graphics','height',900)
        Config.write()
        super().__init__(**kwargs)
        self.map_view = MapView()
        self.sentiment_view1 = GraphView("sentiment.html")
        self.probability_view1 = GraphView("sentiment.html")
        self.start_button = Button(text="Starting Point", size_hint_y=None, height=40)
        self.scroll = ScrollView(size_hint=(None, 1), width=500)
        self.option_button = Button(text="Options", size_hint_y=None, height=40)
        self.country_button = Button(text="Country", size_hint_y=None, height=40, size_hint_x=None, width=500)
        self.graph_view = BoxLayout(orientation='vertical', size_hint_x=None, width=1000)
        self.graph_view.bind(minimum_width=self.graph_view.setter('width'))
        self.graph_view.add_widget(self.sentiment_view1)
        self.scroll.add_widget(self.graph_view)
        self.scroll.do_scroll_x=True
        self.scroll.do_scroll_y=False
        self.scroll1 = ScrollView(size_hint=(None, 1), width=500)
        self.probability_view = BoxLayout(orientation='vertical', size_hint_x=None, width=800)
        self.probability_view.bind(minimum_width=self.probability_view.setter('width'))
        self.probability_view.add_widget(self.probability_view1)
        self.scroll1.add_widget(self.probability_view)
        self.scroll1.do_scroll_x=True
        self.scroll1.do_scroll_y=False


    def build(self) -> Widget:
        root = BoxLayout(orientation='horizontal')
        left_top = GridLayout(cols=1, rows=3, size_hint_x=None, width=500, size_hint_y=None, height=120)
        left_mid = GridLayout(cols=1, rows=3, size_hint_x=None, width=500)
        left_bot = GridLayout(cols=1, rows=3, size_hint_x=None, width=500)
        left = BoxLayout(orientation='vertical', size_hint_x=None, width=500)


        dropdown1 = DropDown()
        for key in NAME_BY_INDEX:
            btn = Button(text=NAME_BY_INDEX[key], size_hint_y=None, height=40, size_hint_x=None, width=500)
            btn.bind(on_release=lambda btn: dropdown1.select(btn.text)) 
            dropdown1.add_widget(btn)
        self.start_button.bind(on_release=dropdown1.open)
        dropdown1.bind(on_select=lambda instance, x: setattr(self.start_button, 'text', x)) 

        dropdown2 = DropDown()
        btn = Button(text="Least Distance travelled", size_hint_y=None, height=40, size_hint_x=None, width=500)
        btn.bind(on_release=lambda btn: dropdown2.select(btn.text)) 
        dropdown2.add_widget(btn)
        btn = Button(text="Better Investment", size_hint_y=None, height=40)
        btn.bind(on_release=lambda btn: dropdown2.select(btn.text)) 
        dropdown2.add_widget(btn)
        btn = Button(text="Optimum Route", size_hint_y=None, height=40)
        btn.bind(on_release=lambda btn: dropdown2.select(btn.text)) 
        dropdown2.add_widget(btn)
        
        self.option_button.bind(on_release=dropdown2.open)
        dropdown2.bind(on_select=lambda instance, x: setattr(self.option_button, 'text', x))

        route_button = Button(text="Find Route", size_hint_y=None, height=40, on_press=self._on_click)
        left_top.add_widget(self.start_button)
        left_top.add_widget(self.option_button)
        left_top.add_widget(route_button)

        dropdown3 = DropDown()
        btn = Button(text="Sentiment Score", size_hint_y=None, height=40, size_hint_x=None, width=500)
        btn.bind(on_release=lambda btn: dropdown3.select(btn.text)) 
        dropdown3.add_widget(btn)
        for key in NAME_BY_INDEX:
            btn = Button(text=NAME_BY_INDEX[key], size_hint_y=None, height=40, size_hint_x=None, width=500)
            btn.bind(on_release=lambda btn: dropdown3.select(btn.text)) 
            dropdown3.add_widget(btn)
        self.country_button.bind(on_release=dropdown3.open)
        dropdown3.bind(on_select=lambda instance, x: setattr(self.country_button, 'text', x)) 
        show_graph_button = Button(text="Show Graph", size_hint_y=None, height=40, size_hint_x=None, width=500, on_press=self._country_on_click)

        
        left_mid.add_widget(self.scroll1)

        left_bot.add_widget(self.country_button)
        left_bot.add_widget(self.scroll)
        left_bot.add_widget(show_graph_button)

        left.add_widget(left_top)
        left.add_widget(left_mid)
        left.add_widget(left_bot)

        root.add_widget(left)
        root.add_widget(self.map_view)

        return root

    def _on_click(self, instance) -> None:
        path = ""
        #self.probability_view.clear_widgets()
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

        elif self.option_button.text == "Optimum Route":
            m = distance.adjacency_matrix()
            scores = SENTIMENT
            solver = ModifiedNearestNeighbourSolver(m, scores, start=INDEX_BY_NAME[self.start_button.text])
            route = solver.best_route()
            routes = solver.all_route()
            graph = Probability_distribution(routes, self.start_button.text).plot_graph()
            self.probability_view1.show_graph(self.start_button.text+"probability.html")
            #self.probability_view.add_widget(FigureCanvasKivyAgg(graph.plot_graph(0.35)))
            print("Routes: ", routes)
            for i in route:
                path += i + ","
            
            
        self.map_view.set_path(path)
        print(path)
        

    def _country_on_click(self, instance):
        #self.graph_view.clear_widgets()
        if self.country_button.text == "Sentiment Score":
            graph1 = Sentiment_graph().plot_graph()
            self.sentiment_view1.show_graph("sentiment.html")
            #self.graph_view.add_widget(FigureCanvasKivyAgg(graph1.plot_graph(0.35)))
        else:
            graph1= Graph(self.country_button.text).plot_all_graph()
            self.sentiment_view1.show_graph(self.country_button.text+"graph.html")
            #self.graph_view.add_widget(FigureCanvasKivyAgg(graph1.plot_all_graph(0.35)))




if __name__ == '__main__':
    app = TripyApp()
    TripyApp().run()
