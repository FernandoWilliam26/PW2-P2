from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from repositories.schemas import UserCreate, UserDB
from repositories.user_repository import UserRepository
from services.auth_service import verify_password, create_access_token

router = APIRouter()

@router.post("/register", response_model=UserDB, status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate):
    existing_user = await UserRepository.get_user_by_username(user.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El nombre de usuario ya está registrado"
        )
    
    new_user = await UserRepository.create_user(user)
    return new_user

# --- NUEVA RUTA DE LOGIN ---
@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # 1. Buscamos al usuario en la base de datos
    user = await UserRepository.get_user_by_username(form_data.username)
    
    # 2. Comprobamos si existe y si la contraseña coincide (usando nuestra función con bcrypt nativo)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 3. Generamos el token JWT metiendo el nombre de usuario y su rol dentro
    access_token = create_access_token(
        data={"sub": user["username"], "role": user["role"]}
    )
    
    # 4. Devolvemos el token en el formato estándar que espera FastAPI y Svelte
    return {"access_token": access_token, "token_type": "bearer"}