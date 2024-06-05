from fastapi import FastAPI, HTTPException
from .flat_price_handler import FlatPriceHandler
import logging
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Counter, Histogram, Gauge
import psutil

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

app =FastAPI()

app.handler = FlatPriceHandler()

Instrumentator().instrument(app).expose(app)

# счетчик положительных предсказаний -значение больше 0 значит предсказание прошло успешно
total_requests = Counter('total_requests', 'Total number of requests')

# счетчик предсказаний цены 
successful_requests = Counter('successful_requests', 'Number of successful requests') 

# общие значения предсказаний
flat_app_predictions = Histogram('main_app_predictions', 'Prediction values')  

# измеритель ресурса памяти
memory_usage_gauge = Gauge('memory_usage', 'Memory usage of the application')

# измеритель ресурса cpu
cpu_usage_gauge = Gauge('cpu_usage', 'CPU usage of the application')

"""
Далее в Графане на основе этих метрик будет посчитана доля удачно обработанных запросов
через использование PromQL
rate(successful_requests[1m]) / rate(total_requests[1m])

"""

@app.post('/api/predict/')
def get_prediction(model_params: dict):
    try:
        prediction = app.handler.handle(model_params)
    except Exception as e:
        logging.error(f"Problem with request: {e}")
        raise HTTPException(status_code=500, detail=f'Problem with request: {e}')

    if 'predicted price' not in prediction:
        logging.error("Prediction does not contain 'predicted price'")
        raise HTTPException(status_code=500, detail='Prediction does not contain predicted price')
    total_requests.inc()
    if prediction['predicted price'] > 0:
            logging.info(f"Successful prediction: {prediction['predicted price']}")
            successful_requests.inc()
    
    memory_usage_gauge.set(psutil.virtual_memory().percent)  # Использование памяти
    cpu_usage_gauge.set(psutil.cpu_percent())  # Использование CPU

    return prediction
