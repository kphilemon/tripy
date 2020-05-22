import tkinter as tk


class App(tk.Tk):
    def __init__(self):
        super().__init__()

    def run(self):
        self.title('Tripy')
        self.mainloop()


if __name__ == '__main__':
    app = App()
    app.run()
