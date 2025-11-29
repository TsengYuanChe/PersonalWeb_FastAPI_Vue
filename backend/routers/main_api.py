from fastapi import APIRouter
from datetime import datetime
import os, json

router = APIRouter()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

def load_json(filename):
    filepath = os.path.join(DATA_DIR, filename)
    
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    last_modified = os.path.getmtime(filepath)
    updated_at = datetime.fromtimestamp(last_modified).strftime("%Y-%m-%d %H:%M:%S")
    
    data["updated_at"] = updated_at
    return data 

@router.get("/api/about")
def about():
    return load_json("about.json")

@router.get("/api/experience")
def experience():
    return load_json("exp.json")

@router.get("/api/projects")
def projects():
    return load_json("projects.json")