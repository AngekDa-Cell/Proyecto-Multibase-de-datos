# Guía de Instalación y Despliegue - Sistema de Agenda Corporativa Multibase

Esta guía te ayudará a instalar y desplegar el **Sistema de Agenda Corporativa Multibase** utilizando Docker y Docker Compose.

## Endpoints Implementados (7 Entidades)
- **Usuarios (PostgreSQL)**:
  - `GET /api/users` - Lista de usuarios activos.
  - `POST /api/users` - Crear usuario.
  - `PATCH /api/users/{user_id}` - Actualizar usuario parcialmente.
  - `DELETE /api/users/{user_id}` - Borrado lógico de usuario.
- **Departamentos (PostgreSQL)**:
  - `GET /api/departments` - Lista de departamentos activos.
  - `POST /api/departments` - Crear departamento.
  - `PATCH /api/departments/{dept_id}` - Actualizar departamento parcialmente.
  - `DELETE /api/departments/{dept_id}` - Borrado lógico de departamento.
- **Roles (PostgreSQL)**:
  - `GET /api/roles` - Lista de roles activos.
  - `POST /api/roles` - Crear rol.
  - `PATCH /api/roles/{role_id}` - Actualizar rol parcialmente.
  - `DELETE /api/roles/{role_id}` - Borrado lógico de rol.
- **Contactos (MongoDB)**:
  - `GET /api/contacts` - Lista de contactos activos.
  - `POST /api/contacts` - Crear contacto.
  - `PATCH /api/contacts/{contact_id}` - Actualizar contacto parcialmente.
  - `DELETE /api/contacts/{contact_id}` - Borrado lógico de contacto.
- **Eventos (MongoDB)**:
  - `GET /api/events` - Lista de eventos activos.
  - `POST /api/events` - Crear evento.
  - `PATCH /api/events/{event_id}` - Actualizar evento parcialmente.
  - `DELETE /api/events/{event_id}` - Borrado lógico de evento.
- **Configuraciones (Redis)**:
  - `GET /api/config/{key}` - Obtener configuración activa.
  - `POST /api/config` - Crear configuración.
  - `PATCH /api/config/{key}` - Actualizar configuración parcialmente.
  - `DELETE /api/config/{key}` - Borrado lógico de configuración.
- **Sesiones de Usuario (Redis)**:
  - `GET /api/sessions/{user_id}` - Obtener sesión activa.
  - `POST /api/sessions` - Crear sesión.
  - `PATCH /api/sessions/{user_id}` - Actualizar sesión parcialmente.
  - `DELETE /api/sessions/{user_id}` - Borrado lógico de sesión.

**Nota**: Todos los endpoints implementan borrado lógico (soft delete) y filtran registros inactivos en GET. La API está disponible en `http://localhost:8000` con documentación en `/docs`.

## Prerrequisitos

Antes de comenzar, asegúrate de tener instalados los siguientes componentes en tu sistema:

- **Docker**: Versión 20.10 o superior. Descárgalo desde [docker.com](https://www.docker.com/).
- **Docker Compose**: Generalmente incluido con Docker Desktop. Versión 2.0 o superior.
- **Git**: Para clonar el repositorio (opcional, si no tienes el código localmente).

Verifica las versiones instaladas:
```bash
docker --version
docker-compose --version
```

## Instalación y Despliegue

### Paso 1: Clonar o Navegar al Repositorio

Si no tienes el código localmente, clónalo desde GitHub:
```bash
git clone https://github.com/AngekDa-Cell/Proyecto-Multibase-de-datos.git
cd Proyecto-Multibase-de-datos
```

Si ya tienes el código, navega al directorio del proyecto:
```bash
cd "Tu Ruta del Repositorio"
```

### Paso 2: Construir y Levantar los Servicios

Ejecuta el siguiente comando para construir las imágenes y levantar todos los contenedores (bases de datos y API):
```bash
docker-compose up --build
```

Este comando:
- Construirá la imagen de la aplicación Python (`api_app`).
- Levantará los contenedores para PostgreSQL, MongoDB y Redis.
- Esperará a que las bases de datos estén listas antes de iniciar la API.
- La API estará disponible en `http://localhost:8000`.

**Nota**: La primera ejecución puede tomar varios minutos debido a la descarga de imágenes y construcción.

### Paso 3: Verificar el Despliegue

Una vez que todos los contenedores estén ejecutándose, verifica que todo funcione correctamente:

1. **Verifica los contenedores en ejecución**:
   ```bash
   docker-compose ps
   ```
   Deberías ver 4 contenedores: `postgres_agenda`, `mongo_agenda`, `redis_agenda` y `api_agenda`.

2. **Accede a la API**:
   Abre tu navegador y ve a `http://localhost:8000/docs` para ver la documentación interactiva de FastAPI (Swagger UI).

3. **Prueba un endpoint**:
   - GET `http://localhost:8000/users/` (debería devolver una lista vacía inicialmente).
   - POST `http://localhost:8000/users/` con body JSON: `{"name": "Juan Pérez", "email": "juan@example.com"}`.
   - GET `http://localhost:8000/contacts/` (lista de contactos).
   - POST `http://localhost:8000/contacts/` con body JSON: `{"name": "María García", "phone": "123456789"}`.
   - GET `http://localhost:8000/config/test_key` (después de crear una configuración).

### Paso 4: Detener los Servicios

Para detener todos los servicios:
```bash
docker-compose down
```

Para detener y eliminar volúmenes (borrar datos persistentes):
```bash
docker-compose down -v
```

## Estructura del Proyecto

```
Proyecto-Multibase-de-datos/
├── .env                  # Variables de entorno para desarrollo local
├── docker-compose.yml    # Configuración de servicios Docker
├── Dockerfile            # Imagen de la aplicación Python
├── requirements.txt      # Dependencias Python
├── instrucciones.md      # Documento con especificaciones del proyecto
├── README.md             # Guía de instalación
└── app/
    ├── main.py           # Punto de entrada de FastAPI
    ├── models.py         # Modelos SQLAlchemy para PostgreSQL
    ├── schemas.py        # Esquemas Pydantic para validación
    ├── __init__.py       # Paquete Python
    ├── routers/
    │   ├── __init__.py   # Paquete routers
    │   ├── postgres.py   # Endpoints PostgreSQL (Users, Departments, Roles)
    │   ├── mongo.py      # Endpoints MongoDB (Contacts, Events)
    │   └── redis.py      # Endpoints Redis (AppConfig, UserSessions)
    └── database/
        ├── postgres.py   # Configuración PostgreSQL
        ├── mongo.py      # Configuración MongoDB
        └── redis.py      # Configuración Redis
```

## Tecnologías Utilizadas

- **Python 3.11**: Lenguaje de programación.
- **FastAPI**: Framework para la API REST.
- **PostgreSQL**: Base de datos relacional.
- **MongoDB**: Base de datos NoSQL documental.
- **Redis**: Base de datos clave-valor.
- **Docker & Docker Compose**: Contenerización y orquestación.

## Solución de Problemas

### Error: "docker-compose command not found"
- Instala Docker Desktop desde [docker.com](https://www.docker.com/products/docker-desktop).
- En Windows, asegúrate de que Docker esté ejecutándose.

### Error: Puerto 8000 ya en uso
- Cambia el puerto en `docker-compose.yml` (línea `ports: - "8000:8000"`).
- O detén el proceso que usa el puerto 8000.

### Error de conexión a bases de datos
- Verifica que los contenedores de BD estén ejecutándose: `docker-compose ps`.
- Revisa logs: `docker-compose logs postgres_db` (o el servicio correspondiente).

### La API no responde
- Espera a que los healthchecks de las BD pasen (puede tomar 30-60 segundos).
- Revisa logs de la API: `docker-compose logs api_app`.
