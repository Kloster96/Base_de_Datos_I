
# Sistema de Gestión de Biblioteca

## Descripción General
El sistema de gestión de biblioteca es una aplicación de escritorio desarrollada en Python utilizando Tkinter para la interfaz gráfica y MySQL como base de datos. El sistema permite gestionar usuarios, libros, préstamos, cuotas y multas de una biblioteca.

## Modelo Entidad-Relación

### Diagrama de Base de Datos
```sql
-- Usuarios de la biblioteca
CREATE TABLE usuarios (
    usuario_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    telefono VARCHAR(20),
    fecha_registro DATE NOT NULL,
    activo BOOLEAN DEFAULT TRUE
);

-- Libros disponibles
CREATE TABLE libros (
    libro_id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(200) NOT NULL,
    autor VARCHAR(100) NOT NULL,
    isbn VARCHAR(50) UNIQUE,
    editorial VARCHAR(100),
    anio_publicacion INT,
    cantidad_disponible INT DEFAULT 1,
    activo BOOLEAN DEFAULT TRUE
);

-- Préstamos de libros
CREATE TABLE prestamos (
    prestamo_id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT,
    libro_id INT,
    fecha_prestamo DATE NOT NULL,
    fecha_devolucion_esperada DATE NOT NULL,
    fecha_devolucion_real DATE,
    devuelto BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(usuario_id),
    FOREIGN KEY (libro_id) REFERENCES libros(libro_id)
);

-- Cuotas mensuales
CREATE TABLE cuotas (
    cuota_id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT,
    monto DECIMAL(10,2) NOT NULL,
    fecha_vencimiento DATE NOT NULL,
    fecha_pago DATE,
    pagado BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(usuario_id)
);

-- Multas por retrasos
CREATE TABLE multas (
    multa_id INT AUTO_INCREMENT PRIMARY KEY,
    prestamo_id INT,
    monto DECIMAL(10,2) NOT NULL,
    descripcion VARCHAR(255),
    pagado BOOLEAN DEFAULT FALSE,
    fecha_generacion DATE NOT NULL,
    FOREIGN KEY (prestamo_id) REFERENCES prestamos(prestamo_id)
);
```

## Script de Creación de Base de Datos

```sql
-- Crear base de datos
CREATE DATABASE biblioteca;
USE biblioteca;

-- Tabla Usuarios
CREATE TABLE usuarios (
    usuario_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    telefono VARCHAR(20),
    fecha_registro DATE NOT NULL,
    activo BOOLEAN DEFAULT TRUE
);

-- Tabla Libros
CREATE TABLE libros (
    libro_id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(200) NOT NULL,
    autor VARCHAR(100) NOT NULL,
    isbn VARCHAR(50) UNIQUE,
    editorial VARCHAR(100),
    anio_publicacion INT,
    cantidad_disponible INT DEFAULT 1,
    activo BOOLEAN DEFAULT TRUE
);

-- Tabla Préstamos
CREATE TABLE prestamos (
    prestamo_id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT,
    libro_id INT,
    fecha_prestamo DATE NOT NULL,
    fecha_devolucion_esperada DATE NOT NULL,
    fecha_devolucion_real DATE,
    devuelto BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(usuario_id),
    FOREIGN KEY (libro_id) REFERENCES libros(libro_id)
);

-- Tabla Cuotas
CREATE TABLE cuotas (
    cuota_id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT,
    monto DECIMAL(10,2) NOT NULL,
    fecha_vencimiento DATE NOT NULL,
    fecha_pago DATE,
    pagado BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(usuario_id)
);

-- Tabla Multas
CREATE TABLE multas (
    multa_id INT AUTO_INCREMENT PRIMARY KEY,
    prestamo_id INT,
    monto DECIMAL(10,2) NOT NULL,
    descripcion VARCHAR(255),
    pagado BOOLEAN DEFAULT FALSE,
    fecha_generacion DATE NOT NULL,
    FOREIGN KEY (prestamo_id) REFERENCES prestamos(prestamo_id)
);
```

## Estructura del Proyecto
El proyecto está compuesto por varios módulos principales:

- **interfaz.py**: Interfaz gráfica de usuario (GUI)
- **usuarios.py**: Gestión de usuarios
- **libros.py**: Gestión de libros
- **prestamos.py**: Gestión de préstamos y multas
- **conexion.py**: Conexión a la base de datos

## Funcionalidades Principales

### Gestión de Usuarios
- Agregar nuevos usuarios
- Listar usuarios
- Identificar usuarios con cuotas pendientes

### Gestión de Libros
- Agregar nuevos libros
- Listar libros
- Actualizar información de libros
- Eliminar libros

### Gestión de Préstamos
- Registrar préstamos
- Devolver libros
- Calcular multas por retraso
- Listar préstamos activos e históricos

### Gestión de Cuotas y Multas
- Identificar usuarios con cuotas pendientes
- Registrar multas por retraso en devolución de libros
- Listar usuarios con multas pendientes

## Características Técnicas

### Tecnologías Utilizadas
- **Lenguaje**: Python
- **Interfaz Gráfica**: Tkinter
- **Base de Datos**: MySQL
- **Librería de Conexión**: mysql-connector-python

## Detalles de Implementación

### Interfaz de Usuario
- Ventanas emergentes para diferentes acciones
- Uso de Treeview para mostrar listados
- Validación de entrada de datos
- Mensajes de confirmación y error

### Gestión de Base de Datos
- Conexión mediante función `conectar()` en `conexion.py`
- Manejo de transacciones y excepciones
- Uso de consultas parametrizadas para prevenir inyección SQL

### Cálculo de Multas
- Multa de $30 por día de retraso en la devolución
- Cálculo automático basado en la fecha de devolución esperada

## Mejoras Potenciales
- Implementar autenticación de usuarios
- Añadir más validaciones de entrada de datos
- Mejorar el manejo de errores y logging
- Implementar backup de base de datos
- Añadir más opciones de búsqueda y filtrado

## Consideraciones de Seguridad
- Credenciales de base de datos directamente en el código (recomendado usar variables de entorno)
- Implementar conexiones seguras
- Validar y sanitizar todas las entradas de usuario

## Conclusión
El sistema proporciona una solución integral para la gestión de una biblioteca pequeña o mediana, con funcionalidades completas de registro, préstamo y seguimiento de libros y usuarios.
