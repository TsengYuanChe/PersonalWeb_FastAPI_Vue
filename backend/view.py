from flask import Blueprint, jsonify

main_views = Blueprint('main_views', __name__)

@main_views.route('/api/index')
def index():
    return jsonify({
        "title": "Hi, I’m Tseng Yuan Che",
        "intro": "I’m a developer with a background in chemistry, now building full-stack web applications and exploring AI.",
        "desc": "I specialize in Python and Flask, and I’m passionate about creating efficient, elegant, and impactful software."
    })

@main_views.route('/api/about')
def about():
    return jsonify({
        "name": "Tseng Yuan Che",
        "role": "Software Developer",
        "description": "I build intelligent, efficient digital experiences with Python, Flask, and modern tools.",
        "skills": ["Python", "Flask", "Vue.js", "SQL", "AI"]
    })

@main_views.route('/api/projects')
def projects():
    return jsonify({
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
    })