from sqlalchemy import select, func, cast, Date
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from model.database import sessionLocal
from model import models

class SalesRepository:

    @staticmethod
    async def get_sales_data_for_forecast(product_id: int, start_date: datetime, end_date: datetime):
        async with sessionLocal() as sess:
            query = select(
                models.Sale.date,
                func.sum(models.InfoAboutSale.amount).label('total_amount')
            ).join(
                models.Sale, models.InfoAboutSale.idSale == models.Sale.id
            ).where(
                models.InfoAboutSale.idProduct == product_id,
                cast(models.Sale.date, Date) >= start_date.date(),
                cast(models.Sale.date, Date) <= end_date.date()
            ).group_by(
                models.Sale.date
            ).order_by(
                models.Sale.date
            )

            result = await sess.execute(query)
            rows = result.all()

            sales_data = []
            for row in rows:
                sales_data.append({
                    "date": row.date,
                    "total_amount": float(row.total_amount)
                })

        return sales_data

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
import numpy as np
import pandas as pd

class ForecastModel:

    @staticmethod
    def create_forecast_model(input_shape):
        model = Sequential()
        model.add(LSTM(50, activation='relu', input_shape=input_shape))
        model.add(Dense(1))
        model.compile(optimizer='adam', loss='mse')
        return model

    @staticmethod
    def train_forecast_model(sales_data, epochs=50, batch_size=32):
        # Подготовка данных
        try:
            dates = [datetime.strptime(d["date"], "%d.%m.%Y") for d in sales_data]
            amounts = [float(d["total_amount"]) for d in sales_data]

            data = pd.DataFrame({"date": dates, "amount": amounts})
            data.set_index("date", inplace=True)

            data = data.asfreq('D').fillna(0)

            X = []
            y = []

            # Проверка, что данных достаточно для создания истории в 30 дней
            if len(data) < 30:
                raise ValueError("Данных недостаточно для создания истории в 30 дней")

            for i in range(30, len(data)):
                X.append(data["amount"].values[i - 30:i])
                y.append(data["amount"].values[i])

            X = np.array(X)
            y = np.array(y)
            X = X.reshape((X.shape[0], X.shape[1], 1))
            model = ForecastModel.create_forecast_model((X.shape[1], X.shape[2]))
            model.fit(X, y, epochs=epochs, batch_size=batch_size, verbose=0)

            return model
        except Exception as e:
            raise ValueError(f"Ошибка при подготовке или обучении модели: {e}")

    @staticmethod
    def predict_sales(model, last_30_days_data):
        try:
            last_30_days_data = np.array(last_30_days_data).reshape((1, 30, 1))
            prediction = model.predict(last_30_days_data)[0][0]
            return float(prediction)
        except Exception as e:
            raise ValueError(f"Ошибка при прогнозировании: {e}")