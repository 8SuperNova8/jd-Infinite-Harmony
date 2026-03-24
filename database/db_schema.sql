CREATE DATABASE IF NOT EXISTS dj_infinite_harmony_hotel;
USE dj_infinite_harmony_hotel;

-- ==================================================
-- CREACIÓN DE TABLAS PARA SISTEMA DE RESERVAS HOTEL
-- ==================================================

-- 1. Tipos de habitaciones
CREATE TABLE room_types (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    description TEXT,
    base_price DECIMAL(10,2) NOT NULL
);

-- 2. Habitaciones
CREATE TABLE rooms (
    id INT AUTO_INCREMENT PRIMARY KEY,
    room_number INT NOT NULL UNIQUE,
    floor INT NOT NULL,
    status ENUM(
        'active',
        'maintenance',
        'inactive') DEFAULT 'active' NOT NULL,
    room_type_id INT NOT NULL,
    FOREIGN KEY (room_type_id) REFERENCES room_types(id) ON DELETE RESTRICT
);

-- 3. Reservas
CREATE TABLE reservations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    room_id INT NOT NULL,
    check_in DATE NOT NULL,
    check_out DATE NOT NULL,
    reservation_date DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    /* confirmed = reserva activa(futuro)
    checked_in = huesped en el hotel (presente)
    cancelled = Canceló (pasado)
    no_show =  No llegó (pasado)
    finished = Termina la estancia del huesped (pasado)*/
    status ENUM(
        'confirmed', 
        'checked_in', 
        'cancelled', 
        'no_show',
        'finished' 
        ) DEFAULT 'confirmed' NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,

    -- Datos del huésped
    guest_name VARCHAR(100) NOT NULL,
    guest_email VARCHAR(100) NOT NULL,
    guest_phone VARCHAR(20) NOT NULL,
    guest_document VARCHAR(50) NOT NULL,
    -- para generar el token de reserva
    token

    -- Datos de tarjeta (SOLO PARA GARANTÍA - NUNCA GUARDAR NÚMERO COMPLETO)`
    /*
    card_last_four VARCHAR(4) NOT NULL, -- Últimos 4 dígitos
    card_holder_name VARCHAR(100) NOT NULL,
    card_brand VARCHAR(20) NOT NULL, -- Visa, MC, Amex
    tokenization_id VARCHAR(100) NOT NULL, -- Token de pago (NO la tarjeta)
    authorization_code VARCHAR(100) NOT NULL, -- Código de autorización de la pre-autorización
    */

    FOREIGN KEY (room_id) REFERENCES rooms(id)  ON DELETE RESTRICT,

    -- Evita duplicados en el mismo rango de fechas
    CONSTRAINT uq_reservation UNIQUE (room_id, check_in, check_out)
);

-- 4. Pagos
CREATE TABLE payments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    reservation_id INT NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    payment_date DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    payment_method ENUM('cash','card','transfer') NOT NULL,
    payment_type ENUM('deposit','final','penalty') NOT NULL,
    status ENUM('pending', 'completed', 'failed', 'refunded') NOT NULL DEFAULT 'pending',
    card_last_four VARCHAR(4), -- Solo si es con tarjeta

    FOREIGN KEY (reservation_id) REFERENCES reservations(id) ON DELETE RESTRICT
) ENGINE=InnoDB;
