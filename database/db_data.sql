-- Datos para room_types
INSERT INTO room_types (id, name, description, base_price) VALUES
	(1, 'Estándar', 'Perfecta para viajeros individuales o parejas que buscan comodidad a un precio accesible.', 130000.00),
	(2, 'Ejecutiva', 'Espacio amplio con áreas separadas para trabajar y descansar, ideal para viajes de negocios.', 220000.00),
	(3, 'Penthouse Premier', 'La máxima experiencia de lujo con espacios exclusivos y servicios personalizados', 450000.00),
	(4, 'Prueba', 'Habitacion de prueba', 350000.00);

-- Datos para rooms
INSERT INTO rooms (id, room_number, floor, status, room_type_id) VALUES
	(1, 201, 2, 'active', 1),
	(3, 202, 2, 'active', 1),
	(4, 203, 2, 'active', 1),
	(5, 204, 2, 'active', 2),
	(6, 205, 2, 'active', 2),
	(7, 301, 3, 'active', 1),
	(8, 302, 3, 'inactive', 1),
	(9, 303, 3, 'maintenance', 1),
	(10, 304, 3, 'active', 2),
	(11, 305, 3, 'active', 2),
	(12, 401, 4, 'maintenance', 2),
	(13, 402, 4, 'inactive', 3),
	(14, 403, 4, 'active', 3),
	(15, 404, 4, 'maintenance', 3),
	(16, 501, 5, 'active', 3),
	(17, 502, 5, 'inactive', 3);
