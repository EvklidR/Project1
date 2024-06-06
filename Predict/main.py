from fastapi import FastAPI, HTTPException
from datetime import datetime, timedelta
from typing import List

from model.CRUD import SalesRepository, ForecastModel

app = FastAPI()

@app.get("/predict/{product_id}")
async def predict_sales(product_id: int):
    # Определяем период для извлечения данных (например, последние 6 месяцев)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=360)

    sales_data = await SalesRepository.get_sales_data_for_forecast(product_id, start_date, end_date)
    print(sales_data)
    if not sales_data or len(sales_data) < 50:
        return None

    model = ForecastModel.train_forecast_model(sales_data)


    # Берем последние 30 дней данных для прогнозирования
    last_30_days_data = [d["total_amount"] for d in sales_data[-30:]]

    forecast = []
    for _ in range(90):  # Прогнозируем на следующие 90 дней
        prediction = ForecastModel.predict_sales(model, last_30_days_data)

        forecast.append(prediction)

        # Обновляем данные последних 30 дней, добавляя новый прогноз и удаляя самый старый день
        last_30_days_data.append(prediction)
        last_30_days_data = last_30_days_data[1:]

    return {"forecast": forecast}
