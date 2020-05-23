import re
from kivy.app import App
from tripy.widgets import MapView
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout


class TripyApp(App):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.btn = Button(text='Plot Line', size_hint_x=None, width=100)
        self.input = TextInput(multiline=False, font_size=18)
        self.map_view = MapView()

    def build(self):
        root = BoxLayout(orientation='vertical')

        input_row = GridLayout(cols=2, padding=5, spacing=2.5, size_hint_y=None, height=50)
        input_row.add_widget(self.input)
        input_row.add_widget(self.btn)

        root.add_widget(input_row)
        root.add_widget(self.map_view)

        self.btn.bind(on_press=self._on_click)

        return root

    def _on_click(self, instance):
        locations = re.split(r',\s*', self.input.text)
        print(locations)
        self.map_view.set_path(locations)


if __name__ == '__main__':
    app = TripyApp()
    app.run()
