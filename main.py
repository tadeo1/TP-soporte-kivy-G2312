from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

import db

import sqlite3


class PaginaInicio(Screen):
    caja_lista = ObjectProperty(None)
    widgets = []

    def ver_productos(self, nombre):
        for w in self.widgets:
            self.caja_lista.remove_widget(w)
        self.widgets = []
        resultado = db.buscar_producto_por_nombre(nombre)
        for prod in resultado:
            nombre = Label(
                text=f"{prod[1]}",
                size_hint_y=None,
                height=40
            )
            self.caja_lista.add_widget(nombre)
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


class PaginaBaja(Screen):
    caja_lista = ObjectProperty(None)
    widgets = []

    def listar_borrado_productos(self, termino_busqueda):
        for w in self.widgets:
            self.caja_lista.remove_widget(w)
        self.widgets = []
        resultado = db.buscar_producto_por_nombre(termino_busqueda)
        for prod in resultado:
            item = BoxLayout(
                orientation="horizontal",
                size_hint_y=None,
                height=40,
            )
            boton_borrar = Button(
                text="Borrar",
                size_hint=(None, None),
                height=40,
                width=60,
                # font_size=12,
                # background_normal='borrar.png',
                # background_down='borrar.png',
                # size_hint=(.3, .3),
                # pos_hint={"x": 0.35, "y": 0.3},
                on_release=self.borrar_prod(prod[1], termino_busqueda)
            )
            label_nombre = Label(
                text=f"{prod[1]}",
                size_hint_y=None,
                height=40,
                # font_size=12,
            )
            item.add_widget(label_nombre)
            item.add_widget(boton_borrar)
            self.caja_lista.add_widget(item)
            self.widgets.append(item)

    def borrar_prod(self, nombre, termino_busqueda):
        def func_borrar(*args):
            db.borrar_producto_por_nombre(nombre)
            self.listar_borrado_productos(termino_busqueda)
        return func_borrar


class WindowManager(ScreenManager):
    pass


class MyApp(App):
    def build(self):
        db.crear_tabla()


if __name__ == "__main__":
    MyApp().run()
