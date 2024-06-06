from datetime import datetime

from fastapi_users import FastAPIUsers
from starlette.responses import JSONResponse

from fastapi import APIRouter, HTTPException, Depends

from app.auth.auth import auth_backend
from app.auth.manager import get_user_manager, UserManager
from model import CRUD

import app.companyData.models as prodModels
import app.auth.models as authModels

from app.auth import schemas as authSchemas
from app.companyData import schemas as companySchemas

from model.CRUD import EntityRepository, AbstractEntityRepository
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
import httpx

router = APIRouter(
    prefix="/db",
    tags=["db"]
)

fastapi_users = FastAPIUsers[authModels.User, int](
    get_user_manager,
    [auth_backend],
)
current_user = fastapi_users.current_user()


@router.get("/users/", status_code=200)
async def read_users(skip: int = 0, limit: int = 100, search_query: str = "",
                     user: authModels.User = Depends(current_user),
                     entity_repo: AbstractEntityRepository = Depends(EntityRepository)):
    return await entity_repo.get_entities(entity_class=authModels.User, idCompany=user.idCompany, skip=skip,
                                          limit=limit, search_query=search_query)


@router.post("/users/")
async def create_user(user: authSchemas.UserCreate,
                      cur_user: authModels.User = Depends(current_user)):

    user.idCompany = cur_user.idCompany

    # Отправка данных пользователя на адрес /auth/register
    async with httpx.AsyncClient() as client:
        response = await client.post("http://127.0.0.1:8000/auth/register", json=user.model_dump())

    if response.status_code == 201:
        return JSONResponse(content="user was successfully added", status_code=201)
    else:
        raise HTTPException(status_code=response.status_code, detail="Error registering user")


@router.patch("/users/")
async def update_user(
    user: authSchemas.UserUpdate,
    cur_user: authModels.User = Depends(current_user),
    entity_repo: AbstractEntityRepository = Depends(EntityRepository),
    user_manager: UserManager = Depends(get_user_manager)):

    user.idCompany = cur_user.idCompany

    await entity_repo.update_entity(entity_class=authModels.User, entity_data=user.model_dump())
    if user.password:
        await user_manager.reset_password_for_user(user.id, user.password)
    return JSONResponse(content="user was successfully updated")


@router.delete("/users/", status_code=204)
async def delete_user(user_id: int,
                      user: authModels.User = Depends(current_user),
                      entity_repo: AbstractEntityRepository = Depends(EntityRepository)
                      ):
    if not await entity_repo.delete_entity(entity_type=authModels.User, entity_id=user_id):
        return JSONResponse(status_code=404, content="there is no such user")


@router.get("/stores/", status_code=200)
async def read_stores(skip: int = 0, limit: int = 100, search_query: str = "",
                      user: authModels.User = Depends(current_user),
                      entity_repo: AbstractEntityRepository = Depends(EntityRepository)
                      ):
    return await entity_repo.get_entities(search_query=search_query, entity_class=prodModels.Store,
                                          idCompany=user.idCompany, skip=skip,
                                          limit=limit)


@router.post("/stores/")
async def create_store(store: companySchemas.StoreCreate,
                       user: authModels.User = Depends(current_user),
                       entity_repo: AbstractEntityRepository = Depends(EntityRepository)
                       ):
    store.idCompany = user.idCompany
    await entity_repo.create_entity(entity_class=prodModels.Store, entity_data=store.model_dump())
    return JSONResponse(content="store was successfully added", status_code=201)

@router.patch("/stores/")
async def update_store(store: companySchemas.StoreUpdate,
                      user: authModels.User = Depends(current_user),
                      entity_repo: AbstractEntityRepository = Depends(EntityRepository)
                      ):
    store.idCompany = user.idCompany
    await entity_repo.update_entity(entity_class=prodModels.Store, entity_data=store.model_dump())
    return JSONResponse(content="store was successfully updated")

@router.delete("/stores/", status_code=204)
async def delete_store(store_id: int,
                       user: authModels.User = Depends(current_user),
                       entity_repo: AbstractEntityRepository = Depends(EntityRepository)
                       ):
    if not await entity_repo.delete_entity(entity_type=prodModels.Store, entity_id=store_id):
        return JSONResponse(content="there is no such store", status_code=404)


@router.patch("/stores/")
async def update_store(store: companySchemas.Store,
                       user: authModels.User = Depends(current_user),
                       entity_repo: AbstractEntityRepository = Depends(EntityRepository)):
    await entity_repo.update_entity(entity_class=prodModels.Store, entity_data=store.model_dump())
    return JSONResponse(content="store was successfully updated")


@router.post("/company/")
async def create_company(company: companySchemas.Company,
                         user: authModels.User = Depends(current_user),
                         entity_repo: AbstractEntityRepository = Depends(EntityRepository)):
    idCompany = await entity_repo.create_entity(entity_class=prodModels.Company, entity_data=company.model_dump())
    user_to_update = authSchemas.UserUpdate(id=user.id, idCompany=idCompany, name=user.name, login=user.login)
    await entity_repo.update_entity(authModels.User, user_to_update.model_dump())
    return JSONResponse(content="company was successfully added", status_code=201)


@router.get("/product/", status_code=200)
async def read_products(skip: int = 0, limit: int = 30, search_query: str = "",
                        user: authModels.User = Depends(current_user),
                        entity_repo: AbstractEntityRepository = Depends(EntityRepository)):
    return await entity_repo.get_entities(entity_class=prodModels.Product,
                                          idCompany=user.idCompany,
                                          search_query=search_query,
                                          skip=skip, limit=limit)


@router.post("/product/")
async def create_product(
        product: companySchemas.ProductCreate,
        user: authModels.User = Depends(current_user),
        entity_repo: AbstractEntityRepository = Depends(EntityRepository)
):
    same_product = await entity_repo.get_product_by_company_id_and_name(id=product.idCompany, name=product.name)
    if same_product:
        raise HTTPException(status_code=409, detail="product already exist")
    group = await entity_repo.get_group_by_company_id_and_name(name=product.type, id=user.idCompany)
    if not group:
        raise HTTPException(status_code=409, detail="group doesn't exist")
    product.idCompany = user.idCompany
    product.type = group.id
    await entity_repo.create_entity(entity_class=prodModels.Product, entity_data=product.model_dump())
    return JSONResponse(content="product was successfully added", status_code=201)

@router.patch("/product/")
async def update_store(product: companySchemas.ProductUpdate,
                       user: authModels.User = Depends(current_user),
                       entity_repo: AbstractEntityRepository = Depends(EntityRepository)):
    group = await entity_repo.get_group_by_company_id_and_name(name=product.type, id=user.idCompany)
    if not group:
        raise HTTPException(status_code=409, detail="group doesn't exist")
    product.idCompany = user.idCompany
    product.type = group.id
    await entity_repo.update_entity(entity_class=prodModels.Product, entity_data=product.model_dump())
    return JSONResponse(content="store was successfully updated")


@router.delete("/product/", status_code=204)
async def delete_product(product_id: int,
                         user: authModels.User = Depends(current_user),
                         entity_repo: AbstractEntityRepository = Depends(EntityRepository)):

    # Проверка продаж, связанных с продуктом
    sales_to_delete = await entity_repo.get_sales_with_only_this_product(product_id=product_id)
    buys_to_delete = await entity_repo.get_buys_with_only_this_product(product_id=product_id)

    if not await entity_repo.delete_entity(entity_type=prodModels.Product, entity_id=product_id):
        return JSONResponse(status_code=404, content="there is no such product")


    # Удаление продаж, у которых после удаления продукта не осталось товаров
    for sale in sales_to_delete:
        await entity_repo.delete_entity(entity_type=prodModels.Sale, entity_id=sale)
    for buy in buys_to_delete:
        await entity_repo.delete_entity(entity_type=prodModels.Buy, entity_id=buy)



@router.get("/group/", status_code=200)
async def read_groups(skip: int = 0, limit: int = 100,
                      user: authModels.User = Depends(current_user),
                      entity_repo: AbstractEntityRepository = Depends(EntityRepository)):
    return await entity_repo.get_entities(entity_class=prodModels.GroupOfProducts,
                                          idCompany=user.idCompany,
                                          skip=skip,
                                          limit=limit)


@router.post("/group/")
async def create_group(group: companySchemas.GroupCreate,
                       user: authModels.User = Depends(current_user),
                       entity_repo: AbstractEntityRepository = Depends(EntityRepository)):
    group.idCompany = user.idCompany
    same_group = await entity_repo.get_group_by_company_id_and_name(group.idCompany, group.name)
    if same_group:
        raise HTTPException(status_code=409, detail="group already exist")
    await entity_repo.create_entity(entity_class=prodModels.GroupOfProducts, entity_data=group.model_dump())
    return JSONResponse(content="group was successfully added", status_code=201)

@router.patch("/group/")
async def update_group(group: companySchemas.GroupUpdate,
                      user: authModels.User = Depends(current_user),
                      entity_repo: AbstractEntityRepository = Depends(EntityRepository)
                      ):
    group.idCompany = user.idCompany
    await entity_repo.update_entity(entity_class=prodModels.GroupOfProducts, entity_data=group.model_dump())
    return JSONResponse(content="group was successfully updated")

@router.get("/get_group_id/")
async def update_group(group_name: str,
                      user: authModels.User = Depends(current_user),
                      entity_repo: AbstractEntityRepository = Depends(EntityRepository)
                      ):
    return await entity_repo.get_group_by_company_id_and_name(id=user.idCompany, name=group_name)



@router.delete("/group/", status_code=204)
async def delete_group(group_name: str,
                       user: authModels.User = Depends(current_user),
                       entity_repo: AbstractEntityRepository = Depends(EntityRepository)):
    group = await entity_repo.get_group_by_company_id_and_name(user.idCompany, group_name)
    if not group:
        return JSONResponse(status_code=404, content="there is no such group")
    else:
        await entity_repo.delete_entity(entity_type=prodModels.GroupOfProducts, entity_id=group.id)


@router.get("/sale/", status_code=200)
async def read_sale(skip: int = 0, limit: int = 100,
                    user: authModels.User = Depends(current_user),
                    entity_repo: AbstractEntityRepository = Depends(EntityRepository)):
    return await entity_repo.get_entities(entity_class=prodModels.Sale, idCompany=user.idCompany, skip=skip,
                                          limit=limit)


@router.post("/sale/")
async def create_sale(sale: companySchemas.SaleCreate, info: list[dict],
                      user: authModels.User = Depends(current_user),
                      entity_repo: AbstractEntityRepository = Depends(EntityRepository)):
    sale.idCompany = user.idCompany
    sale.idWorker = user.id
    sale_id = await entity_repo.create_entity(entity_class=prodModels.Sale, entity_data=sale.model_dump())
    for product in info:
        cur_prod = await entity_repo.get_product_by_company_id_and_name(name=product["name"], id=user.idCompany)
        await entity_repo.update_product_on_store(minus=True,
                                                  product_id=cur_prod.id,
                                                  store_id=sale.idStore,
                                                  amount=product["amount"])
        info_db = {
            "idSale": sale_id,
            "idProduct": cur_prod.id,
            "amount": product["amount"],
            "cost": product["cost"]
        }
        await entity_repo.create_entity(entity_class=prodModels.InfoAboutSale, entity_data=info_db)
    return JSONResponse(content="sale was successfully added", status_code=201)


@router.delete("/sale/", status_code=204)
async def delete_sale(sale_id: int,
                      user: authModels.User = Depends(current_user),
                      entity_repo: AbstractEntityRepository = Depends(EntityRepository)):
    try:
        products = await entity_repo.get_products_for_sale(sale_id=sale_id)
        sale = await entity_repo.get_entity(entity_type=prodModels.Sale, entity_id=sale_id)
        store_id = sale.idStore
        await entity_repo.delete_entity(entity_type=prodModels.Sale, entity_id=sale_id)
        for product in products:
            await entity_repo.update_product_on_store(minus=False,
                                                      product_id=product["product_id"],
                                                      store_id=store_id,
                                                      amount=product["amount"])
    except:
        return JSONResponse(content="fail to delete sale", status_code=404)


@router.get("/getAddressStore/", status_code=200)
async def get_addr_store(store_id: int,
                         user: authModels.User = Depends(current_user),
                         entity_repo: AbstractEntityRepository = Depends(EntityRepository)):
    return await entity_repo.get_address_of_store(id=store_id)


@router.get("/get_total_amount_of_sale", status_code=200)
async def get_amount(product_id: int, period: int,
                     user: authModels.User = Depends(current_user),
                     entity_repo: AbstractEntityRepository = Depends(EntityRepository)):
    return await entity_repo.get_total_product_sales(product_id=product_id, period=period)

@router.get("/get_total_amount_of_buy", status_code=200)
async def get_amount(product_id: int, period: int,
                     user: authModels.User = Depends(current_user),
                     entity_repo: AbstractEntityRepository = Depends(EntityRepository)):
    return await entity_repo.get_total_product_buys(product_id=product_id, period=period)

@router.get("/get_turnover", status_code=200)
async def get_turnover(product_id: int, period: int,
                     user: authModels.User = Depends(current_user),
                     entity_repo: AbstractEntityRepository = Depends(EntityRepository)):
    return await entity_repo.get_turnover(product_id=product_id, period=period)


@router.get("/get_total_amount_on_store", status_code=200)
async def get_amount(product_id: int,
                     user: authModels.User = Depends(current_user),
                     entity_repo: AbstractEntityRepository = Depends(EntityRepository)):
    return await entity_repo.get_total_product_amount(product_id=product_id)

@router.get("/get_monthly_sale", status_code=200)
async def get_amount(product_id: int, period: int,
                     user: authModels.User = Depends(current_user),
                     entity_repo: AbstractEntityRepository = Depends(EntityRepository)):
    return await entity_repo.get_monthly_product_sales(product_id=product_id, period=period)

@router.get("/get_monthly_buys", status_code=200)
async def get_buys(product_id: int, period: int,
                   user: authModels.User = Depends(current_user),
                   entity_repo: AbstractEntityRepository = Depends(EntityRepository)):
    return await entity_repo.get_monthly_product_buys(product_id=product_id, period=period)


@router.get("/buy/", status_code=200)
async def read_buy(skip: int = 0, limit: int = 100,
                   user: authModels.User = Depends(current_user),
                   entity_repo: AbstractEntityRepository = Depends(EntityRepository)):
    return await entity_repo.get_entities(entity_class=prodModels.Buy, idCompany=user.idCompany, skip=skip, limit=limit)


@router.post("/buy/")
async def create_buy(buy: companySchemas.BuyCreate, info: list[dict],
                     user: authModels.User = Depends(current_user),
                     entity_repo: AbstractEntityRepository = Depends(EntityRepository)):
    buy.idCompany = user.idCompany
    buy.idWorker = user.id
    buy_id = await entity_repo.create_entity(entity_class=prodModels.Buy, entity_data=buy.model_dump())

    for product in info:
        cur_prod = await entity_repo.get_product_by_company_id_and_name(name=product["name"], id=user.idCompany)
        await entity_repo.update_product_on_store(minus=False,
                                                  product_id=cur_prod.id,
                                                  store_id=buy.idStore,
                                                  amount=product["amount"])
        info_db = {
            "idBuy": buy_id,
            "idProduct": cur_prod.id,
            "amount": product["amount"],
            "cost": product["cost"]
        }
        await entity_repo.create_entity(entity_class=prodModels.InfoAboutBuy, entity_data=info_db)
    return JSONResponse(content="buy was successfully added", status_code=201)


@router.delete("/buy/", status_code=204)
async def delete_buy(buy_id: int,
                     user: authModels.User = Depends(current_user),
                     entity_repo: AbstractEntityRepository = Depends(EntityRepository)):
    try:
        products = await entity_repo.get_products_for_buy(buy_id=buy_id)
        buy = await entity_repo.get_entity(entity_type=prodModels.Buy, entity_id=buy_id)
        store_id = buy.idStore
        await entity_repo.delete_entity(entity_type=prodModels.Buy, entity_id=buy_id)
        for product in products:
            await entity_repo.update_product_on_store(minus=True,
                                                      product_id=product["product_id"],
                                                      store_id=store_id,
                                                      amount=product["amount"])
    except:
        return JSONResponse(content="fail to delete buy", status_code=404)


@router.get("/get_amount_buy_of_store/", status_code=200)
async def get_buy_of_store(store_id: int, period: int,
                           user: authModels.User = Depends(current_user),
                           entity_repo: AbstractEntityRepository = Depends(EntityRepository)):
    number = await entity_repo.get_total_store_buy(store_id=store_id, period=period)
    number += await entity_repo.get_total_store_displacement_to(store_id=store_id, period=period)
    number += await entity_repo.get_total_returns(store_id=store_id, period=period)
    return number


@router.get("/get_amount_sale_of_store/", status_code=200)
async def get_sales_of_store(store_id: int, period: int,
                             user: authModels.User = Depends(current_user),
                             entity_repo: AbstractEntityRepository = Depends(EntityRepository)):
    number = await entity_repo.get_total_store_sale(store_id=store_id, period=period)
    number += await entity_repo.get_total_store_displacement_from(store_id=store_id, period=period)
    return number


@router.get("/get_amount_products_on_store/", status_code=200)
async def get_products_on_store(store_id: int,
                                user: authModels.User = Depends(current_user),
                                entity_repo: AbstractEntityRepository = Depends(EntityRepository)):
    return await entity_repo.get_total_store_products(store_id=store_id)


@router.get("/get_cost_of_sale/", status_code=200)
async def get_total_cost_sale(sale_id: int,
                              user: authModels.User = Depends(current_user),
                              entity_repo: AbstractEntityRepository = Depends(EntityRepository)):
    return await entity_repo.get_total_cost_value_sale(id=sale_id)


@router.get("/get_cost_of_buy/", status_code=200)
async def get_total_cost_buy(buy_id: int,
                             user: authModels.User = Depends(current_user),
                             entity_repo: AbstractEntityRepository = Depends(EntityRepository)):
    return await entity_repo.get_total_cost_value_buy(id=buy_id)


@router.get("/get_buy_products/", status_code=200)
async def get_buy_products(buy_id: int,
                           user: authModels.User = Depends(current_user),
                           entity_repo: AbstractEntityRepository = Depends(EntityRepository)):
    products = await entity_repo.get_products_for_buy(buy_id)
    return products


@router.get("/get_sale_products/", status_code=200)
async def get_sale_products(sale_id: int,
                            user: authModels.User = Depends(current_user),
                            entity_repo: AbstractEntityRepository = Depends(EntityRepository)):
    products = await entity_repo.get_products_for_sale(sale_id)
    return products

@router.get("/get_returns_for_sale/", status_code=200)
async def get_sale_returns(sale_id: int,
                            user: authModels.User = Depends(current_user),
                            entity_repo: AbstractEntityRepository = Depends(EntityRepository)):
    returns = await entity_repo.get_returns_for_sale(sale_id=sale_id)
    return returns

@router.get("/get_total_summ_of_buys/", status_code=200)
async def get_total_sum_of_buys(product_id: int, period: int,
                            user: authModels.User = Depends(current_user),
                            entity_repo: AbstractEntityRepository = Depends(EntityRepository)):
    returns = await entity_repo.get_total_product_buys_cost(product_id=product_id, period=period)
    return returns



@router.get("/do_ABC_analysis/", status_code=200)
async def do_ABC_analysis(period: int,
                          user: authModels.User = Depends(current_user),
                          entity_repo: AbstractEntityRepository = Depends(EntityRepository)):
    return await entity_repo.do_ABC_analysis(company_id=user.idCompany, period=period)



@router.get("/displacement/", status_code=200)
async def read_displacement(skip: int = 0, limit: int = 100,
                           user: authModels.User = Depends(current_user),
                           entity_repo: AbstractEntityRepository = Depends(EntityRepository)):
    return await entity_repo.get_entities(entity_class=prodModels.Displacement, idCompany=user.idCompany, skip=skip, limit=limit)


@router.post("/displacement/", status_code=201)
async def create_displacement(displacement: companySchemas.DisplacementCreate,
                             user: authModels.User = Depends(current_user),
                             entity_repo: AbstractEntityRepository = Depends(EntityRepository)):
    displacement.idCompany = user.idCompany
    displacement.idWorker = user.id
    await entity_repo.create_entity(entity_class=prodModels.Displacement, entity_data=displacement.model_dump())
    await entity_repo.update_product_on_store(minus=True, product_id=displacement.idProduct,
                                        store_id=displacement.idStore, amount=displacement.amount)
    await entity_repo.update_product_on_store(minus=False, product_id=displacement.idProduct,
                                        store_id=displacement.idStoreToMove, amount=displacement.amount)
    return JSONResponse(content="displacement was successfully added", status_code=201)


@router.delete("/displacement/", status_code=204)
async def delete_displacement(displacement_id: int,
                                user: authModels.User = Depends(current_user),
                                entity_repo: AbstractEntityRepository = Depends(EntityRepository)):
    try:
        displacement = await entity_repo.get_entity(entity_type=prodModels.Displacement, entity_id=displacement_id)
        product_id = displacement.idProduct
        store_id = displacement.idStore
        amount = displacement.amount
        store2_id = displacement.idStoreToMove
        await entity_repo.delete_entity(entity_type=prodModels.Displacement, entity_id=displacement_id)

        await entity_repo.update_product_on_store(minus=True,
                                                  product_id=product_id,
                                                  store_id=store2_id,
                                                  amount=amount)

        await entity_repo.update_product_on_store(minus=False,
                                                  product_id=product_id,
                                                  store_id=store_id,
                                                  amount=amount)
    except:
        return JSONResponse(content="fail to delete displacement", status_code=404)



@router.get("/get_name_of_product/", status_code=200)
async def get_name_of_product(product_id: int,
                          user: authModels.User = Depends(current_user),
                          entity_repo: AbstractEntityRepository = Depends(EntityRepository)):
    product = await entity_repo.get_entity(entity_type=prodModels.Product, entity_id=product_id)
    if product:
        return product.name
    else:
        return JSONResponse(content="failed to get product name", status_code=404)

@router.get("/get_name_of_group/", status_code=200)
async def get_name_of_product(group_id: int,
                          user: authModels.User = Depends(current_user),
                          entity_repo: AbstractEntityRepository = Depends(EntityRepository)):
    group = await entity_repo.get_entity(entity_type=prodModels.GroupOfProducts, entity_id=group_id)
    if group:
        return group.name
    else:
        return JSONResponse(content="failed to get group name", status_code=404)


# @router.get("/inventory/", status_code=200)
# async def read_inventory(skip: int = 0, limit: int = 100,
#                            user: authModels.User = Depends(current_user),
#                            entity_repo: AbstractEntityRepository = Depends(EntityRepository)):
#     return await entity_repo.get_entities(entity_class=prodModels.Inventory,
#                                           idCompany=user.idCompany,
#                                           skip=skip, limit=limit)


@router.get("/get_return/", status_code=200)
async def read_return(skip: int = 0, limit: int = 100,
                           user: authModels.User = Depends(current_user),
                           entity_repo: AbstractEntityRepository = Depends(EntityRepository)):
    return await entity_repo.get_entities(entity_class=prodModels.Return,
                                          idCompany=user.idCompany,
                                          skip=skip, limit=limit)

@router.post("/create_return/")
async def create_return(cur_return: companySchemas.ReturnCreate,
                         user: authModels.User = Depends(current_user),
                         entity_repo: AbstractEntityRepository = Depends(EntityRepository)):
    cur_return.idCompany = user.idCompany
    cur_return.idWorker = user.id
    cur_return.date = datetime.now().strftime("%d.%m.%Y")
    return_id = await entity_repo.create_entity(entity_class=prodModels.Return, entity_data=cur_return.model_dump())
    return JSONResponse(content={"message":"Return was successfully added", "id":return_id}, status_code=201)

@router.delete("/del_return/", status_code=204)
async def delete_return(return_id: int,
                        user: authModels.User = Depends(current_user),
                        entity_repo: AbstractEntityRepository = Depends(EntityRepository)):
    try:
        cur_return = await entity_repo.get_entity(entity_type=prodModels.Return, entity_id=return_id)
        product_id = cur_return.idProduct
        store_id = cur_return.idStore
        amount = cur_return.amount
        status = cur_return.status
        await entity_repo.delete_entity(entity_type=prodModels.Return, entity_id=return_id)
        if status == prodModels.StatusOfReturn.done:
            await entity_repo.update_product_on_store(minus=False,
                                                      product_id=product_id,
                                                      store_id=store_id,
                                                      amount=amount)
    except:
        return JSONResponse(content="fail to delete return", status_code=404)

@router.patch("/update_return/")
async def update_return(return_id: int, status: prodModels.StatusOfReturn,
                       user: authModels.User = Depends(current_user),
                       entity_repo: AbstractEntityRepository = Depends(EntityRepository)):

    cur_return = await entity_repo.get_entity(entity_type=prodModels.Return, entity_id=return_id)
    if cur_return.status == prodModels.StatusOfReturn.done and status != prodModels.StatusOfReturn.done:
        entity_repo.update_product_on_store(minus=True,
                                            store_id=cur_return.idStore,
                                            product_id=cur_return.idProduct,
                                            amount=cur_return.amount)
    if cur_return.status != prodModels.StatusOfReturn.done and status == prodModels.StatusOfReturn.done:
        entity_repo.update_product_on_store(minus=False,
                                            store_id=cur_return.idStore,
                                            product_id=cur_return.idProduct,
                                            amount=cur_return.amount)
    cur_return.status = status
    cur_return.date = datetime.now().strftime("%d.%m.%Y")
    await entity_repo.update_entity(entity_class=prodModels.Return, entity_data=cur_return.to_dict())
    return JSONResponse(content="return was successfully updated")

@router.get("/getTotalRevenue/", status_code=200)
async def get_revenue(period: int,
                      user: authModels.User = Depends(current_user),
                      entity_repo: AbstractEntityRepository = Depends(EntityRepository)):
    return await entity_repo.get_total_revenue_by_company(company_id=user.idCompany, period=period)

@router.get("/getTotalSales/", status_code=200)
async def get_revenue(period: int,
                      user: authModels.User = Depends(current_user),
                      entity_repo: AbstractEntityRepository = Depends(EntityRepository)):
    return await entity_repo.get_total_sales_for_company(company_id=user.idCompany, period=period)

@router.get("/getTotalBuys/", status_code=200)
async def get_revenue(period: int,
                      user: authModels.User = Depends(current_user),
                      entity_repo: AbstractEntityRepository = Depends(EntityRepository)):
    return await entity_repo.get_total_buys_for_company(company_id=user.idCompany, period=period)

@router.get("/getTotalReturns/", status_code=200)
async def get_revenue(period: int,
                      user: authModels.User = Depends(current_user),
                      entity_repo: AbstractEntityRepository = Depends(EntityRepository)):
    return await entity_repo.get_total_returns_for_company(company_id=user.idCompany, period=period)

@router.get("/getMonthlyRevenue/", status_code=200)
async def get_revenue(period: int,
                      user: authModels.User = Depends(current_user),
                      entity_repo: AbstractEntityRepository = Depends(EntityRepository)):
    return await entity_repo.get_monthly_company_revenue(company_id=user.idCompany, period=period)


@router.get("/get_company_data", response_model=dict)
async def get_company_data(period: int,
                           user: authModels.User = Depends(current_user),
                           entity_repo: AbstractEntityRepository = Depends(EntityRepository)):
    company_id = user.idCompany
    total_revenue = await entity_repo.get_total_revenue_by_company(company_id, period)
    total_sales = await entity_repo.get_total_sales_for_company(company_id, period)
    total_buys = await entity_repo.get_total_buys_for_company(company_id, period)
    total_returns = await entity_repo.get_total_returns_for_company(company_id, period)
    statistic = await entity_repo.get_company_statistics(company_id)

    return {
        "totalRevenue": total_revenue,
        "totalSales": total_sales,
        "totalBuys": total_buys,
        "totalReturns": total_returns,
        "totalProducts": statistic["total_products"],
        "totalStores": statistic["total_stores"],
        "totalEmployees": statistic["total_employees"]
    }


@router.get("/get_company")
async def get_company_data(user: authModels.User = Depends(current_user),
                           entity_repo: AbstractEntityRepository = Depends(EntityRepository)):
    return await entity_repo.get_entity(entity_type=prodModels.Company, entity_id=user.idCompany)