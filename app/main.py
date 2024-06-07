import os
from fastapi import FastAPI, HTTPException
from .flat_price_handler import FlatPriceHandler
import logging
import numpy as np
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Counter, Histogram, Gauge
import psutil

log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Настройка логирования в файл
log_file = os.path.join(log_dir, "app.log")
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s",
                    handlers=[
                        logging.FileHandler(log_file),
                        logging.StreamHandler()
                    ])
logger = logging.getLogger(__name__)

app =FastAPI()

app.handler = FlatPriceHandler()

Instrumentator().instrument(app).expose(app)

class Metrics():
    """
    Класс метрик для обработчика.
    Далее в Графане на основе этих метрик будет посчитана доля удачно обработанных запросов
    через использование PromQL
    rate(successful_requests_total[10m]) / rate(total_requests_total[10m])

    Остальные метрики не требуют рассчета через PromQL и будут выбраны из интерфейса Графаны в привязке
    к Прометеус.
    """
    
    def __init__(self):
        # счетчик положительных предсказаний -значение больше 0 значит предсказание прошло успешно
        self.total_requests = Counter('total_requests', 'Total number of requests')

        # счетчик предсказаний цены 
        self.successful_requests = Counter('successful_requests', 'Number of successful requests') 

        # общие значения предсказаний
        self.flat_app_predictions = Histogram(
            'flat_app_predictions',
            'Prediction values',
            buckets = np.arange(10e6, 13e7, 10e6).astype(int)
            )
        # измеритель ресурса памяти
        self.memory_usage_gauge = Gauge('memory_usage', 'Memory usage of the application')

        # измеритель ресурса cpu
        self.cpu_usage_gauge = Gauge('cpu_usage', 'CPU usage of the application')
 

metrics = Metrics()

@app.post('/api/predict/')
def get_prediction(model_params: dict):
    try:
        prediction = app.handler.handle(model_params)
    except Exception as e:
        logger.error(f"Problem with request: {e}")
        raise HTTPException(status_code=500, detail=f'Problem with request: {e}')

    if 'predicted price' not in prediction:
        logger.error("Prediction does not contain 'predicted price'")
        raise HTTPException(status_code=500, detail='Prediction does not contain predicted price')

    metrics.total_requests.inc()
    if prediction['predicted price'] > 0:
        logger.info(f"Successful prediction: {prediction['predicted price']}")
        metrics.flat_app_predictions.observe(prediction['predicted price'])
        metrics.successful_requests.inc()
    
    metrics.memory_usage_gauge.set(psutil.virtual_memory().percent)
    metrics.cpu_usage_gauge.set(psutil.cpu_percent())

    return prediction