import httpx
from fastapi import FastAPI, HTTPException, Depends
from fastapi_users import FastAPIUsers
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, RedirectResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from app.auth.auth import auth_backend
from app.auth.manager import get_user_manager
from app.auth.models import User
from app.auth.router import router as auth_router
from app.auth.schemas import UserRead, UserCreate
from app.companyData.router import router as prod_router
from model.core import router as core_router

from fastapi.responses import FileResponse

app = FastAPI()


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app.mount("/static", StaticFiles(directory="presentation"), name="static")
templates = Jinja2Templates(directory="presentation")

app.include_router(auth_router)
app.include_router(prod_router)
app.include_router(core_router)

current_user = fastapi_users.current_user()


@app.get("/predict")
async def get_prediction(product_id: int):
    url = "http://127.0.0.1:8080/predict/" + str(product_id)

    async with httpx.AsyncClient() as client:
        response = await client.get(url, timeout=60.0)
        return response.json()


@app.get("/")
async def prod_table(request: Request, user: User = Depends(current_user)):
    return RedirectResponse(url=request.app.url_path_for("prod_table"))


app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)


@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    # Переопределите обработчик ошибок HTTPException по своему усмотрению
    # Возможно, вам потребуется вернуть свой собственный ответ или выполнить перенаправление
    if exc.status_code == 401:
        return RedirectResponse(url="/auth/formlogin")
    else:
        return JSONResponse(
            status_code=exc.status_code,
            content={"message": exc.detail}
        )
