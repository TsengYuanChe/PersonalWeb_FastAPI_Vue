conda create -n fastapi-env python=3.11

conda activate fastapi-env

uvicorn main:app --reload --host 127.0.0.1 --port 8000

# Test docker file

docker build --platform linux/amd64 -t vue-frontend .

docker run -p 8080:8080 vue-frontend

## 建立 Artifact Registry repository

Artifact Registry → Repositories → 建立 repository

Repository name：frontend

Format：Docker

Location type：Region

Region：asia-east1

Mode：Standard

按 Create

## Push to google cloud

gcloud auth login

gcloud config set project personal-website-479501

gcloud auth configure-docker asia-east1-docker.pkg.dev

docker tag vue-frontend asia-east1-docker.pkg.dev/personal-website-479501/frontend/vue-frontend

docker push asia-east1-docker.pkg.dev/personal-website-479501/frontend/vue-frontend

# Deploy steps

https://console.cloud.google.com/run/overview?project=personal-website-479501

->部署容器（Deploy container）
