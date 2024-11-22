# **Diseño de Base de Datos: Sistema de Estadías en Hoteles**  

---

## **Diagrama**
_El código está en formato DBML ([dbdiagram.io](https://dbdiagram.io)):_

```dbml
Table HOTEL {
  codHotel int [pk]
  ciudadHotel varchar
  direccionHotel varchar
  cantidadHabitaciones int
  dniGerente int [ref: > GERENTE.dniGerente]
}

Table GERENTE {
  dniGerente int [pk]
  nombre varchar
  apellido varchar
}

Table HABITACION {
  codHotel int [pk, ref: > HOTEL.codHotel]
  nroHabitacion int [pk]
  tipo varchar
  precio decimal
}

Table CLIENTE {
  dniCliente int [pk]
  nombre varchar
  apellido varchar
  telefono varchar
}

Table ESTADIA {
  codHotel int [pk, ref: > HOTEL.codHotel]
  nroHabitacion int [pk, ref: > HABITACION.nroHabitacion]
  dniCliente int [pk, ref: > CLIENTE.dniCliente]
  fechaInicio date [pk]
  cantidadDias int
}
Descripción del Esquema
El esquema propuesto consta de cinco tablas principales que modelan el sistema de estadías en hoteles.

Tablas y sus Propósitos
Tabla	Propósito	Clave Principal (PK)	Campos Importantes
HOTEL	Almacena la información básica de cada hotel.	codHotel	ciudad, dirección, cantidad de habitaciones
GERENTE	Contiene la información de los gerentes.	dniGerente	nombre, apellido
HABITACION	Registra las habitaciones de cada hotel.	codHotel, nroHabitacion	tipo, precio
CLIENTE	Almacena los datos de los clientes.	dniCliente	nombre, apellido, teléfono
ESTADIA	Registra las reservas y estadías realizadas por los clientes.	codHotel, nroHabitacion,	duración de la estadía
dniCliente, fechaInicio	
Justificación de las Decisiones de Diseño
Cumplimiento de Restricciones
Único gerente por hotel
Relación HOTEL → GERENTE (FK dniGerente).
Cada hotel tiene un único gerente; sin embargo, un gerente puede administrar múltiples hoteles.
Cliente puede reservar múltiples habitaciones
La tabla ESTADIA permite múltiples registros para el mismo cliente y fecha.
Las claves primarias compuestas garantizan esta flexibilidad.
Cantidad de habitaciones
El campo cantidadHabitaciones en la tabla HOTEL define la capacidad total de cada hotel.
Código de hotel único
codHotel es clave primaria en la tabla HOTEL, garantizando unicidad global.
Reservas en diferentes hoteles
El diseño de ESTADIA permite que un cliente tenga múltiples registros para distintos hoteles.
Número de habitación repetible
El número de habitación (nroHabitacion) se diferencia por el código del hotel (codHotel), permitiendo habitaciones con el mismo número en distintos hoteles.
Múltiples hoteles en una misma dirección
Los campos direccionHotel y ciudadHotel no son únicos, permitiendo varias instalaciones en la misma ubicación.