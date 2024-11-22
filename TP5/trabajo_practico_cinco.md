Diagrama "El codigo esta en DBML(dbdiagram.io)

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
--------------------------------------------------------------------------------------------------------
Diseño de Base de Datos: Sistema de Estadías en Hoteles
Descripción del Esquema
El esquema propuesto consta de cinco tablas principales que modelan el sistema de estadías en hoteles:
Tablas y sus Propósitos

HOTEL
    Almacena la información básica de cada hotel
    Primary Key: codHotel
    Incluye: ciudad, dirección, cantidad de habitaciones y referencia al gerente

GERENTE
    Contiene información de los gerentes
    Primary Key: dniGerente
    Datos personales básicos: nombre y apellido

HABITACION
    Registra las habitaciones de cada hotel
    Primary Key compuesta: (codHotel, nroHabitacion)
    Incluye: tipo y precio

CLIENTE
    Almacena los datos de los clientes
    Primary Key: dniCliente
    Datos personales y de contacto

ESTADIA
    Registra las reservas y estadías
    Primary Key compuesta: (codHotel, nroHabitacion, dniCliente, fechaInicio)
    Incluye: duración de la estadía

--------------------------------------------------------------------------------------------------------
Justificación de las Decisiones de Diseño

Cumplimiento de Restricciones

a. Único gerente por hotel

    Implementado mediante la relación HOTEL -> GERENTE (FK dniGerente)
    Un gerente puede administrar múltiples hoteles, pero cada hotel tiene un único gerente

b. Cliente puede reservar múltiples habitaciones

    La tabla ESTADIA permite múltiples registros para el mismo cliente y fecha
    Las claves primarias compuestas permiten esta flexibilidad

c. Cantidad de habitaciones
    Campo cantidadHabitaciones en la tabla HOTEL
    Sirve como restricción de integridad para verificar el número total de habitaciones

d. Código de hotel único
    codHotel es Primary Key en la tabla HOTEL
    Garantiza la unicidad global del código, independiente de la ciudad

e. Reservas en diferentes hoteles
    El diseño de ESTADIA permite que un cliente tenga múltiples registros
    No hay restricciones que impidan reservas simultáneas en diferentes hoteles

f. Número de habitación repetible
    nroHabitacion es parte de una PK compuesta con codHotel
    Permite que exista el mismo número en diferentes hoteles

g. Múltiples hoteles en una dirección
    direccionHotel y ciudadHotel son campos regulares (no únicos)
    Permite múltiples hoteles en la misma ubicación

----------------------------------------------------------------------------------------------------------------

