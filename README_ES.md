 # 🌐 Idioma

- [**Inglés / English**](README.md)
- [Español](readme_es.md) (estás aquí)
---

 <h1 aling='center'>🏨 Sistema de Reservas API </h1>

API backend para una plataforma de gestión y reservas hoteleras desarrollada con **Django REST Framework**.  
El proyecto fue diseñado con mentalidad de entorno real, aplicando separación entre endpoints **públicos vs administrativos**, autenticación **JWT**, control de acceso por roles (**RBAC**), limitación de peticiones (**rate limiting**) y validación de reglas de negocio para reservas, disponibilidad y pagos.

## 🌍 Demo en Producción (Deploy en Render)

#### 📌 Documentación Swagger (API Docs)
https://sistema-de-reservas-4827.onrender.com/api/docs/

#### 📌 Documentación Redoc
https://sistema-de-reservas-4827.onrender.com/api/schema/redoc/

---

## 🚀 Tecnologías Usadas (Tech Stack)

- **Python**
- **Django**
- **Django REST Framework**
- **PostgreSQL**
- **JWT Authentication (SimpleJWT)**
- **drf-spectacular** (Swagger/OpenAPI Documentation)
- **django-filter** (Filtros avanzados)
- **DRF Throttling / Rate Limiting**
- **Deploy en Render**


## 🎯 Funcionalidades Principales

### 🛏️ Gestión de Habitaciones
- CRUD completo para habitaciones y tipos de habitación (solo admins).
- Endpoint de disponibilidad con validación real de solapamiento de fechas.
- Manejo de estados reales de habitaciones:
  - active
  - inactive
  - maintenance

### 📅 Sistema de Reservas
- Creación de reservas con cálculo automático del total.
- Prevención de reservas duplicadas (double booking).
- Ciclo de vida de la reserva:
  - confirmed
  - checked_in
  - cancelled
  - no_show
  - finished

### 💳 Sistema de Pagos
- Pagos asociados a reservas.
- Validación de reglas de negocio antes de registrar un pago.
- Control de saldo y pagos acumulados.

---

# 🧠 Arquitectura y Calidad de Código

El proyecto está estructurado siguiendo principios inspirados en **SOLID** y patrones reales de backend escalable.

### Separación clara de responsabilidades:
- **Serializers**: validación y serialización de datos.
- **ViewSets**: exposición de endpoints y control del flujo.
- **Services**: reglas de negocio desacopladas (ej: pagos).
- **Mixins**: reutilización de lógica compartida.
- **Filters**: filtros avanzados desacoplados del ViewSet.

Esto evita tener vistas sobrecargadas (“fat views”) y facilita mantenimiento y pruebas.

---

# 🔐 Seguridad y Buenas Prácticas

Este proyecto está diseñado con prácticas de seguridad similares a un entorno productivo.

## ✅ Autenticación (JWT)

Autenticación implementada con **JWT** usando SimpleJWT.  
Los endpoints administrativos requieren tokens válidos.

## ✅ Control de Acceso por Roles (RBAC)

Permisos personalizados para controlar acceso:

- `BaseUserPermission` (usuario autenticado y activo)
- `IsSuperUser`
- `IsReceptionist`

El rol recepcionista se maneja mediante **Django Groups**.

## ✅ Migración Automática para Grupo Receptionist

Se creó una migración que genera automáticamente el grupo `Receptionist`, garantizando consistencia en producción.

## ✅ Separación de Endpoints Públicos vs Administrativos

Decisión clave para evitar errores comunes de seguridad:  
los endpoints públicos NO exponen CRUD completo.

### Endpoints públicos:
- consulta de disponibilidad
- creación de reserva
- cancelación de reserva por token

### Endpoints administrativos:
- CRUD habitaciones
- CRUD tipos de habitación
- gestión de reservas
- gestión de pagos
- control de cambios de estado
- Control de usuarios (solo SuperUser)

Esto evita que un usuario externo pueda modificar o eliminar recursos sensibles.

## ✅ Transiciones Seguras de Estado (Status Flow Control)

El cambio de estado de una reserva se controla con un endpoint dedicado que valida transiciones permitidas:

- `confirmed → checked_in | cancelled | no_show`
- `checked_in → finished`

Cualquier transición inválida es rechazada, evitando inconsistencias en la base de datos.

## ✅ Protección Anti-Spam (Rate Limiting)

Los endpoints públicos de reservas incluyen **throttling / rate limiting** para prevenir abuso y spam.

Esto demuestra enfoque de seguridad y protección de recursos en un API real.

---

# 🧠 Lógica de Negocio y Consistencia

## ✅ Prevención de Double Booking

La disponibilidad de habitaciones se calcula usando lógica de solapamiento:

```
python
check_in__lt = requested_check_out
check_out__gt = requested_check_in
``` 

Esto evita que dos reservas ocupen la misma habitación en fechas cruzadas.

## ✅ Cálculo Financiero en Reservas (Propiedades Calculadas)

Las reservas incluyen propiedades calculadas:

- total_real = total_amount + extra_charges
- total_paid = suma de pagos asociados
- balance = saldo restante

Esto permite escenarios reales como minibar, daños, cargos extra, etc.

## ✅ Service Layer para Pagos

El módulo de pagos usa un service layer para validar reglas de negocio:

- no permite pagos en reservas finalizadas
- no permite montos inválidos
- no permite sobrepago por encima del balance

Esto mejora escalabilidad y limpieza del código.

## 🔍 Sistema de Filtros (Admin)

El listado de reservas en admin soporta filtros avanzados con django-filter:

- status
- room_id
- guest_document
- rango de fechas (con solapamiento real)

Ejemplo:
`GET /api/admin/reservations/?status=confirmed&room_id=10`

## 📍 Endpoints Principales

### API Pública

Disponibilidad de habitaciones  
`GET /api/public/rooms/available/?room_type=3&check_in=2026-03-28&check_out=2026-03-30`  
Crear reserva  
`POST /api/public/reservations/`  
Cancelar reserva (token-based)  
`PATCH /api/public/reservations/{token}/cancel/`

### API Administrativa (Protegida con JWT)

CRUD Habitaciones  
`/api/admin/rooms/`  
CRUD Tipos de habitación  
`/api/admin/roomtypes/`  
Gestión de Reservas  
`/api/admin/reservations/`  
Cambio de estado de reserva  
`PATCH /api/admin/reservations/{id}/change_status/`  
Pagos  
`/api/admin/payments/`

## 🔑 Autenticación (JWT)
Login  
`POST /api/auth/login/`

Body:
``` 
{
    "email": "admin@mail.com",
    "password": "password"
}
```

Response:
``` 
{
    "access": "...",
    "refresh": "..."
}
``` 

---

# 🛠️ Instalación Local
### Clonar proyecto
```
git clone <repo-url>
cd Sistema_de_Reservas
```

### Crear entorno virtual
```
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### Instalar dependencias
`pip install -r requirements.txt`

### Variables de entorno
Crear archivo .env:
```
DEBUG=True
SECRET_KEY=your_secret_key
DATABASE_URL=postgres://user:password@localhost:5432/dbname
```

### Migraciones
`python manage.py migrate`

### Ejecutar servidor
`python manage.py runserver`

---
## 📌 ¿Por qué este proyecto destaca?

Este proyecto NO es un CRUD básico.

Demuestra prácticas reales de ingeniería backend:

✅ JWT authentication y RBAC por roles  
✅ separación entre endpoints públicos y administrativos  
✅ throttling / rate limiting para evitar abuso  
✅ validación de transiciones de estado en reservas  
✅ prevención de double booking con queries de solapamiento  
✅ service layer para lógica de negocio (pagos)  
✅ arquitectura limpia inspirada en SOLID  
✅ documentación profesional Swagger + Redoc  
✅ deploy funcional en Render

---

## 📬 Autor

Desarrollado por Verónica sierra  
Backend Developer | Django & REST API

