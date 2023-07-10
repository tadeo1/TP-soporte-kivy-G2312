from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty

import sqlite3

import db


class MyGrid(Widget):
    nombre = ObjectProperty(None)
    descripcion = ObjectProperty(None)
    categoria = ObjectProperty(None)
    precio = ObjectProperty(None)
    stock = ObjectProperty(None)

    def alta(self):
        db.crear_producto(
            self.nombre.text,
            self.descripcion.text,
            self.categoria.text,
            self.precio.text,
            self.stock.text
        )


class MyApp(App):
    def build(self):
        db.crear_tabla()
        return MyGrid()



if __name__ == "__main__":
    MyApp().run()
