

from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi_users import FastAPIUsers
from starlette import status
from starlette.responses import HTMLResponse, RedirectResponse, StreamingResponse

from app.auth.auth import auth_backend
from app.auth.manager import get_user_manager
from app.auth.models import User
from app.companyData.models import Product
from model.CRUD import AbstractEntityRepository, EntityRepository

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

router = APIRouter(
    prefix="/company",
    tags=["Products"]
)

templates = Jinja2Templates(directory="presentation")

current_user = fastapi_users.current_user()


@router.get("/company")
async def prod_table(request: Request, user: User = Depends(current_user)):
    if user.idCompany:
        return templates.TemplateResponse(
            name="products/products.html",
            context={"request": request,
                     "login": user.login,
                     "status": user.isOwner}
        )
    else:
        return RedirectResponse(url=request.app.url_path_for("add_company"), status_code=status.HTTP_302_FOUND)


@router.get("/addCompany")
async def add_company(request: Request, user: User = Depends(current_user)):
    return templates.TemplateResponse(
        name="forms/formcompany/formcompany.html", context={"request": request,
                                                            "login": user.login,
                                                            "status": user.isOwner}
    )


@router.get("/stores")
async def stores_table(request: Request, user: User = Depends(current_user)):
    return templates.TemplateResponse(
        name="stores/stores.html",
        context={"request": request,
                 "login": user.login,
                 "status": user.isOwner}
    )


@router.get("/info")
async def prod_info(request: Request, id: int,
                    user: User = Depends(current_user),
                    entity_repo: AbstractEntityRepository = Depends(EntityRepository)
                    ):
    product = await entity_repo.get_entity(entity_type=Product, entity_id=id)
    return templates.TemplateResponse(
        name="prod/prod.html", context={"request": request,
                                        'product': product,
                                        "login": user.login,
                                        "status": user.isOwner}
    )


@router.get("/addProd", response_class=HTMLResponse)
async def add_product(request: Request, user: User = Depends(current_user)):
    return templates.TemplateResponse(
        name="forms/formProduct/form.html", context={"request": request,
                                                     "login": user.login,
                                                     "status": user.isOwner}
    )


@router.get("/upProd", response_class=HTMLResponse, name="update_product")
async def update_product(request: Request, id: int,
                         user: User = Depends(current_user),
                         entity_repo: AbstractEntityRepository = Depends(EntityRepository)
                         ):
    product = await entity_repo.get_entity(entity_type=Product, entity_id=id)
    return templates.TemplateResponse(
        name="forms/formupdateproduct/form.html", context={"request": request,
                                                           "product": product,
                                                           "login": user.login,
                                                           "status": user.isOwner}
    )


@router.get("/addSale", response_class=HTMLResponse)
async def add_sale(request: Request, user: User = Depends(current_user)):
    return templates.TemplateResponse(
        name="forms/formSale/form.html", context={"request": request,
                                                  "login": user.login,
                                                  "status": user.isOwner}
    )


@router.get("/addBuy", response_class=HTMLResponse)
async def add_buy(request: Request, user: User = Depends(current_user)):
    return templates.TemplateResponse(
        name="forms/formbuy/form.html", context={"request": request,
                                                 "login": user.login,
                                                 "status": user.isOwner}
    )


@router.get("/addStore", response_class=HTMLResponse)
async def add_store(request: Request, user: User = Depends(current_user)):
    return templates.TemplateResponse(
        name="forms/formstore/formstore.html", context={"request": request,
                                                        "login": user.login,
                                                        "status": user.isOwner}
    )


@router.get("/addUser", response_class=HTMLResponse)
async def add_user(request: Request, user: User = Depends(current_user)):
    return templates.TemplateResponse(
        name="forms/formworker/form.html", context={"request": request,
                                                    "login": user.login,
                                                    "status": user.isOwner}
    )


@router.get("/sales")
async def sales_table(request: Request, user: User = Depends(current_user)):
    return templates.TemplateResponse(
        name="operations/sale/sale.html",
        context={"request": request,
                 "login": user.login,
                 "status": user.isOwner}
    )


@router.get("/buy")
async def buy_table(request: Request, user: User = Depends(current_user)):
    return templates.TemplateResponse(
        name="operations/buy/buy.html",
        context={"request": request,
                 "login": user.login,
                 "status": user.isOwner}
    )


@router.get("/abc")
async def abc_table(request: Request, user: User = Depends(current_user)):
    return templates.TemplateResponse(
        name="abc/products.html",
        context={"request": request,
                 "login": user.login,
                 "status": user.isOwner}
    )


@router.get("/users")
async def users_table(request: Request, user: User = Depends(current_user)):
    return templates.TemplateResponse(
        name="workers/workers.html",
        context={"request": request,
                 "login": user.login,
                 "status": user.isOwner}
    )


@router.get("/displacement")
async def displacement_table(request: Request, user: User = Depends(current_user)):
    return templates.TemplateResponse(
        name="operations/displacement/displacement.html",
        context={"request": request,
                 "login": user.login,
                 "status": user.isOwner}
    )


@router.get("/return")
async def return_table(request: Request, user: User = Depends(current_user)):
    return templates.TemplateResponse(
        name="operations/return/return.html",
        context={"request": request,
                 "login": user.login,
                 "status": user.isOwner}
    )


@router.get("/report")
async def report(request: Request, user: User = Depends(current_user)):
    return templates.TemplateResponse(
        name="report/report.html",
        context={"request": request,
                 "login": user.login,
                 "status": user.isOwner}
    )


# @router.get("/inventory")
# async def inventory_table(request: Request, user: User = Depends(current_user)):
#     return templates.TemplateResponse(
#         name="operations/inventory/inventory.html",
#         context={"request": request,
#                  "login": user.login,
#                  "status": user.isOwner}
#     )
