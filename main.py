from fastapi import FastAPI
from routers import users, uploads, butterflies
from db import engine
import models as tables

print("App wird gestartet")
app = FastAPI()

tables.Base.metadata.create_all(bind=engine)

# Routen registrieren
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(uploads.router, prefix="/uploads", tags=["uploads"])
app.include_router(butterflies.router, prefix="/butterflies", tags=["butterflies"])