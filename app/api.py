from functools import lru_cache
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.core import Studio
from pathlib import Path as StaticPath
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Annotation Review Studio")


@lru_cache
def service():
    return Studio()


class AnnotationIn(BaseModel):
    annotator: str
    label: str


class DecisionIn(BaseModel):
    label: str
    reviewer: str
    reason: str


@app.get("/api/tasks")
def tasks():
    return service().tasks()


@app.post("/api/tasks/{tid}/annotations")
def annotate(tid: str, b: AnnotationIn):
    try:
        return service().annotate(tid, b.annotator, b.label)
    except ValueError as e:
        raise HTTPException(409, str(e)) from e


@app.post("/api/tasks/{tid}/decision")
def decide(tid: str, b: DecisionIn):
    try:
        return service().adjudicate(tid, b.label, b.reviewer, b.reason)
    except ValueError as e:
        raise HTTPException(409, str(e)) from e


@app.get("/api/export")
def export():
    return service().export()


# Serve the compiled React client after all API routes.

if StaticPath("web/dist").is_dir():
    app.mount("/", StaticFiles(directory="web/dist", html=True), name="web")
