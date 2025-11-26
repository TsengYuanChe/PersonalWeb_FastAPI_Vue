conda create -n fastapi-env python=3.11

conda activate fastapi-env

uvicorn main:app --reload --host 127.0.0.1 --port 8000