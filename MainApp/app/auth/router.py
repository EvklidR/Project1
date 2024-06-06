from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi_users import exceptions
from starlette import status
from starlette.responses import HTMLResponse, RedirectResponse, JSONResponse

from app.auth.manager import get_user_manager

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

templates = Jinja2Templates(directory="presentation")


@router.get("/check-login")
async def check_login(login: str, user_manager=Depends(get_user_manager)):
    try:
        await user_manager.get_by_username(login)
        return JSONResponse(content={"exists": True})
    except exceptions.UserNotExists:
        return JSONResponse(content={"exists": False})


@router.get("/formlogin", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse(
        name="forms/auth/index.html", context={"request": request}
    )

@router.get("/formregister", response_class=HTMLResponse)
async def for_register(request: Request):
    return templates.TemplateResponse(
        name="forms/auth/reg.html", context={"request": request}
    )
