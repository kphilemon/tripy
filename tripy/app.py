from kivy.app import App
from tripy.widgets import MapView


class TripyApp(App):

    def build(self):
        return MapView()


if __name__ == '__main__':
    app = TripyApp()
    app.run()
