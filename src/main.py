import uvicorn
from fastapi import FastAPI
from src.controllers.api_controllers import router

app = FastAPI(title="Système Distributeur PFE")

# Inclure toutes les routes définies dans le contrôleur
app.include_router(router, prefix="/api")

@app.get("/")
def home():
    return {"message": "Serveur opérationnel"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)