import motor.motor_asyncio

# URL de conexión por defecto de MongoDB en local
MONGO_DETAILS = "mongodb://localhost:27017"

# Inicializamos el cliente asíncrono
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
database = client.practica2_db

# Referencias directas a las colecciones (equivalente a las tablas)
product_collection = database.get_collection("products")
user_collection = database.get_collection("users")