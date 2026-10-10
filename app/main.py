from fastapi import FastAPI
from pydantic import BaseModel
import os 
APP_NAME = os.getenv(
    "APP_NAME",
    "AI DevOps Incident Assistant"
)

APP_VERSION = os.getenv(
    "APP_VERSION",
    "0.1.0"
)
app = FastAPI(
    title = APP_NAME,
    description = "An AI-powered assistant for managing and resolving incidents in DevOps environments.",
    version = APP_VERSION
)

class Incident(BaseModel):
    application: str
    problem: str
    environment: str

@app.get("/")
def home():
    return {
        "message": "AI DevOps Incident Assistant is running."
       }
@app.get("/health")
def health():
    return {
        "status": "healthy"
    }

@app.post("/incident")
def create_incident(incident: Incident):
    return{
        "message": "Incident received",
        "incident": {
            "application": incident.application,
            "problem": incident.problem,
            "environment": incident.environment
        }
    }