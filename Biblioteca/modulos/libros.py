from db.conexion import conectar
import mysql.connector

def agregar_libro(titulo: str, autor: str, editorial: str, isbn: str, anio_publicacion: int, cantidad_disponible: int):
    conexion = conectar()
    cursor = conexion.cursor()
    sql = """
    INSERT INTO libros (titulo, autor, editorial, isbn, anio_publicacion, cantidad_disponible)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    try:
        cursor.execute(sql, (titulo, autor, editorial, isbn, anio_publicacion, cantidad_disponible))
        conexion.commit()
        print("Libro agregado correctamente.")
    except mysql.connector.IntegrityError as e:
        if "Duplicate entry" in str(e):
            print("El libro ya existe en la base de datos.")
        else:
            print("Error de integridad: ", e)
    except Exception as e:
        print("Error al agregar el libro: ", e)
    finally:
        cursor.close()
        conexion.close()


def listar_libros():
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
    sql = "SELECT * FROM libros"
    try:
        cursor.execute(sql)
        return cursor.fetchall()
    except Exception as e:
        print("Error al listar los libros: ", e)
        return []
    finally:
        cursor.close()
        conexion.close()


def actualizar_libro(libro_id: int, titulo: str, autor: str, isbn: str, editorial: str, anio_publicacion: int, cantidad_disponible: int):
    conexion = conectar()
    cursor = conexion.cursor()
    sql = """
    UPDATE libros
    SET titulo=%s, autor=%s, isbn=%s, editorial=%s, anio_publicacion=%s, cantidad_disponible=%s
    WHERE libro_id = %s
    """
    try:
        cursor.execute(sql, (titulo, autor, isbn, editorial, anio_publicacion, cantidad_disponible, libro_id))
        conexion.commit()
        print("Libro actualizado correctamente.")
    except Exception as e:
        print("Error al actualizar el libro: ", e)
    finally:
        cursor.close()
        conexion.close()


def eliminar_libro(libro_id: int):
    conexion = conectar()
    cursor = conexion.cursor()
    sql = "DELETE FROM libros WHERE libro_id = %s"
    try:
        cursor.execute(sql, (libro_id,))
        conexion.commit()
        print(f"Libro con ID {libro_id} eliminado correctamente")
    except Exception as e:
        print("Error al eliminar el libro: ", e)
    finally:
        cursor.close()
        conexion.close()

def buscar_libros(termino_busqueda):
    """
    Busca libros por título, autor o ISBN de manera parcial
    """
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
    sql = """
    SELECT * FROM libros 
    WHERE titulo LIKE %s OR 
          autor LIKE %s OR 
          isbn LIKE %s
    """
    termino = f"%{termino_busqueda}%"
    try:
        cursor.execute(sql, (termino, termino, termino))
        return cursor.fetchall()
    except Exception as e:
        print("Error al buscar libros:", e)
        return []
    finally:
        cursor.close()
        conexion.close()