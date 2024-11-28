from db.conexion import conectar
import mysql.connector
from datetime import datetime

def agregar_usuario(nombre:str, apellido:str, email:str, telefono:int):
    conexion = conectar()
    cursor = conexion.cursor()
    sql = """
    INSERT INTO usuarios (nombre, apellido, email, telefono, fecha_registro)
    VALUES (%s, %s, %s, %s, CURDATE())
    """
    try:
        cursor.execute(sql, (nombre, apellido, email, telefono))
        conexion.commit()
        print("Usuario agregado exitosamente.")
    except mysql.connector.IntegrityError as e:
        print("El email ya existe en la base de datos.")
    except Exception as e:
        print("Error al agregar el usuario: ", e)
    finally:
        cursor.close()
        conexion.close()

def listar_usuarios():
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
    sql = "SELECT * FROM usuarios"
    try:
        cursor.execute(sql)
        return cursor.fetchall()
    except Exception as e:
        print("Error al listar los usuarios: ", e)
        return []
    finally:
        cursor.close()
        conexion.close()

def listar_morosos_con_monto():
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
    sql = """
    SELECT u.usuario_id, u.nombre AS usuario, u.email,
           COUNT(c.cuota_id) AS cuotas_pendientes, 
           COUNT(c.cuota_id) * 1000 AS monto_total  -- Suponemos que cada cuota vale 1000
    FROM usuarios u
    INNER JOIN cuotas c ON u.usuario_id = c.usuario_id
    WHERE c.pagado = FALSE
    GROUP BY u.usuario_id
    HAVING cuotas_pendientes > 0
    """
    try:
        cursor.execute(sql)
        return cursor.fetchall()  # Devuelve la lista de usuarios con sus cuotas pendientes y monto total
    except Exception as e:
        print("Error al listar morosos con monto:", e)
        return []
    finally:
        cursor.close()
        conexion.close()

def buscar_usuarios(termino_busqueda):
    """
    Busca usuarios por nombre, apellido o email de manera parcial
    """
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
    sql = """
    SELECT * FROM usuarios 
    WHERE nombre LIKE %s OR 
          apellido LIKE %s OR 
          email LIKE %s
    """
    termino = f"%{termino_busqueda}%"
    try:
        cursor.execute(sql, (termino, termino, termino))
        return cursor.fetchall()
    except Exception as e:
        print("Error al buscar usuarios:", e)
        return []
    finally:
        cursor.close()
        conexion.close()

def calcular_promedio_meses_morosos():
    """
    Calcula el promedio de meses de cuotas pendientes para usuarios morosos
    """
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
    sql = """
    SELECT 
        u.usuario_id, 
        u.nombre, 
        u.apellido,
        COUNT(c.cuota_id) AS cuotas_pendientes,
        AVG(TIMESTAMPDIFF(MONTH, c.fecha_vencimiento, CURDATE())) AS promedio_meses_pendientes
    FROM 
        usuarios u
    INNER JOIN 
        cuotas c ON u.usuario_id = c.usuario_id
    WHERE 
        c.pagado = FALSE
    GROUP BY 
        u.usuario_id, u.nombre, u.apellido
    HAVING 
        cuotas_pendientes > 0
    """
    try:
        cursor.execute(sql)
        return cursor.fetchall()
    except Exception as e:
        print("Error al calcular promedio de meses morosos:", e)
        return []
    finally:
        cursor.close()
        conexion.close()

def modificar_cuota(usuario_id, anio, mes, nuevo_monto):
    """
    Modifica el monto de una cuota para un mes y año específicos
    """
    conexion = conectar()
    cursor = conexion.cursor()
    sql = """
    UPDATE cuotas 
    SET monto = %s 
    WHERE usuario_id = %s 
      AND YEAR(fecha_vencimiento) = %s 
      AND MONTH(fecha_vencimiento) = %s
    """
    try:
        cursor.execute(sql, (nuevo_monto, usuario_id, anio, mes))
        conexion.commit()
        
        if cursor.rowcount > 0:
            print(f"Cuota modificada exitosamente para el usuario {usuario_id}")
            return True
        else:
            print(f"No se encontró cuota para el usuario {usuario_id} en {mes}/{anio}")
            return False
    except Exception as e:
        print("Error al modificar cuota:", e)
        return False
    finally:
        cursor.close()
        conexion.close()


def actualizar_usuario(email: str, nuevo_nombre: str, nuevo_apellido: str, nuevo_telefono: int):
    conexion = conectar()
    cursor = conexion.cursor()
    sql = """
    UPDATE usuarios 
    SET nombre = %s, apellido = %s, telefono = %s 
    WHERE email = %s
    """
    try:
        cursor.execute(sql, (nuevo_nombre, nuevo_apellido, nuevo_telefono, email))
        conexion.commit()
        
        # Verificar si se actualizó algún registro
        if cursor.rowcount == 0:
            raise Exception("No se encontró un usuario con ese email")
        
        print("Usuario actualizado exitosamente.")
    except Exception as e:
        conexion.rollback()
        raise e
    finally:
        cursor.close()
        conexion.close()

def eliminar_usuario(email: str):
    conexion = conectar()
    cursor = conexion.cursor()
    sql = "DELETE FROM usuarios WHERE email = %s"
    try:
        cursor.execute(sql, (email,))
        conexion.commit()
        
        # Verificar si se eliminó algún registro
        if cursor.rowcount == 0:
            raise Exception("No se encontró un usuario con ese email")
        
        print("Usuario eliminado exitosamente.")
    except Exception as e:
        conexion.rollback()
        raise e
    finally:
        cursor.close()
        conexion.close()