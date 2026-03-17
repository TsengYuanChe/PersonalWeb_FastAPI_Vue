import logging

from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from routers.v1 import content, health
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI()
logger = logging.getLogger(__name__)

# 允許你的 Vue 前端連線（本機 + 部署）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # 若部署後要更安全，我可再幫你限定 domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 載入 API 路由
app.include_router(content.router)
app.include_router(health.router)


@app.exception_handler(FileNotFoundError)
async def file_not_found_handler(request: Request, exc: FileNotFoundError):
    logger.warning("content_not_found", extra={"path": request.url.path})
    return JSONResponse(
        status_code=404,
        content={
            "error": {
                "code": "CONTENT_NOT_FOUND",
                "message": str(exc),
                "details": None,
            }
        },
    )


@app.exception_handler(HTTPException)
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: Exception):
    status_code = getattr(exc, "status_code", 500)
    detail = getattr(exc, "detail", "HTTP error")
    code = "NOT_FOUND" if status_code == 404 else f"HTTP_{status_code}"

    logger.warning("http_error", extra={"path": request.url.path, "status_code": status_code})
    return JSONResponse(
        status_code=status_code,
        content={
            "error": {
                "code": code,
                "message": str(detail),
                "details": None,
            }
        },
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.exception("internal_error", extra={"path": request.url.path})
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "Internal server error",
                "details": None,
            }
        },
    )


@app.get("/")
def root():
    return {"msg": "FastAPI backend running!"}
