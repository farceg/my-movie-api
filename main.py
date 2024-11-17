from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from config.database import Base, engine
from middlewares.error_handler import ErrorHandler
from routers.movie import movie_router
from routers.user import user_router


# Crear la instancia de FastAPI
app = FastAPI()
# Modificar el nombre que aparece en la documentación localhost:port/docs
app.title = "Mi aplicación con FastAPI"
# Modificar la versión que aparece en la documentación
app.version = "1.0"

# Middleware de la aplicación
app.add_middleware(ErrorHandler)

# Incluir routers para tener la aplicación seccionada
app.include_router(movie_router)
app.include_router(user_router)

# Crear la base de datos
Base.metadata.create_all(bind=engine)


# Ruta y nombre del método en la documentación
@app.get("/test", tags=["home"])
def message():
    return HTMLResponse("<h1>Hello World!</h1>")
