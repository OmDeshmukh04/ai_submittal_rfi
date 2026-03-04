from fastapi import FastAPI
from api import health

app = FastAPI(title="AI Submittal RFI Backend")

app.include_router(health.router, prefix="/api")

@app.get("/")
def root():
    return {"message": "AI Submittal RFI backend running"}
