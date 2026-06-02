from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware 
from routers import auth, products, users
from repositories.database import client 

app = FastAPI(title="Backend Práctica 2")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "error": "Datos inválidos", 
            "detalle": exc.errors() 
        },
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Error Interno del Servidor",
            "detalle": "Ha ocurrido un problema inesperado. Revisa la consola."
        }
    )

app.include_router(auth.router, prefix="/api", tags=["Auth"])
app.include_router(products.router, prefix="/api/products", tags=["Products"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])

@app.get("/")
def root():
    return {"message": "API en FastAPI funcionando correctamente"}

@app.get("/health", tags=["System"])
async def check_db_connection():
    try:
        await client.admin.command('ping')
        return {"status": "online", "database": "MongoDB", "message": "¡Conexión a la base de datos exitosa! 🚀"}
    except Exception as e:
        return {"status": "offline", "database": "MongoDB", "message": f"Error de conexión: {str(e)}"}