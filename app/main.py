
from fastapi import FastAPI
from pydantic import BaseModel
import os

APP_NAME = os.getenv(
    "APP_NAME",
    "AI DevOps Incident Assistant"
)

APP_VERSION = os.getenv(
    "APP_VERSION",
    "0.2.0"
)

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

    if (
        "out of memory" in problem_lower
        or "oom" in problem_lower
    ):
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

    return {
        "message": "Incident analyzed",
        "incident": {
            "application": incident.application,
            "problem": incident.problem,
            "environment": incident.environment
        },
        "analysis": analysis
    }
