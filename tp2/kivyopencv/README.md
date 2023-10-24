# App Login Registro Facial con OpenCV y Kivy

Creamos una app de Kivy con OpenCV con la cual podemos realziar el login con reoconocimiento facial utilizando la libreria (OpenCV). 

La consigna del trabajo es:

Crear una aplicación CÁMARA empleando OpenCV y Kivy con las siguientes características:

1) Logeo por reconocimiento facial (tener el cuenta solo el alta de ususario, no es necesario bajas y modificaciones).

2) Si detecta un rostro que habilite la captura según las siguientes situaciones:

	a) Si detecta la mano izquierda: Tomar una foto cuando cuente 5 segundos mostrando en la pantalla la cuenta regresiva.
	b) Si detecta la mano derecha: Grabar un video hasta que deje de detectar la mano derecha.

3) Grabar el nombre de los archivos creados (video o imágenes) y mostrar en una lista para poder reproducirla mediante un click.

## Demostracion
https://youtu.be/lIMfghmwZio

## Iniciar la app
*Se recomienda utilzar un entorno virtual para ininciar la app y descargar librerias*

Crear entorno virtual
```
python -m venv .venv
.\.venv\Scripts\activate
```

Descargar App
```
git clone https://github.com/santipdmonte/Soporte2023_Kivy_OpenCV_APP
cd Soporte2023_Kivy_OpenCV_APP
pip install -r requirements.txt
```

Ejecurar el archivo index.py
