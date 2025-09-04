-- seed.sql: 10 filas por tabla (usuarios, productos, ventas, detalle_ventas)

-- 1. usuarios
INSERT INTO usuarios (nombre, email, password_hash, rol, creado_en) VALUES
('Carlos Pérez', 'carlos.perez@example.com', 'hash123', 'admin', '2025-09-01 09:00:00+00'),
('María Gómez', 'maria.gomez@example.com', 'hash456', 'vendedor', '2025-09-01 09:05:00+00'),
('Juan Torres', 'juan.torres@example.com', 'hash789', 'vendedor', '2025-09-01 09:10:00+00'),
('Ana Ramírez', 'ana.ramirez@example.com', 'hash321', 'vendedor', '2025-09-01 09:15:00+00'),
('Luis Martínez', 'luis.martinez@example.com', 'hash654', 'vendedor', '2025-09-01 09:20:00+00'),
('Sofía Hernández', 'sofia.hernandez@example.com', 'hash987', 'admin', '2025-09-01 09:25:00+00'),
('Pedro Castillo', 'pedro.castillo@example.com', 'hash111', 'vendedor', '2025-09-01 09:30:00+00'),
('Laura Ortega', 'laura.ortega@example.com', 'hash222', 'vendedor', '2025-09-01 09:35:00+00'),
('Andrés Silva', 'andres.silva@example.com', 'hash333', 'vendedor', '2025-09-01 09:40:00+00'),
('Fernanda Díaz', 'fernanda.diaz@example.com', 'hash444', 'vendedor', '2025-09-01 09:45:00+00');

-- 2. productos
INSERT INTO productos (nombre, descripcion, precio, stock, creado_en) VALUES
('Laptop Lenovo ThinkPad', 'Laptop 16GB RAM, 512GB SSD', 850.00, 15, now()),
('Mouse Logitech MX Master', 'Mouse inalámbrico ergonómico', 95.00, 50, now()),
('Teclado Mecánico Keychron', 'Teclado RGB', 120.00, 30, now()),
('Monitor Dell 27', 'Monitor QHD 27"', 320.00, 25, now()),
('Auriculares Sony WH-1000XM5', 'Cancelación de ruido', 280.00, 20, now()),
('Disco Duro Externo 2TB', 'USB 3.0', 110.00, 40, now()),
('Silla Ergonómica', 'Soporte lumbar', 210.00, 18, now()),
('Impresora HP LaserJet', 'Láser multifunción', 150.00, 12, now()),
('Tablet Samsung Tab S8', 'Tablet Android', 650.00, 10, now()),
('Smartwatch Apple Watch SE', 'Reloj con GPS', 300.00, 22, now());

-- 3. ventas (usuario_id deben existir)
INSERT INTO ventas (usuario_id, fecha, total) VALUES
(2, '2025-09-01 10:30:00+00', 1245.00),
(3, '2025-09-01 11:00:00+00', 300.00),
(4, '2025-09-01 12:15:00+00', 450.00),
(5, '2025-09-01 14:00:00+00', 220.00),
(6, '2025-09-02 09:45:00+00', 1050.00),
(7, '2025-09-02 10:20:00+00', 520.00),
(8, '2025-09-02 15:30:00+00', 750.00),
(9, '2025-09-03 16:00:00+00', 980.00),
(10,'2025-09-03 17:15:00+00', 310.00),
(2, '2025-09-03 18:45:00+00', 640.00);

-- 4. detalle_ventas (venta_id y producto_id deben existir)
INSERT INTO detalle_ventas (venta_id, producto_id, cantidad, precio_unitario, subtotal) VALUES
(1, 1, 1, 850.00, 850.00),
(1, 2, 2, 95.00, 190.00),
(1, 3, 1, 120.00, 120.00),
(2, 10, 1, 300.00, 300.00),
(3, 4, 1, 320.00, 320.00),
(3, 2, 1, 95.00, 95.00),
(4, 6, 2, 110.00, 220.00),
(5, 5, 2, 280.00, 560.00),
(6, 1, 1, 850.00, 850.00),
(6, 8, 1, 150.00, 150.00),
(7, 7, 2, 210.00, 420.00),
(7, 2, 1, 95.00, 95.00),
(8, 9, 1, 650.00, 650.00),
(8, 3, 1, 120.00, 120.00),
(9, 10, 1, 300.00, 300.00),
(10, 4, 2, 320.00, 640.00);
