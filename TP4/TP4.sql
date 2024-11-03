CREATE DATABASE practica_tareas;
USE practica_tareas;

-- Crear la tabla de Empleados
CREATE TABLE Empleados (
    Id INT PRIMARY KEY AUTO_INCREMENT,
    Nombre VARCHAR(100) NOT NULL,
    Departamento VARCHAR(50) NOT NULL,
    TareasPendientes INT DEFAULT 0
);

-- Crear la tabla de Tareas
CREATE TABLE Tareas (
    TareaId INT PRIMARY KEY AUTO_INCREMENT,
    Descripcion VARCHAR(255) NOT NULL,
    Prioridad INT NOT NULL
);

-- Crear la tabla de TareasAsignadas
CREATE TABLE TareasAsignadas (
    AsignacionId INT PRIMARY KEY AUTO_INCREMENT,
    EmpleadoId INT NOT NULL,
    TareaId INT NOT NULL,
    FechaAsignacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (EmpleadoId) REFERENCES Empleados(Id),
    FOREIGN KEY (TareaId) REFERENCES Tareas(TareaId)
);

-- Insertar empleados de ejemplo
INSERT INTO Empleados (Nombre, Departamento) VALUES 
    ('Juan Pérez', 'IT'),
    ('Ana García', 'IT'),
    ('Carlos López', 'IT'),
    ('María Rodríguez', 'IT');

-- Insertar tareas de ejemplo
INSERT INTO Tareas (Descripcion, Prioridad) VALUES 
    ('Arreglar bug en producción', 1),
    ('Actualizar documentación', 2),
    ('Hacer backup semanal', 1),
    ('Revisar logs del sistema', 2),
    ('Actualizar antivirus', 3);
    
    DELIMITER //

CREATE PROCEDURE AsignarTareas(IN p_Departamento VARCHAR(50))
BEGIN
    DECLARE v_TareaId INT;
    DECLARE v_EmpleadoId INT;
    DECLARE v_finished INTEGER DEFAULT 0;

    DECLARE tareas_cursor CURSOR FOR 
        SELECT TareaId
        FROM Tareas
        WHERE TareaId NOT IN (SELECT TareaId FROM TareasAsignadas)
        ORDER BY Prioridad ASC;

    DECLARE CONTINUE HANDLER FOR NOT FOUND SET v_finished = 1;

    START TRANSACTION;

    OPEN tareas_cursor;

    tareas_loop: LOOP
        FETCH tareas_cursor INTO v_TareaId;

        IF v_finished = 1 THEN 
            LEAVE tareas_loop;
        END IF;

        SELECT Id INTO v_EmpleadoId
        FROM Empleados
        WHERE Departamento = p_Departamento
        ORDER BY TareasPendientes ASC
        LIMIT 1;

        INSERT INTO TareasAsignadas (EmpleadoId, TareaId)
        VALUES (v_EmpleadoId, v_TareaId);

        UPDATE Empleados
        SET TareasPendientes = TareasPendientes + 1
        WHERE Id = v_EmpleadoId;

    END LOOP;

    CLOSE tareas_cursor;

    COMMIT;
END //

DELIMITER ;

-- Ejecutar el procedimiento
CALL AsignarTareas('IT');

-- Ver los resultados
SELECT 
    e.Nombre,
    e.TareasPendientes,
    t.Descripcion as TareaAsignada,
    t.Prioridad
FROM Empleados e
JOIN TareasAsignadas ta ON e.Id = ta.EmpleadoId
JOIN Tareas t ON ta.TareaId = t.TareaId
ORDER BY e.Nombre;

    