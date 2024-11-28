from db.conexion import conectar

def buscar_libros_por_titulo(termino_busqueda):
    """
    Busca libros por título de manera parcial.
    """
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
    sql = """
    SELECT * FROM libros 
    WHERE titulo LIKE %s
    """
    termino = f"%{termino_busqueda}%"
    try:
        cursor.execute(sql, (termino,))
        return cursor.fetchall()
    except Exception as e:
        print("Error al buscar libros por título:", e)
        return []
    finally:
        cursor.close()
        conexion.close()

def buscar_libros_por_autor(termino_busqueda):
    """
    Busca libros por autor de manera parcial.
    """
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
    sql = """
    SELECT * FROM libros 
    WHERE autor LIKE %s
    """
    termino = f"%{termino_busqueda}%"
    try:
        cursor.execute(sql, (termino,))
        return cursor.fetchall()
    except Exception as e:
        print("Error al buscar libros por autor:", e)
        return []
    finally:
        cursor.close()
        conexion.close()

def buscar_usuarios_por_id(termino_busqueda):
    """
    Busca usuarios por ID de manera exacta.
    """
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
    sql = """
    SELECT * FROM usuarios 
    WHERE usuario_id = %s
    """
    try:
        cursor.execute(sql, (termino_busqueda,))
        return cursor.fetchall()
    except Exception as e:
        print("Error al buscar usuarios por ID:", e)
        return []
    finally:
        cursor.close()
        conexion.close()

def buscar_usuarios_por_nombre(termino_busqueda):
    """
    Busca usuarios por nombre o apellido de manera parcial.
    """
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
    sql = """
    SELECT * FROM usuarios
    WHERE LOWER(nombre) LIKE %s OR LOWER(apellido) LIKE %s
    """
    termino = f"%{termino_busqueda.strip().lower()}%"  # Aseguramos que no haya espacios y convertimos a minúsculas
    print(f"Consulta SQL: {sql}")
    print(f"Parámetros: {(termino, termino)}")
    try:
        cursor.execute(sql, (termino, termino))
        usuarios = cursor.fetchall()
        print(f"Usuarios encontrados: {usuarios}")
        return usuarios if usuarios else None  # Retorna None si no se encuentra usuario
    except Exception as e:
        print("Error al buscar usuarios:", e)
        return None
    finally:
        cursor.close()
        conexion.close()
