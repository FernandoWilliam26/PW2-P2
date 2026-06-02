from pydantic import BaseModel, Field, ConfigDict, BeforeValidator
from typing import Optional, Annotated

PyObjectId = Annotated[str, BeforeValidator(str)]

class ProductBase(BaseModel):
    name: str
    description: str
    price: float

class ProductDB(ProductBase):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )

class UserCreate(BaseModel):
    username: str
    password: str
    role: str = "usuario"  

class UserDB(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    username: str
    role: str
    
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )