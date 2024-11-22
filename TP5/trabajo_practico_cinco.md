# Sistema de Estadías en Hoteles 🏨

## Índice
- [Diagrama](#diagrama)
- [Descripción del Esquema](#descripción-del-esquema)
- [Tablas y sus Propósitos](#tablas-y-sus-propósitos)
- [Justificación del Diseño](#justificación-del-diseño)

## Diagrama

El código está en formato DBML ([dbdiagram.io](https://dbdiagram.io)):

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
```

## Descripción del Esquema

El esquema propuesto consta de cinco tablas principales que modelan el sistema de estadías en hoteles. Cada tabla cumple un rol específico en la gestión de reservas y administración hotelera.

## Tablas y sus Propósitos

### 📝 Tabla HOTEL
- **Clave Principal:** `codHotel`
- **Propósito:** Almacena la información básica de cada hotel
- **Campos Importantes:**
  - Ciudad
  - Dirección
  - Cantidad de habitaciones
  - DNI del gerente (FK)

### 👔 Tabla GERENTE
- **Clave Principal:** `dniGerente`
- **Propósito:** Contiene la información de los gerentes
- **Campos Importantes:**
  - Nombre
  - Apellido

### 🛏️ Tabla HABITACION
- **Clave Principal:** `codHotel`, `nroHabitacion`
- **Propósito:** Registra las habitaciones de cada hotel
- **Campos Importantes:**
  - Tipo
  - Precio

### 👥 Tabla CLIENTE
- **Clave Principal:** `dniCliente`
- **Propósito:** Almacena los datos de los clientes
- **Campos Importantes:**
  - Nombre
  - Apellido
  - Teléfono

### 📅 Tabla ESTADIA
- **Clave Principal:** `codHotel`, `nroHabitacion`, `dniCliente`, `fechaInicio`
- **Propósito:** Registra las reservas y estadías realizadas
- **Campos Importantes:**
  - Duración de la estadía

## Justificación del Diseño

### Cumplimiento de Restricciones

#### 1. Gestión de Gerentes
- ✅ Un único gerente por hotel
- ✅ Relación HOTEL → GERENTE mediante FK `dniGerente`
- ✅ Un gerente puede administrar múltiples hoteles

#### 2. Sistema de Reservas
- ✅ Cliente puede reservar múltiples habitaciones
- ✅ La tabla ESTADIA permite múltiples registros por cliente y fecha
- ✅ Claves primarias compuestas para mayor flexibilidad

#### 3. Administración de Habitaciones
- ✅ Control de capacidad mediante `cantidadHabitaciones`
- ✅ Números de habitación pueden repetirse entre hoteles
- ✅ Identificación única mediante combinación `codHotel` y `nroHabitacion`

#### 4. Características del Hotel
- ✅ Código de hotel único garantizado
- ✅ Permite múltiples hoteles en una misma dirección
- ✅ Flexibilidad en ubicación y distribución