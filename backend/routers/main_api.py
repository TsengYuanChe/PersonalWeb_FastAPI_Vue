from fastapi import APIRouter
from datetime import datetime
import os, json

router = APIRouter()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

def read_json_with_timestamp(filename):
    filepath = os.path.join(DATA_DIR, filename)
    
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    last_modified = os.path.getmtime(filepath)
    updated_at = datetime.fromtimestamp(last_modified).strftime("%Y-%m-%d %H:%M:%S")
    return data, updated_at

def legacy_response(filename):
    data, updated_at = read_json_with_timestamp(filename)
    data["updated_at"] = updated_at
    return data

def v1_response(filename):
    data, updated_at = read_json_with_timestamp(filename)
    return {
        "data": data,
        "meta": {
            "updated_at": updated_at,
            "version": "v1",
        },
    }

@router.get("/api/about")
def about():
    return legacy_response("about.json")

@router.get("/api/experience")
def experience():
    return legacy_response("exp.json")

@router.get("/api/projects")
def projects():
    return legacy_response("projects.json")

@router.get("/api/v1/about")
def about_v1():
    return v1_response("about.json")

@router.get("/api/v1/experience")
def experience_v1():
    return v1_response("exp.json")

@router.get("/api/v1/projects")
def projects_v1():
    return v1_response("projects.json")
