# Memoria de Uso de Inteligencia Artificial - Práctica 2 (Backend FastAPI)

## 1. Registro de Prompts y Estrategia de Desarrollo

El desarrollo de este backend se ha realizado utilizando asistencia de Inteligencia Artificial (Gemini) aplicando una metodología de desarrollo iterativo. En lugar de solicitar el código completo en un solo *prompt* (lo cual suele generar errores de arquitectura), se dividió el problema en fases secuenciales:

* **Fase 1: Estructura y Arquitectura Base:** Se solicitó la creación del esqueleto del proyecto en FastAPI separando responsabilidades (`main.py`, `routers/`, `repositories/`, `services/`).
* **Fase 2: Modelado y Base de Datos:** Se implementó la conexión a MongoDB. La decisión de utilizar Docker para levantar la infraestructura del backend y la base de datos permitió replicar el entorno original del profesor con exactitud, aislando el entorno y facilitando la depuración.
* **Fase 3: Autenticación y Seguridad:** Se requirió la implementación del registro de usuarios y el sistema de login para generar tokens JWT (`OAuth2PasswordRequestForm`).
* **Fase 4: Desarrollo del CRUD Protegido:** Se solicitaron los endpoints para el recurso de Productos y Usuarios, asegurando que todas las rutas verificaran la validez del token JWT mediante inyección de dependencias (`Depends`).
* **Fase 5: Adaptación de la Interfaz (Frontend):** Se solicitó ayuda para mapear la estructura de datos que enviaba Svelte (en español y formato JSON) a lo que esperaba recibir FastAPI (en inglés y formato *form-data* para el login), solucionando los problemas de CORS y puertos.

---

## 2. Análisis Crítico y Resolución de Problemas

Durante el desarrollo con la IA surgieron dos errores críticos derivados de la obsolescencia de librerías y cambios recientes en los *frameworks*. A continuación, se detalla el análisis y la solución de cada incidencia:

### Incidencia 1: Incompatibilidad de `passlib` con versiones modernas de `bcrypt`
* **El Error:** Al intentar registrar el primer usuario, el servidor devolvía un código `500 Internal Server Error`. El *Traceback* de la terminal mostraba: `AttributeError: module 'bcrypt' has no attribute '__about__'`.
* **Análisis:** La IA recomendó inicialmente utilizar la librería estándar `passlib[bcrypt]` para el *hashing* de contraseñas. Sin embargo, en el entorno con Python 3.11, la dependencia subyacente `bcrypt` se instaló en su versión 4.0+. Esta nueva versión elimina componentes internos (`__about__`) que la librería `passlib` (que lleva tiempo sin actualizarse) sigue intentando consumir, provocando una colisión fatal en tiempo de ejecución.
* **Solución Aplicada:** En lugar de forzar un *downgrade* de la librería a la versión 3.2.2 (lo cual es una mala práctica de seguridad a largo plazo), se optó por una refactorización arquitectónica. Se eliminó el intermediario `passlib` del archivo `auth_service.py` y se implementó el cifrado y verificación de contraseñas consumiendo directamente los métodos nativos de `bcrypt` (`bcrypt.hashpw` y `bcrypt.checkpw`).

### Incidencia 2: Pydantic V2 y la validación estricta de MongoDB (ObjectId)
* **El Error:** Tras solucionar el problema de cifrado, la base de datos registraba el usuario correctamente, pero FastAPI devolvía un error al intentar enviar la respuesta al cliente: `pydantic_core._pydantic_core.ValidationError: 1 validation error for UserDB... Input should be a valid string`.
* **Análisis:** El modelo de datos (`schemas.py`) propuesto inicialmente por la IA utilizaba una clase personalizada para transformar el `_id` de MongoDB. Dicha solución era válida para Pydantic V1. Sin embargo, FastAPI ahora utiliza Pydantic V2, que está programado en Rust y tiene un tipado extremadamente estricto. Al recibir un objeto de tipo `ObjectId` de la base de datos (BSON), el validador lo rechazaba porque esperaba estrictamente un tipo `str` nativo de Python.
* **Solución Aplicada:** Se modernizó el esquema utilizando las herramientas actuales de Pydantic V2. Se reemplazó la clase heredada por el uso de `Annotated` y `BeforeValidator`, instruyendo al modelo para que aplicara una conversión de tipos (cast a *string*) de forma automática antes de evaluar la validación estricta:
  `PyObjectId = Annotated[str, BeforeValidator(str)]`