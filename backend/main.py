from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.main_api import router as main_router

app = FastAPI()

# 允許你的 Vue 前端連線（本機 + 部署）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # 若部署後要更安全，我可再幫你限定 domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 載入 API 路由
app.include_router(main_router)

@app.get("/")
def root():
    return {"msg": "FastAPI backend running!"}