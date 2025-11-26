from fastapi import APIRouter

router = APIRouter()

@router.get("/api/index")
def index():
    return {
        "title": "Hi, I’m Tseng Yuan Che",
        "intro": "I’m a developer with a background in chemistry, now building full-stack web applications and exploring AI.",
        "desc": "I specialize in Python and Flask, and I’m passionate about creating efficient, elegant, and impactful software."
    }

@router.get("/api/about")
def about():
    return {
        "name": "Tseng Yuan Che",
        "role": "Software Developer",
        "description": "I build intelligent, efficient digital experiences with Python, Flask, and modern tools.",
        "skills": ["Python", "Flask", "Vue.js", "SQL", "AI"]
    }

@router.get("/api/projects")
def projects():
    return {
        "projects": [
            {
                "title": "AI Care Website",
                "description": "Flask-based AI-powered care system with OpenCV and health education integration."
            },
            {
                "title": "Financial Report Crawler",
                "description": "Crawler that automates financial report download from TWSE for analysts."
            },
            {
                "title": "yt_pod",
                "description": "Integration tool for collecting and summarizing YouTube + Podcast content."
            }
        ]
    }