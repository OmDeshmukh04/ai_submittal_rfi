from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import health, upload

app = FastAPI(title="AI Submittal RFI Backend")

# Allow local frontend during development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api")
app.include_router(upload.router, prefix="/api/upload")

@app.get("/")
def root():
    return {"message": "AI Submittal RFI backend running"}
