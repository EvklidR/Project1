from abc import abstractmethod, ABC
from datetime import datetime, timedelta
from typing import Type, List, Tuple

from sqlalchemy import select, func, cast, Date

from model.database import sessionLocal


import app.companyData.models as ProdModels
import app.auth.models as authModels


class AbstractOperationsRepository(ABC):
    @abstractmethod
    def get_total_returns(store_id: int, period: int) -> int:
        pass

    @abstractmethod
    def get_total_cost_value_sale(id: int) -> int:
        pass

    @abstractmethod
    def get_total_cost_value_buy(id: int) -> int:
        pass

    @abstractmethod
    def get_products_for_buy(buy_id: int) -> List[dict]:
        pass

    @abstractmethod
    def get_products_for_sale(sale_id: int) -> List[dict]:
        pass

    @abstractmethod
    def get_returns_for_sale(sale_id: int) -> List[dict]:
        pass

    @abstractmethod
    def get_total_product_buys_cost(product_id: int, period: int) -> int:
        pass

class AbstractCompanyRepository(ABC):

    @abstractmethod
    def get_total_revenue_by_company(company_id: int, period: int) -> int:
        pass

    @abstractmethod
    def do_ABC_analysis(company_id: int, period: str):
        pass


    @abstractmethod
    def get_total_sales_for_company(company_id: int, period: int) -> int:
        pass

    @abstractmethod
    def get_total_buys_for_company(company_id: int, period: int) -> int:
        pass

    @abstractmethod
    def get_total_returns_for_company(company_id: int, period: int) -> int:
        pass

    @abstractmethod
    def get_monthly_company_revenue(company_id: int, period: int):
        pass

    @abstractmethod
    def get_company_statistics(company_id: int):
        pass

class AbstractStoreRepository(ABC):

    @abstractmethod
    def get_total_store_products(store_id: int) -> int:
        pass

    @abstractmethod
    def get_address_of_store(id: int):
        pass

    @abstractmethod
    def get_total_store_displacement_from(store_id: int, period: int) -> int:
        pass

    @abstractmethod
    def get_total_store_displacement_to(store_id: int, period: int) -> int:
        pass

    @abstractmethod
    def get_total_store_buy(store_id: int, period: int) -> int:
        pass

    @abstractmethod
    def get_total_store_sale(store_id: int, period: int) -> int:
        pass


class AbstractProductRepository(ABC):
    @abstractmethod
    def get_revenue_of_product(company_id: int, period: int):
        pass

    @abstractmethod
    def get_monthly_product_sales(product_id: int, period: int) -> dict:
        pass

    @abstractmethod
    def get_monthly_product_buys(product_id: int, period: int):
        pass

    @abstractmethod
    def get_total_product_amount(product_id: int) -> int:
        pass

    @abstractmethod
    def get_product_by_company_id_and_name(id: int, name: str):
        pass

    @abstractmethod
    def get_group_by_company_id_and_name(id: int, name: str):
        pass

    @abstractmethod
    def get_total_product_sales(product_id: int, period: int) -> int:
        pass

    @abstractmethod
    def get_total_product_buys(product_id: int, period: int) -> int:
        pass

    @abstractmethod
    def get_total_product_returns(product_id: int, period: int) -> int:
        pass

    @abstractmethod
    def get_turnover(product_id: int, period: int) -> int:
        pass

    @abstractmethod
    def get_sales_with_only_this_product(product_id: int):
        pass

    @abstractmethod
    def get_buys_with_only_this_product(product_id: int):
        pass

class AbstractGeneralRepository(ABC):

    @abstractmethod
    def get_entities(entity_class: Type, search_query: str, idCompany: int, skip: int = 0, limit: int = 100):
        pass

    @abstractmethod
    def get_entity(entity_type: Type, entity_id: int):
        pass

    @abstractmethod
    def delete_entity(entity_type: Type, entity_id: int):
        pass

    @abstractmethod
    def create_entity(entity_class: Type, entity_data: dict):
        pass

    @abstractmethod
    def update_entity(entity_class: Type, entity_data: dict):
        pass

    @abstractmethod
    def update_product_on_store(minus: bool, product_id: int, store_id: int, amount: int):
        pass


class AbstractEntityRepository(AbstractProductRepository,
                               AbstractGeneralRepository,
                               AbstractStoreRepository,
                               AbstractCompanyRepository,
                               AbstractOperationsRepository):
    pass


class EntityProductRepository(AbstractProductRepository):

    @staticmethod
    def calculate_start_date(period: int):
        end_date = datetime.now()
        start_date = end_date.replace(day=1)
        for _ in range(period - 1):
            if start_date.month == 1:
                start_date = start_date.replace(year=start_date.year - 1, month=12)
            else:
                start_date = start_date.replace(month=start_date.month - 1)
        return start_date

    @staticmethod
    async def get_product_by_company_id_and_name(id: int, name: str):
        async with (sessionLocal() as sess):
            query = select(ProdModels.Product).filter(ProdModels.Product.idCompany == id
                                                      ).filter(ProdModels.Product.name == name)
            result = await sess.execute(query)
            product = result.scalars().first()
            return product

    @staticmethod
    async def get_group_by_company_id_and_name(id: int, name: str):
        async with sessionLocal() as sess:
            query = select(ProdModels.GroupOfProducts).filter(ProdModels.GroupOfProducts.idCompany == id
                                                              ).filter(ProdModels.GroupOfProducts.name == name)
            result = await sess.execute(query)
            group = result.scalars().first()
            return group

    @staticmethod
    async def get_total_product_sales(product_id: int, period: int) -> int:
        async with sessionLocal() as sess:

            start_date = EntityProductRepository.calculate_start_date(period)

            query = select(
                func.sum(ProdModels.InfoAboutSale.amount)
            ).join(
                ProdModels.Sale, ProdModels.InfoAboutSale.idSale == ProdModels.Sale.id
            ).where(
                ProdModels.InfoAboutSale.idProduct == product_id,
                cast(func.to_date(ProdModels.Sale.date, 'DD.MM.YYYY'), Date) >= start_date.date()
            )

            result: Tuple[int] = await sess.execute(query)
            total_sales = result.scalar()

        return total_sales or 0

    @staticmethod
    async def get_total_product_buys(product_id: int, period: int) -> int:
        async with sessionLocal() as sess:
            start_date = EntityProductRepository.calculate_start_date(period)

            query = select(
                func.sum(ProdModels.InfoAboutBuy.amount)
            ).join(
                ProdModels.Buy, ProdModels.InfoAboutBuy.idBuy == ProdModels.Buy.id
            ).where(
                ProdModels.InfoAboutBuy.idProduct == product_id,
                cast(func.to_date(ProdModels.Buy.date, 'DD.MM.YYYY'), Date) >= start_date.date()
            )

            result: Tuple[int] = await sess.execute(query)
            total_buys_amount = result.scalar()

        return total_buys_amount or 0

    @staticmethod
    async def get_total_product_returns(product_id: int, period: int) -> int:
        async with sessionLocal() as sess:

            start_date = EntityProductRepository.calculate_start_date(period)

            # Получить количество возвратов за указанный период
            query = select(
                func.sum(ProdModels.Return.amount)
            ).where(
                ProdModels.Return.idProduct == product_id,
                cast(func.to_date(ProdModels.Return.date, 'DD.MM.YYYY'), Date) >= start_date.date(),
            )

            result = await sess.execute(query)
            total_returns = result.scalar()

        return total_returns or 0

    @staticmethod
    async def get_avarage_amount_of_product(product_id: int, period: int) -> int:

        cur_amount = await EntityProductRepository.get_total_product_amount(product_id)
        buys_amount = await EntityProductRepository.get_total_product_buys(product_id=product_id, period=period)
        sales_amount = await EntityProductRepository.get_total_product_sales(product_id=product_id, period=period)
        returns_amount = await EntityProductRepository.get_total_product_returns(product_id=product_id, period=period)

        return (2 * cur_amount + sales_amount - buys_amount - returns_amount) // 2

    @staticmethod
    async def get_monthly_product_buys(product_id: int, period: int):
        async with sessionLocal() as sess:
            end_date = datetime.now()
            start_date = EntityProductRepository.calculate_start_date(period)

            query = select(
                ProdModels.Buy.date,
                func.sum(ProdModels.InfoAboutBuy.amount).label('total_buys')
            ).join(
                ProdModels.Buy, ProdModels.InfoAboutBuy.idBuy == ProdModels.Buy.id
            ).where(
                ProdModels.InfoAboutBuy.idProduct == product_id,
                cast(ProdModels.Buy.date, Date) >= start_date.date()
            ).group_by(
                ProdModels.Buy.date
            ).order_by(
                ProdModels.Buy.date
            )

            result = await sess.execute(query)
            rows = result.all()

            monthly_buys = {}
            current_date = start_date.date()

            # Initialize all months in the period with 0
            while current_date <= end_date.date():
                year_month = current_date.strftime("%Y-%m")
                monthly_buys[year_month] = 0
                next_month = current_date.month % 12 + 1
                next_year = current_date.year + (current_date.month // 12)
                current_date = current_date.replace(year=next_year, month=next_month, day=1)

            for row in rows:
                buy_date = datetime.strptime(row.date, "%d.%m.%Y")
                year_month = buy_date.strftime("%Y-%m")
                if year_month in monthly_buys:
                    monthly_buys[year_month] += row.total_buys

        return monthly_buys

    @staticmethod
    async def get_monthly_product_sales(product_id: int, period: int):
        async with sessionLocal() as sess:
            end_date = datetime.now()
            start_date = EntityProductRepository.calculate_start_date(period)

            query = select(
                ProdModels.Sale.date,
                func.sum(ProdModels.InfoAboutSale.amount).label('total_sales')
            ).join(
                ProdModels.Sale, ProdModels.InfoAboutSale.idSale == ProdModels.Sale.id
            ).where(
                ProdModels.InfoAboutSale.idProduct == product_id,
                cast(ProdModels.Sale.date, Date) >= start_date.date()
            ).group_by(
                ProdModels.Sale.date
            ).order_by(
                ProdModels.Sale.date
            )

            result = await sess.execute(query)
            rows = result.all()

            monthly_sales = {}
            current_date = start_date.date()

            # Initialize all months in the period with 0
            while current_date <= end_date.date():
                year_month = current_date.strftime("%Y-%m")
                monthly_sales[year_month] = 0
                next_month = current_date.month % 12 + 1
                next_year = current_date.year + (current_date.month // 12)
                current_date = current_date.replace(year=next_year, month=next_month, day=1)

            for row in rows:
                sale_date = datetime.strptime(row.date, "%d.%m.%Y")
                year_month = sale_date.strftime("%Y-%m")
                if year_month in monthly_sales:
                    monthly_sales[year_month] += row.total_sales

        return monthly_sales

    @staticmethod
    async def get_total_product_amount(product_id: int) -> int:
        async with sessionLocal() as sess:
            query = select(
                func.sum(ProdModels.ProductOnStore.amount)
            ).where(
                ProdModels.ProductOnStore.idProduct == product_id
            )
            result = await sess.execute(query)
            total_quantity = result.scalar()
            return total_quantity or 0

    @staticmethod
    async def get_revenue_of_product(company_id: int, period: int):
        async with sessionLocal() as sess:
            start_date = EntityProductRepository.calculate_start_date(period)

            query = select(
                ProdModels.Product.id,
                func.sum(ProdModels.InfoAboutSale.amount * ProdModels.InfoAboutSale.cost)
            ).join(
                ProdModels.InfoAboutSale, ProdModels.Product.id == ProdModels.InfoAboutSale.idProduct
            ).join(
                ProdModels.Sale, ProdModels.InfoAboutSale.idSale == ProdModels.Sale.id
            ).filter(
                ProdModels.Sale.idCompany == company_id,
                cast(ProdModels.Sale.date, Date) >= start_date.date()
            ).group_by(
                ProdModels.Product.id
            )
            return await sess.execute(query)

    @staticmethod
    async def get_turnover(product_id: int, period: int) -> float:
        generalAmountOfSales = await EntityProductRepository.get_total_product_sales(product_id=product_id,
                                                                                       period=period)
        avarageAmount = await EntityProductRepository.get_avarage_amount_of_product(product_id=product_id,
                                                                                    period=period)

        if avarageAmount:
            return round(generalAmountOfSales/avarageAmount, 2)
        else:
            return 0

    @staticmethod
    async def get_sales_with_only_this_product(product_id: int):
        async with sessionLocal() as sess:
            subquery = select(
                ProdModels.InfoAboutSale.idSale
            ).group_by(
                ProdModels.InfoAboutSale.idSale
            ).having(
                func.count(ProdModels.InfoAboutSale.idProduct) == 1
            ).alias('subquery')

            query = select(
                ProdModels.Sale.id
            ).join(
                subquery, ProdModels.Sale.id == subquery.c.idSale
            ).filter(
                ProdModels.InfoAboutSale.idProduct == product_id
            )

            result = await sess.execute(query)
            sales = result.scalars().all()

        return sales
    @staticmethod
    async def get_buys_with_only_this_product(product_id: int):
        async with sessionLocal() as sess:
            subquery = select(
                ProdModels.InfoAboutBuy.idBuy
            ).group_by(
                ProdModels.InfoAboutBuy.idBuy
            ).having(
                func.count(ProdModels.InfoAboutBuy.idProduct) == 1
            ).alias('subquery')

            query = select(
                ProdModels.Buy.id
            ).join(
                subquery, ProdModels.Buy.id == subquery.c.idBuy
            ).filter(
                ProdModels.InfoAboutBuy.idProduct == product_id
            )

            result = await sess.execute(query)
            sales = result.scalars().all()

        return sales
class EntityStoreRepository(AbstractStoreRepository):
    @staticmethod
    async def get_address_of_store(id: int):
        async with sessionLocal() as sess:
            query = select(ProdModels.Store).filter(ProdModels.Store.id == id)
            result = await sess.execute(query)
            store = result.scalars().first()
            return store.name

    @staticmethod
    async def get_total_store_buy(store_id: int, period: int) -> int:
        async with sessionLocal() as sess:
            # Get the current date
            end_date = datetime.now()
            # Calculate the start date based on the period (first day of the start month)
            start_date = end_date.replace(day=1)

            for _ in range(period - 1):
                if start_date.month == 1:
                    start_date = start_date.replace(year=start_date.year - 1, month=12)
                else:
                    start_date = start_date.replace(month=start_date.month - 1)

            start_date_str = start_date.strftime("%d.%m.%Y")

            query = select(
                func.sum(ProdModels.InfoAboutBuy.amount)
            ).join(
                ProdModels.Buy, ProdModels.InfoAboutBuy.idBuy == ProdModels.Buy.id
            ).where(
                ProdModels.Buy.idStore == store_id,
                cast(func.to_date(ProdModels.Buy.date, 'DD.MM.YYYY'), Date) >= start_date.date()
            )

            result: Tuple[int] = await sess.execute(query)
            total_buys = result.scalar()

        return total_buys or 0

    @staticmethod
    async def get_total_store_sale(store_id: int, period: int) -> int:
        async with sessionLocal() as sess:
            # Get the current date
            end_date = datetime.now()
            # Calculate the start date based on the period (first day of the start month)
            start_date = end_date.replace(day=1)

            for _ in range(period - 1):
                if start_date.month == 1:
                    start_date = start_date.replace(year=start_date.year - 1, month=12)
                else:
                    start_date = start_date.replace(month=start_date.month - 1)

            start_date_str = start_date.strftime("%d.%m.%Y")

            query = select(
                func.sum(ProdModels.InfoAboutSale.amount)
            ).join(
                ProdModels.Sale, ProdModels.InfoAboutSale.idSale == ProdModels.Sale.id
            ).where(
                ProdModels.Sale.idStore == store_id,
                cast(func.to_date(ProdModels.Sale.date, 'DD.MM.YYYY'), Date) >= start_date.date()
            )

            result: Tuple[int] = await sess.execute(query)
            total_sales = result.scalar()

        return total_sales or 0

    @staticmethod
    async def get_total_store_displacement_from(store_id: int, period: int) -> int:
        async with sessionLocal() as sess:
            end_date = datetime.now()
            start_date = end_date.replace(day=1)

            for _ in range(period - 1):
                if start_date.month == 1:
                    start_date = start_date.replace(year=start_date.year - 1, month=12)
                else:
                    start_date = start_date.replace(month=start_date.month - 1)

            start_date_str = start_date.strftime("%d.%m.%Y")

            query = select(
                func.sum(ProdModels.Displacement.amount)
            ).where(
                ProdModels.Displacement.idStore == store_id,
                cast(func.to_date(ProdModels.Displacement.date, 'DD.MM.YYYY'), Date) >= start_date.date()
            )

            result: Tuple[int] = await sess.execute(query)
            total_displacement_from = result.scalar()

        return total_displacement_from or 0

    @staticmethod
    async def get_total_store_displacement_to(store_id: int, period: int) -> int:
        async with sessionLocal() as sess:
            end_date = datetime.now()
            start_date = end_date.replace(day=1)

            for _ in range(period - 1):
                if start_date.month == 1:
                    start_date = start_date.replace(year=start_date.year - 1, month=12)
                else:
                    start_date = start_date.replace(month=start_date.month - 1)

            start_date_str = start_date.strftime("%d.%m.%Y")

            query = select(
                func.sum(ProdModels.Displacement.amount)
            ).where(
                ProdModels.Displacement.idStoreToMove == store_id,
                cast(func.to_date(ProdModels.Displacement.date, 'DD.MM.YYYY'), Date) >= start_date.date()
            )

            result: Tuple[int] = await sess.execute(query)
            total_displacement_to = result.scalar()

        return total_displacement_to or 0

    @staticmethod
    async def get_total_store_products(store_id: int) -> int:
        async with sessionLocal() as sess:
            query = select(
                func.sum(ProdModels.ProductOnStore.amount)
            ).where(ProdModels.ProductOnStore.idStore == store_id)

            result: Tuple[int] = await sess.execute(query)
            total_sales = result.scalar()

        return total_sales or 0


class EntityOperationsRepository(AbstractOperationsRepository):
    @staticmethod
    async def get_total_returns(store_id: int, period: int) -> int:
        async with sessionLocal() as sess:
            start_date = datetime.now() - timedelta(days=period * 30)

            query = select(
                func.sum(ProdModels.Return.amount)
            ).filter(
                ProdModels.Return.idStore == store_id,
                cast(ProdModels.Return.date, Date) >= start_date.date()
            )

            result: Tuple[int] = await sess.execute(query)
            total_returns = result.scalar()

        return total_returns or 0

    @staticmethod
    async def get_total_cost_value_buy(id: int) -> int:
        async with sessionLocal() as sess:
            query = select(
                func.sum(ProdModels.InfoAboutBuy.cost * ProdModels.InfoAboutBuy.amount)
            ). \
                where(ProdModels.InfoAboutBuy.idBuy == id)

            result: Tuple[int] = await sess.execute(query)
            total_buy_value = result.scalar()

        return total_buy_value or 0

    @staticmethod
    async def get_total_cost_value_sale(id: int) -> int:
        async with sessionLocal() as sess:
            query = select(
                func.sum(ProdModels.InfoAboutSale.cost * ProdModels.InfoAboutSale.amount)
            ). \
                where(ProdModels.InfoAboutSale.idSale == id)

            result: Tuple[int] = await sess.execute(query)
            total_buy_value = result.scalar()

        return total_buy_value or 0

    @staticmethod
    async def get_products_for_buy(buy_id: int) -> List[dict]:
        async with sessionLocal() as sess:
            result = await sess.execute(
                select(
                    ProdModels.Product.name,
                    ProdModels.InfoAboutBuy.cost,
                    ProdModels.InfoAboutBuy.amount
                )
                .join(ProdModels.InfoAboutBuy, ProdModels.InfoAboutBuy.idProduct == ProdModels.Product.id)
                .join(ProdModels.Buy, ProdModels.Buy.id == ProdModels.InfoAboutBuy.idBuy)
                .where(ProdModels.Buy.id == buy_id)
            )
            products = result.all()
            return [
                {
                    "name": product.name,
                    "cost": product.cost,
                    "amount": product.amount
                } for product in products
            ]

    @staticmethod
    async def get_products_for_sale(sale_id: int) -> List[dict]:
        async with sessionLocal() as sess:
            result = await sess.execute(
                select(
                    ProdModels.Product.id,
                    ProdModels.Product.name,
                    ProdModels.InfoAboutSale.cost,
                    ProdModels.InfoAboutSale.amount
                )
                .join(ProdModels.InfoAboutSale, ProdModels.InfoAboutSale.idProduct == ProdModels.Product.id)
                .join(ProdModels.Sale, ProdModels.Sale.id == ProdModels.InfoAboutSale.idSale)
                .where(ProdModels.Sale.id == sale_id)
            )
            products = result.all()
            return [
                {
                    "product_id": product.id,
                    "name": product.name,
                    "cost": product.cost,
                    "amount": product.amount
                } for product in products
            ]

    @staticmethod
    async def get_returns_for_sale(sale_id: int) -> List[dict]:
        async with sessionLocal() as sess:
            result = await sess.execute(
                select(
                    ProdModels.Return.id.label("return_id"),
                    ProdModels.Product.name,
                    ProdModels.Return.cost,
                    ProdModels.Return.amount
                )
                .join(ProdModels.Sale, ProdModels.Sale.id == ProdModels.Return.idSale)
                .join(ProdModels.Product, ProdModels.Product.id == ProdModels.Return.idProduct)
                .where(ProdModels.Sale.id == sale_id)
            )
            returns = result.all()
            return [
                {
                    "return_id": return_.return_id,
                    "name": return_.name,
                    "cost": return_.cost,
                    "amount": return_.amount
                } for return_ in returns
            ]

    @staticmethod
    async def get_total_product_buys_cost(product_id: int, period: int) -> int:
        async with sessionLocal() as sess:
            end_date = datetime.now()
            start_date = end_date.replace(day=1)

            for _ in range(period - 1):
                if start_date.month == 1:
                    start_date = start_date.replace(year=start_date.year - 1, month=12)
                else:
                    start_date = start_date.replace(month=start_date.month - 1)

            start_date_str = start_date.strftime("%d.%m.%Y")

            query = select(
                func.sum(ProdModels.InfoAboutBuy.amount * ProdModels.InfoAboutBuy.cost)
            ).join(ProdModels.Buy, ProdModels.InfoAboutBuy.idBuy == ProdModels.Buy.id
                   ).filter(ProdModels.InfoAboutBuy.idProduct == product_id,
                            cast(func.to_date(ProdModels.Buy.date, 'DD.MM.YYYY'), Date) >= start_date.date())

            result: Tuple[int] = await sess.execute(query)
            total_buys_cost = result.scalar()

        return total_buys_cost or 0


class EntityGeneralRepository(AbstractGeneralRepository):

    @staticmethod
    async def get_entities(entity_class: Type, idCompany: int, search_query: str = "", skip: int = 0, limit: int = 100):
        async with sessionLocal() as sess:
            query = select(entity_class).where(entity_class.idCompany == idCompany)
            if search_query:
                search_query = search_query.lower()
                query = query.where(func.lower(entity_class.name).contains(search_query))
            result = await sess.execute(query.offset(skip).limit(limit))
            entities = result.scalars().all()
            return entities

    @staticmethod
    async def get_entity(entity_type: Type, entity_id: int):
        async with sessionLocal() as sess:
            query = select(entity_type).where(entity_type.id == entity_id)
            result = await sess.execute(query)
            entity = result.scalars().first()
            return entity

    @staticmethod
    async def delete_entity(entity_type: Type, entity_id: int):
        async with sessionLocal() as sess:
            db_entity = await sess.get(entity_type, entity_id)
            if db_entity:
                await sess.delete(db_entity)
                await sess.commit()
                return True
            return False

    @staticmethod
    async def create_entity(entity_class: Type, entity_data: dict):
        async with sessionLocal() as sess:
            db_entity = entity_class(**entity_data)
            sess.add(db_entity)
            await sess.flush()
            await sess.commit()
            return db_entity.id

    @staticmethod
    async def update_entity(entity_class: Type, entity_data: dict):
        async with sessionLocal() as sess:
            entity_id = entity_data.get("id")

            if entity_id:
                db_entity = await sess.execute(select(entity_class).where(entity_class.id == entity_id))
                db_entity = db_entity.scalar()
                if db_entity:
                    for key, value in entity_data.items():
                        setattr(db_entity, key, value)
                    await sess.commit()
                    return True
                else:
                    return False
            else:
                return False


    @staticmethod
    async def update_product_on_store(minus: bool, product_id: int, store_id: int, amount: int):
        async with sessionLocal() as sess:
            product_on_store = await sess.get(ProdModels.ProductOnStore, (product_id, store_id))
            if product_on_store is None:
                product_on_store = ProdModels.ProductOnStore(idProduct=product_id, idStore=store_id, amount=0)
                sess.add(product_on_store)

            if minus:
                product_on_store.amount -= amount
            else:
                product_on_store.amount += amount
            await sess.commit()
            return True


class EntityCompanyRepository(AbstractCompanyRepository):

    @staticmethod
    def calculate_start_date(period: int):
        end_date = datetime.now()
        start_date = end_date.replace(day=1)
        for _ in range(period - 1):
            if start_date.month == 1:
                start_date = start_date.replace(year=start_date.year - 1, month=12)
            else:
                start_date = start_date.replace(month=start_date.month - 1)
        return start_date

    @staticmethod
    async def get_total_revenue_by_company(company_id: int, period: int) -> int:
        async with sessionLocal() as sess:

            start_date = EntityCompanyRepository.calculate_start_date(period)

            query = select(
                func.sum(ProdModels.InfoAboutSale.amount * ProdModels.InfoAboutSale.cost)
            ).join(
                ProdModels.Sale, ProdModels.InfoAboutSale.idSale == ProdModels.Sale.id
            ).filter(
                ProdModels.Sale.idCompany == company_id,
                cast(ProdModels.Sale.date, Date) >= start_date.date(),
            )

            result = await sess.execute(query)
            total_revenue = result.scalar() or 0

        return total_revenue

    @staticmethod
    async def do_ABC_analysis(company_id: int, period: int):
        # Определяем дату начала периода
        start_date = EntityCompanyRepository.calculate_start_date(period)

        result = await EntityRepository.get_revenue_of_product(company_id, period)

        total_revenue_by_product = []

        total_company_revenue = await EntityRepository.get_total_revenue_by_company(company_id, period)

        # Преобразование результатов запроса в словарь для удобства доступа по идентификатору товара
        revenue_by_product = {product_id: revenue for product_id, revenue in result}

        # Получение списка всех товаров для данной компании
        all_products = await EntityRepository.get_entities(entity_class=ProdModels.Product, idCompany=company_id)

        # Добавление всех товаров в анализ выручки, включая те, у которых нет продаж
        for product in all_products:
            product_id = product.id
            revenue = revenue_by_product.get(product_id, 0)
            product_revenue_percent = round((revenue / total_company_revenue) * 100, 2) if total_company_revenue else 0

            total_revenue_by_product.append({
                "product_id": product_id,
                "revenue": revenue,
                "revenue_percent": product_revenue_percent,
            })

        # Sort the list in descending order by the percentage of revenue
        total_revenue_by_product.sort(key=lambda x: x["revenue_percent"], reverse=True)

        # Add the cumulative percentage to each product's percentage and assign categories
        cumulative_percent = 0
        revenue_analysis = {}
        for product in total_revenue_by_product:
            cumulative_percent += product["revenue_percent"]
            category = 'C'
            if product["revenue_percent"] == 0:
                category = 'C'
            elif cumulative_percent < 80 or product["revenue_percent"] > 80:
                category = 'A'
            elif cumulative_percent < 95:
                category = 'B'

            revenue_analysis[product["product_id"]] = {
                "revenue": product["revenue"],
                "revenue_percent": product["revenue_percent"],
                "cumulative_percent": cumulative_percent,
                "category": category
            }

        return revenue_analysis

    @staticmethod
    async def get_total_sales_for_company(company_id: int, period: int) -> int:
        async with sessionLocal() as sess:
            start_date = EntityProductRepository.calculate_start_date(period)
            query = select(
                func.sum(ProdModels.InfoAboutSale.amount)
            ).join(
                ProdModels.Sale, ProdModels.InfoAboutSale.idSale == ProdModels.Sale.id
            ).join(
                ProdModels.Product, ProdModels.InfoAboutSale.idProduct == ProdModels.Product.id
            ).where(
                ProdModels.Product.idCompany == company_id,
                cast(func.to_date(ProdModels.Sale.date, 'DD.MM.YYYY'), Date) >= start_date.date()
            )

            result: Tuple[int] = await sess.execute(query)
            total_sales = result.scalar()

        return total_sales or 0

    @staticmethod
    async def get_total_buys_for_company(company_id: int, period: int) -> int:
        async with sessionLocal() as sess:
            start_date = EntityProductRepository.calculate_start_date(period)

            query = select(
                func.sum(ProdModels.InfoAboutBuy.amount)
            ).join(
                ProdModels.Buy, ProdModels.InfoAboutBuy.idBuy == ProdModels.Buy.id
            ).join(
                ProdModels.Product, ProdModels.InfoAboutBuy.idProduct == ProdModels.Product.id
            ).where(
                ProdModels.Product.idCompany == company_id,
                cast(func.to_date(ProdModels.Buy.date, 'DD.MM.YYYY'), Date) >= start_date.date()
            )

            result: Tuple[int] = await sess.execute(query)
            total_buys = result.scalar()

        return total_buys or 0

    @staticmethod
    async def get_total_returns_for_company(company_id: int, period: int) -> int:
        async with sessionLocal() as sess:
            start_date = EntityProductRepository.calculate_start_date(period)

            query = select(
                func.sum(ProdModels.Return.amount)
            ).join(
                ProdModels.Product, ProdModels.Return.idProduct == ProdModels.Product.id
            ).where(
                ProdModels.Product.idCompany == company_id,
                cast(func.to_date(ProdModels.Return.date, 'DD.MM.YYYY'), Date) >= start_date.date()
            )

            result: Tuple[int] = await sess.execute(query)
            total_returns = result.scalar()

        return total_returns or 0

    @staticmethod
    async def get_company_statistics(company_id: int):
        async with sessionLocal() as sess:
            # Подсчет общего количества видов товаров
            total_products_query = select(func.count(ProdModels.Product.id)).where(
                ProdModels.Product.idCompany == company_id)
            total_products_result = await sess.execute(total_products_query)
            total_products = total_products_result.scalar()

            # Подсчет общего количества складов
            total_stores_query = select(func.count(ProdModels.Store.id)).where(ProdModels.Store.idCompany == company_id)
            total_stores_result = await sess.execute(total_stores_query)
            total_stores = total_stores_result.scalar()

            # Подсчет общего количества сотрудников
            total_employees_query = select(func.count(authModels.User.id)).where(
                authModels.User.idCompany == company_id)
            total_employees_result = await sess.execute(total_employees_query)
            total_employees = total_employees_result.scalar()

        return {
            "total_products": total_products,
            "total_stores": total_stores,
            "total_employees": total_employees
        }

    @staticmethod
    async def get_monthly_company_revenue(company_id: int, period: int):
        async with sessionLocal() as sess:
            end_date = datetime.now()
            start_date = EntityCompanyRepository.calculate_start_date(period)

            query = select(
                ProdModels.Sale.date,
                func.sum(ProdModels.InfoAboutSale.amount * ProdModels.InfoAboutSale.cost).label('total_revenue')
            ).join(
                ProdModels.Sale, ProdModels.InfoAboutSale.idSale == ProdModels.Sale.id
            ).join(
                ProdModels.Product, ProdModels.InfoAboutSale.idProduct == ProdModels.Product.id
            ).where(
                ProdModels.Product.idCompany == company_id,
                cast(ProdModels.Sale.date, Date) >= start_date.date()
            ).group_by(
                ProdModels.Sale.date
            ).order_by(
                ProdModels.Sale.date
            )

            result = await sess.execute(query)
            rows = result.all()

            monthly_revenue = {}
            current_date = start_date.date()

            # Initialize all months in the period with 0
            while current_date <= end_date.date():
                year_month = current_date.strftime("%Y-%m")
                monthly_revenue[year_month] = 0
                next_month = current_date.month % 12 + 1
                next_year = current_date.year + (current_date.month // 12)
                current_date = current_date.replace(year=next_year, month=next_month, day=1)

            for row in rows:
                sale_date = datetime.strptime(row.date, "%d.%m.%Y")
                year_month = sale_date.strftime("%Y-%m")
                if year_month in monthly_revenue:
                    monthly_revenue[year_month] += row.total_revenue

        return monthly_revenue



class EntityRepository(EntityStoreRepository,
                       EntityGeneralRepository,
                       EntityProductRepository,
                       EntityCompanyRepository,
                       EntityOperationsRepository):
    pass
