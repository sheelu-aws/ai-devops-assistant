
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime, timezone
from pathlib import Path
import json
import os
import threading
import uuid

APP_NAME = os.getenv(
    "APP_NAME",
    "AI DevOps Incident Assistant"
)

APP_VERSION = os.getenv(
    "APP_VERSION",
    "0.3.0"
)

DATA_DIR = Path(os.getenv("DATA_DIR", "/app/data"))
INCIDENTS_FILE = DATA_DIR / "incidents.json"
storage_lock = threading.Lock()

app = FastAPI(
    title=APP_NAME,
    description=(
        "An AI-powered assistant for managing "
        "and resolving DevOps incidents."
    ),
    version=APP_VERSION
)


class Incident(BaseModel):
    application: str
    problem: str
    environment: str


def load_incidents():
    if not INCIDENTS_FILE.exists():
        return []

    try:
        with INCIDENTS_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, list):
            raise ValueError("Incident history must be a JSON list.")

        return data

    except (OSError, json.JSONDecodeError, ValueError) as exc:
        raise HTTPException(
            status_code=500,
            detail="Unable to read incident history."
        ) from exc


def save_incidents(incidents):
    try:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        temporary_file = INCIDENTS_FILE.with_suffix(".tmp")

        with temporary_file.open("w", encoding="utf-8") as file:
            json.dump(incidents, file, indent=2)
            file.flush()
            os.fsync(file.fileno())

        temporary_file.replace(INCIDENTS_FILE)

    except OSError as exc:
        raise HTTPException(
            status_code=500,
            detail="Unable to save incident history."
        ) from exc


def analyze_incident(problem: str):
    problem_lower = problem.lower()

    if "502" in problem_lower or "bad gateway" in problem_lower:
        return {
            "category": "Gateway Error",
            "possible_causes": [
                "Backend service is unavailable",
                "Application is returning errors",
                "Proxy or ingress configuration issue"
            ],
            "recommended_actions": [
                "Check application Pod status",
                "Review application logs",
                "Verify Service endpoints and ports",
                "Check Ingress or proxy configuration"
            ]
        }

    if "cpu" in problem_lower or "high load" in problem_lower:
        return {
            "category": "High CPU",
            "possible_causes": [
                "Heavy application workload",
                "Inefficient code or repeated requests",
                "Insufficient CPU resources"
            ],
            "recommended_actions": [
                "Check kubectl top pods",
                "Review application metrics and logs",
                "Inspect CPU requests and limits",
                "Check HPA scaling status"
            ]
        }

    if "out of memory" in problem_lower or "oom" in problem_lower:
        return {
            "category": "Memory Issue",
            "possible_causes": [
                "Application memory usage is too high",
                "Container memory limit was exceeded"
            ],
            "recommended_actions": [
                "Check Pod restart counts",
                "Inspect Pod events",
                "Review memory usage and limits",
                "Investigate possible memory leaks"
            ]
        }

    return {
        "category": "Unknown Incident",
        "possible_causes": [
            "The problem needs further investigation"
        ],
        "recommended_actions": [
            "Review application logs",
            "Check Pod status and events",
            "Inspect service and resource metrics"
        ]
    }


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
    analysis = analyze_incident(incident.problem)

    with storage_lock:
        incidents = load_incidents()

        record = {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "application": incident.application,
            "problem": incident.problem,
            "environment": incident.environment,
            "analysis": analysis
        }

        incidents.append(record)
        save_incidents(incidents)

    return {
        "message": "Incident analyzed and saved",
        "incident": record
    }



@app.get("/incidents")
def get_incidents(
    environment: str | None = None,
    category: str | None = None
):
    with storage_lock:
        incidents = load_incidents()

    if environment:
        incidents = [
            incident for incident in incidents
            if incident["environment"].lower() == environment.lower()
        ]

    if category:
        incidents = [
            incident for incident in incidents
            if incident["analysis"]["category"].lower() == category.lower()
        ]

    return {
        "count": len(incidents),
        "incidents": incidents
    }

@app.get("/incidents/summary")
def get_incident_summary():
    with storage_lock:
        incidents = load_incidents()

    category_counts = {}
    environment_counts = {}

    for incident in incidents:
        category = incident["analysis"]["category"]
        environment = incident["environment"]

        category_counts[category] = category_counts.get(category, 0) + 1

        environment = environment.lower()
        environment_counts[environment] = (
            environment_counts.get(environment, 0) + 1
        )

    production_count = sum(
        1 for incident in incidents
        if incident["environment"].lower() == "production"
    )

    return {
        "total_incidents": len(incidents),
        "production_incidents": production_count,
        "by_category": category_counts,
        "by_environment": environment_counts
    }
