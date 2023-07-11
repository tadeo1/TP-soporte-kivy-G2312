from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.label import Label
from kivy.uix.popup import Popup

import db

import sqlite3


class PaginaInicio(Screen):
    caja = ObjectProperty(None)
    widgets = []

    def ver_productos(self, nombre):
        for w in self.widgets:
            self.caja.remove_widget(w)
        self.widgets = []
        resultado = db.buscar_producto_por_nombre(nombre)
        for prod in resultado:
            nombre = Label(text=f"{prod[1]}")
            self.caja.add_widget(nombre)
            self.widgets.append(nombre)


class PaginaAlta(Screen):
    nombre = ObjectProperty(None)
    descripcion = ObjectProperty(None)
    categoria = ObjectProperty(None)
    precio = ObjectProperty(None)
    stock = ObjectProperty(None)

    def alta(self):
        if self.nombre.text != "" and self.precio.text != "":
            try:
                db.crear_producto(
                    self.nombre.text,
                    self.descripcion.text,
                    self.categoria.text,
                    self.precio.text,
                    self.stock.text
                )
            except sqlite3.IntegrityError as e:
                if e.sqlite_errorname == "SQLITE_CONSTRAINT_UNIQUE":
                    popup = Popup(size_hint=(None, None))
                    popup.title = "Error"
                    popup.size = (self.width * 0.5, self.height * 0.2)
                    popup.content = Label(text=f"Ya existe el producto con nombre: '{self.nombre.text}'")
                    popup.open()

                    print(f"Ya existe el producto con nombre: '{self.nombre.text}'")
        else:
            popup = Popup(size_hint=(None, None))
            popup.title = "Error"
            popup.size = (self.width*0.5, self.height*0.2)
            popup.content= Label(text="Falta ingresar nombre y/o precio")
            popup.open()

            print("Falta ingresar nombre y/o precio")


class WindowManager(ScreenManager):
    pass


class MyApp(App):
    def build(self):
        db.crear_tabla()


if __name__ == "__main__":
    MyApp().run()
