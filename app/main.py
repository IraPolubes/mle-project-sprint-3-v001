import os
from fastapi import FastAPI, HTTPException
from .flat_price_handler import FlatPriceHandler
import logging
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

# счетчик положительных предсказаний -значение больше 0 значит предсказание прошло успешно
total_requests = Counter('total_requests', 'Total number of requests')

# счетчик предсказаний цены 
successful_requests = Counter('successful_requests', 'Number of successful requests') 

# общие значения предсказаний
flat_app_predictions = Histogram(
    'flat_app_predictions',
    'Prediction values',
    buckets=(10000000, 20000000, 30000000, 40000000, 50000000, 60000000, 70000000, 80000000, 90000000, 100000000, 110000000, 120000000, 130000000)
)
# измеритель ресурса памяти
memory_usage_gauge = Gauge('memory_usage', 'Memory usage of the application')

# измеритель ресурса cpu
cpu_usage_gauge = Gauge('cpu_usage', 'CPU usage of the application')

"""
Далее в Графане на основе этих метрик будет посчитана доля удачно обработанных запросов
через использование PromQL
rate(successful_requests_total[10m]) / rate(total_requests_total[10m])

Остальные метрики не требуют рассчета через PromQL и будут выбраны из интерфейса Графаны в привязке
к Прометеус.

"""

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

    total_requests.inc()
    if prediction['predicted price'] > 0:
        logger.info(f"Successful prediction: {prediction['predicted price']}")
        flat_app_predictions.observe(prediction['predicted price'])
        successful_requests.inc()
    
    memory_usage_gauge.set(psutil.virtual_memory().percent)
    cpu_usage_gauge.set(psutil.cpu_percent())

    return prediction