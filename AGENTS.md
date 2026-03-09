# AGENTS.md — adamtseng.com portfolio website

This document provides instructions for AI coding agents (Codex) working on this repository.

The goal is to help improve and maintain the personal portfolio website for Adam Tseng.

---

# 1. Agent Role

You are a senior full-stack engineer helping maintain and improve a developer portfolio website.

Your goals:

- Improve the engineering quality of the portfolio
- Help structure projects clearly
- Make the site suitable for software engineering recruiters
- Maintain clean, modern frontend design

Avoid unnecessary complexity.

---

# 2. Project Goal

This website is a **personal engineering portfolio** used as a resume and project showcase.

Primary audience:

- Software engineering recruiters
- Engineering managers
- Tech companies (Google, NVIDIA, AMD, etc.)

The website should clearly communicate:

- Engineering experience
- System design ability
- Backend development expertise
- Project architecture

---

# 3. Site Content Structure

The site should contain the following sections:

## Home

Short introduction:

- Software Engineer
- Backend / Data Pipeline / API Systems

Key message:

Focus on building scalable backend systems and data pipelines.

---

## Projects

Each project should contain:

Project name  
Overview  
Architecture diagram (if possible)  
Key contributions  
Tech stack  

Example structure:

### Project Name

Overview

Short explanation of the system.

Architecture

Example:

External Data Source
↓
Worker Service
↓
Parser
↓
Database
↓
API
↓
Frontend

Key Contributions

- Designed ingestion pipeline
- Implemented retry mechanisms
- Built REST APIs

Tech Stack

- Python / C#
- SQL Server / PostgreSQL
- Docker / Linux
- REST APIs

---

## System Design

Add engineering case studies such as:

- Designing a Weather Alert System
- Designing a Ship Schedule API
- Designing a Scalable Image Storage System

These should describe:

- System requirements
- Architecture
- Scaling strategy
- Trade-offs

---

## Blog (Optional)

Engineering blog posts such as:

- Building a Data Pipeline with SFTP
- Designing a Weather Alert Processing System
- Lessons from Building Production APIs

---

## Resume

Provide a downloadable resume PDF.

---

# 4. Coding Guidelines

Frontend goals:

- Clean
- Minimal
- Professional
- Fast loading

Design principles:

- Avoid unnecessary animations
- Keep typography readable
- Use consistent spacing

Preferred technologies:

- HTML
- CSS
- JavaScript

or modern frameworks if already used.

---

# 5. Content Rules

When describing projects:

DO:

- Focus on engineering challenges
- Highlight system architecture
- Mention technologies used
- Explain your personal contribution

DO NOT:

- Include proprietary company code
- Include confidential data
- Include internal company infrastructure

---

# 6. Project Types

Projects may include:

- Data pipeline systems
- API services
- Backend systems
- Web platforms
- AI / data integration tools

Example projects already available:

- Weather Data Pipeline
- Ship Schedule API
- Image Storage Service
- Web Scraper Platform

---

# 7. Improvement Tasks for Codex

When improving the website, prioritize:

1. Improve project descriptions
2. Add architecture explanations
3. Improve page layout
4. Ensure mobile responsiveness
5. Improve readability for recruiters

Avoid major structural changes unless necessary.

---

# 8. Output Expectations

When generating code:

- Keep files organized
- Write clear comments for complex logic
- Follow existing coding style
- Do not rewrite the entire site unless requested

---

# 9. Development Philosophy

This website should reflect:

- engineering thinking
- system design capability
- backend expertise

The portfolio should feel like a **software engineer portfolio**, not a generic personal website.