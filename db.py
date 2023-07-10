import sqlite3


def crear_tabla():
    con = sqlite3.connect("myapp.db")
    try:
        con.execute(
            """CREATE TABLE producto (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT(30) NOT NULL UNIQUE,
                descripcion TEXT(100),
                categoria TEXT(20),
                precio REAL NOT NULL,
                stock INTEGER
            )"""
        )
    except sqlite3.OperationalError as e:
        if str(e) != "table producto already exists":
            print(e.sqlite_errorname, e.sqlite_errorcode)
            raise e
        else:
            print("Error ignorado: la tabla producto ya existe")
    finally:
        con.close()


def crear_producto(nombre, descripcion, categoria, precio, stock):
    con = sqlite3.connect("myapp.db")
    con.execute(
        """INSERT INTO producto (nombre, descripcion, categoria, precio, stock)
        VALUES (?,?,?,?,?)""",
        (nombre, descripcion, categoria, precio, stock)
    )
    con.commit()
    con.close()
    print("alta con exito", nombre, descripcion, categoria, precio, stock)
