from pydantic import BaseModel

# Datos del usuario para iniciar sesión
class User(BaseModel):
    email: str
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "admin@gmail.com",
                "password": "admin",
            }
        }