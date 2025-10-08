from fastapi import FastAPI
from routers import users  
from db import engine
import models as tables

print("App wird gestartet")
app = FastAPI()

tables.Base.metadata.create_all(bind=engine)

# Routen registrieren
app.include_router(users.router, prefix="/users", tags=["users"])