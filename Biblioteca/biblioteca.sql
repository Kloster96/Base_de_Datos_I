CREATE TABLE `usuarios` (
  `usuario_id` int PRIMARY KEY AUTO_INCREMENT,
  `nombre` varchar(255) NOT NULL,
  `apellido` varchar(255) NOT NULL,
  `email` varchar(255) UNIQUE NOT NULL,
  `telefono` varchar(255),
  `fecha_registro` date NOT NULL,
  `activo` boolean DEFAULT true
);

CREATE TABLE `libros` (
  `libro_id` int PRIMARY KEY AUTO_INCREMENT,
  `titulo` varchar(255) NOT NULL,
  `autor` varchar(255) NOT NULL,
  `isbn` varchar(255) UNIQUE,
  `editorial` varchar(255),
  `anio_publicacion` int,
  `cantidad_disponible` int DEFAULT 1,
  `activo` boolean DEFAULT true
);

CREATE TABLE `prestamos` (
  `prestamo_id` int PRIMARY KEY AUTO_INCREMENT,
  `usuario_id` int,
  `libro_id` int,
  `fecha_prestamo` date NOT NULL,
  `fecha_devolucion_esperada` date NOT NULL,
  `fecha_devolucion_real` date,
  `devuelto` boolean DEFAULT false
);

CREATE TABLE `cuotas` (
  `cuota_id` int PRIMARY KEY AUTO_INCREMENT,
  `usuario_id` int,
  `monto` decimal NOT NULL,
  `fecha_vencimiento` date NOT NULL,
  `fecha_pago` date,
  `pagado` boolean DEFAULT false
);

CREATE TABLE `multas` (
  `multa_id` int PRIMARY KEY AUTO_INCREMENT,
  `prestamo_id` int,
  `monto` decimal NOT NULL,
  `descripcion` varchar(255),
  `pagado` boolean DEFAULT false,
  `fecha_generacion` date NOT NULL
);

ALTER TABLE `prestamos` ADD FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`usuario_id`);

ALTER TABLE `prestamos` ADD FOREIGN KEY (`libro_id`) REFERENCES `libros` (`libro_id`);

ALTER TABLE `cuotas` ADD FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`usuario_id`);

ALTER TABLE `multas` ADD FOREIGN KEY (`prestamo_id`) REFERENCES `prestamos` (`prestamo_id`);
