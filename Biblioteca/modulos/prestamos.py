from db.conexion import conectar
from decimal import Decimal
from datetime import datetime

import math

def reporte_morosos_promedio():
    """
    Calcula el promedio de meses que los usuarios están atrasados con sus cuotas.
    Redondea los valores hacia arriba y elimina aquellos con promedio 0.
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
        morosos = cursor.fetchall()  # Devuelve una lista con los usuarios morosos y su promedio de meses

        # Filtrar y procesar los resultados
        morosos_filtrados = []
        for moroso in morosos:
            promedio_meses = moroso["promedio_meses_pendientes"]

            # Si el promedio es mayor que 0, lo redondeamos hacia arriba
            if promedio_meses > 0:
                moroso["promedio_meses_pendientes"] = math.ceil(promedio_meses)  # Redondear hacia arriba
                morosos_filtrados.append(moroso)  # Agregar a la lista filtrada

        return morosos_filtrados  # Devolver la lista de usuarios con los promedios ajustados

    except Exception as e:
        print("Error al obtener reporte de morosos:", e)
        return []
    finally:
        cursor.close()
        conexion.close()


def modificar_cuota(usuario_id, anio, mes, nuevo_monto):
    """
    Modifica el monto de una cuota para un mes y año específicos.
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
            print(f"Cuota modificada exitosamente para el usuario {usuario_id} en {mes}/{anio}")
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

def calcular_multa_por_retraso(prestamo_id):
    """
    Calcula la multa por retraso en la devolución de un libro para un prestamo_id dado.
    La multa es el 3% de la cuota mensual por cada día de retraso.
    """
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)

    # Primero, obtener el prestamo y los detalles de la cuota del usuario
    sql_prestamo = """
    SELECT p.fecha_devolucion_esperada, p.fecha_devolucion_real, c.monto, p.devuelto
    FROM prestamos p
    JOIN cuotas c ON p.usuario_id = c.usuario_id
    WHERE p.prestamo_id = %s
    AND c.pagado = FALSE  -- Solo consideramos los préstamos con cuotas impagas
    """
    
    try:
        cursor.execute(sql_prestamo, (prestamo_id,))
        prestamos = cursor.fetchall()  # Usar fetchall() en lugar de fetchone()

        if not prestamos:
            print("No se encontró el préstamo o la cuota está pagada.")
            return None

        for prestamo in prestamos:  # Iterar sobre los resultados si hay más de uno
            # Verificar si el libro ya ha sido devuelto
            if prestamo['devuelto']:
                print("El libro ya ha sido devuelto.")
                return None

            # Obtener las fechas de devolución
            fecha_devolucion_esperada = prestamo['fecha_devolucion_esperada']
            fecha_devolucion_real = prestamo['fecha_devolucion_real']

            if not fecha_devolucion_real:
                # Si no hay fecha de devolución real, consideramos la fecha actual
                fecha_devolucion_real = datetime.today().date()

            if fecha_devolucion_real > fecha_devolucion_esperada:
                # Calcular los días de retraso
                retraso = (fecha_devolucion_real - fecha_devolucion_esperada).days
                multa = Decimal(prestamo['monto']) * Decimal(0.03) * Decimal(retraso)  # 3% de la cuota por cada día de retraso

                # Insertar multa en la tabla de multas
                sql_insert_multa = """
                INSERT INTO multas (prestamo_id, monto, descripcion, fecha_generacion)
                VALUES (%s, %s, %s, CURDATE())
                """
                descripcion = f"Multa por retraso de {retraso} días."
                cursor.execute(sql_insert_multa, (prestamo_id, multa, descripcion))
                conexion.commit()

                print(f"Multa generada: ${multa} por retraso de {retraso} días.")
                return multa
            else:
                print("No hay retraso en la devolución del libro.")
                return None

    except Exception as e:
        print("Error al calcular la multa:", e)
        return None
    finally:
        cursor.close()
        conexion.close()

def obtener_usuarios_morosos():
    """
    Obtiene una lista de usuarios con cuotas impagas, y el monto pendiente de cada uno.
    """
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)

    sql = """
    SELECT u.usuario_id, u.nombre, u.apellido, COUNT(c.cuota_id) AS cuotas_pendientes, SUM(c.monto) AS monto_pendiente
    FROM usuarios u
    INNER JOIN cuotas c ON u.usuario_id = c.usuario_id
    WHERE c.pagado = FALSE
    GROUP BY u.usuario_id
    HAVING cuotas_pendientes > 0
    """
    
    try:
        cursor.execute(sql)
        return cursor.fetchall()  # Devuelve los usuarios con cuotas pendientes
    except Exception as e:
        print("Error al obtener usuarios morosos:", e)
        return []
    finally:
        cursor.close()
        conexion.close()







