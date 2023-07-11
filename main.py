from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.properties import ObjectProperty
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

import db

import sqlite3


pagina_detalle_id: int = -1


class PaginaInicio(Screen):
    caja_lista = ObjectProperty(None)
    widgets = []

    def ver_productos(self, termino_busqueda):
        for w in self.widgets:
            self.caja_lista.remove_widget(w)
        self.widgets = []
        resultado = db.buscar_producto_por_nombre(termino_busqueda)
        if len(resultado) == 0:
            label = Label(
                text="No hay productos.",
                size_hint_y=None,
                height=40,
            )
            self.caja_lista.add_widget(label)
            self.widgets.append(label)
        for prod in resultado:
            item = BoxLayout(
                orientation="horizontal",
                size_hint_y=None,
                height=40,
            )
            boton_ver = Button(
                text="Ver",
                size_hint=(None, None),
                height=40,
                width=60,
                on_release=self.ver_detalle_prod(prod[0])
            )
            label_nombre = Label(
                text=f"{prod[1]}",
                size_hint_y=None,
                height=40,
            )
            item.add_widget(label_nombre)
            item.add_widget(boton_ver)
            self.caja_lista.add_widget(item)
            self.widgets.append(item)

    def ver_detalle_prod(self, id_prod):
        def ir_a_detalle(*args):
            print("pagina detalle", id_prod)
            global pagina_detalle_id
            pagina_detalle_id = id_prod
            myapp.root.transition = SlideTransition(direction='left', duration=.25)
            myapp.root.current = 'detalle'
        return ir_a_detalle


class PaginaDetalle(Screen):
    nombre = ObjectProperty(None)
    descripcion = ObjectProperty(None)
    categoria = ObjectProperty(None)
    precio = ObjectProperty(None)
    stock = ObjectProperty(None)
    boton_guardar = ObjectProperty(None)

    def ver_detalle(self):
        global pagina_detalle_id
        resultado = db.get_producto_por_id(pagina_detalle_id)
        if resultado is not None:
            self.nombre.text = resultado['nombre']
            self.descripcion.text = str(resultado['descripcion'])
            self.categoria.text = str(resultado['categoria'])
            self.precio.text = str(resultado['precio'])
            self.stock.text = str(resultado['stock'])

            self.nombre.disabled = True
            self.descripcion.disabled = True
            self.categoria.disabled = True
            self.precio.disabled = True
            self.stock.disabled = True
            self.boton_guardar.disabled = True

    def activar_modificacion(self):
        self.nombre.disabled ^= 1
        self.descripcion.disabled ^= 1
        self.categoria.disabled ^= 1
        self.precio.disabled ^= 1
        self.stock.disabled ^= 1
        self.boton_guardar.disabled ^= 1

    def modificar_prod(self):
        global pagina_detalle_id
        db.modificar_producto_por_id(
            pagina_detalle_id,
            self.nombre.text,
            self.descripcion.text,
            self.categoria.text,
            self.precio.text,
            self.stock.text,
        )
        self.activar_modificacion()

    def borrar_prod(self):
        global pagina_detalle_id
        db.borrar_producto_por_id(pagina_detalle_id)


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

    def borrar_campos(self):
        self.nombre.text = ""
        self.descripcion.text = ""
        self.categoria.text = ""
        self.precio.text = ""
        self.stock.text = ""


class WindowManager(ScreenManager):
    pass


class MyApp(App):
    def build(self):
        db.crear_tabla()


if __name__ == "__main__":
    myapp = MyApp()
    myapp.run()
