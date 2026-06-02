# Práctica 2 Programación Web 2

El sistema permite la gestión (CRUD) de productos y usuarios mediante un panel de administración protegido por autenticación basada en tokens JWT.

---

## Tecnologías Utilizadas

* **Frontend:** Svelte 5 (Vite), recogiendo el de la practica 1
* **Backend:** FastAPI (Python 3.11+)
* **Base de Datos:** MongoDB
* **Infraestructura:** Docker (para la virtualización de la base de datos)
* **Seguridad:** JWT (JSON Web Tokens) y cifrado de contraseñas con `bcrypt` nativo.

---

## Requisitos Previos

Asegúrate de tener instalados los siguientes programas antes de ejecutar el proyecto:
* [Node.js](https://nodejs.org/) y npm (para el frontend)
* [Python 3.11+](https://www.python.org/) (para el backend)
* [Docker Desktop](https://www.docker.com/products/docker-desktop/) (para la base de datos MongoDB)

---

## Instrucciones de Instalación y Ejecución

El proyecto está dividido en tres capas que deben ejecutarse en el siguiente orden:

### 1. Base de Datos (MongoDB con Docker)
La base de datos se ejecuta dentro de un contenedor Docker para aislar el entorno.
1. Abre una terminal.
2. Levanta el contenedor utilizando el archivo de configuración proporcionado (o ejecutando la imagen de MongoDB). 
3. Asegúrate de que MongoDB está corriendo en el puerto por defecto (`27017`).

### 2. Backend (FastAPI)
1. Abre una nueva terminal y navega a la carpeta del backend.
2. (Opcional pero recomendado) Crea y activa un entorno virtual:
   ```bash
   python -m venv venv
   # En Windows:
   .\venv\Scripts\activate
   # En Mac/Linux:
   source venv/bin/activate

Instala las dependencias necesarias:

```bash
pip install fastapi uvicorn pymongo pydantic bcrypt pyjwt
```

Levanta el servidor en modo desarrollo:

```bash
uvicorn main:app --reload
```

El backend estará disponible en: `http://localhost:8000`
La documentación interactiva (Swagger UI) está en: `http://localhost:8000/docs`

### 3. Frontend (Svelte)
Abre una nueva terminal y navega a la carpeta del frontend.

Instala las dependencias de Node:

```bash
npm install
```

Arranca el servidor de desarrollo:

```bash
npm run dev
```

El frontend estará disponible en: `http://localhost:5173` (o el puerto que indique Vite en la consola).

   ## 🗺️ Mapa de la API (Endpoints)

El backend expone los siguientes endpoints, divididos por recursos. Todas las rutas (excepto el System, Register y Login) están protegidas y requieren un token JWT válido en la cabecera `Authorization`.

### 🛡️ Autenticación (`/api`)
* `POST /api/register`: Registra un nuevo usuario en la base de datos (encriptando su contraseña).
* `POST /api/login`: Recibe credenciales y devuelve un token de acceso JWT (`access_token`).

### 📦 Productos (`/api/productos`)
* `GET /api/productos`: Lista todos los productos disponibles.
* `POST /api/productos`: Crea un nuevo producto.
* `PUT /api/productos/{id}`: Actualiza la información de un producto existente.
* `DELETE /api/productos/{id}`: Elimina un producto.

### 👥 Usuarios (`/api/users`)
* `GET /api/users`: Lista todos los usuarios registrados.
* `PUT /api/users/{id}`: Actualiza los datos de un usuario.
* `DELETE /api/users/{id}`: Elimina a un usuario del sistema.

### 🩺 Sistema (`/health`)
* `GET /health`: Comprueba el estado del servidor y la conexión activa con MongoDB (Health Check).

---

## 🔒 Estructura y Seguridad Aplicada

* **Arquitectura en capas:** El backend sigue el patrón repositorio (`routers` -> `services` -> `repositories`), aislando la lógica de base de datos de las peticiones HTTP.
* **Manejo Global de Excepciones:** Se interceptan errores 500 y errores de validación de Pydantic (422) para devolver respuestas JSON limpias sin colapsar el servidor.
* **Tipado Estricto:** Pydantic V2 garantiza que todos los datos de entrada y salida cumplen con las estructuras esperadas antes de interactuar con MongoDB.
* **CORS Configurado:** El backend permite peticiones externas de forma segura para comunicarse sin bloqueos con Svelte.
