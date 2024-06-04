# Инструкции по запуску микросервиса

### 1. FastAPI микросервис в виртуальном окружение

Выполняем следующую последовательность комманд из корневой папки проекта:
python3 -m venv venv
source venv/bin/activate/
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8081 --host 0.0.0.0

Затем обращаемся к сервису из корневой папки проекта: 
запускаем следующий curl в терминале и нажимаем Enter чтобы получить результат:


curl -X POST 'http://localhost:8081/api/predict/' \
-H 'Content-Type: application/json' \
-d '{
    "id": 802,
    "flat_id": 0.0,
    "building_id": 6220.0,
    "floor": 9,
    "is_apartment": 0,
    "kitchen_area": 9.9,
    "living_area": 19.9,
    "rooms": 1,
    "studio": 0,
    "total_area": 35.1,
    "build_year": 1965,
    "building_type_int": 6,
    "latitude": 55.717113,
    "longitude": 37.781120,
    "ceiling_height": 2.64,
    "flats_count": 84,
    "floors_total": 12,
    "has_elevator": 1
}'

### 2. FastAPI микросервис в Docker-контейнере
## С помощью Dockerfile:

Строим образ, выполняя в терминале команду из корневой папки проекта:
docker build -f services/Dockerfile_ml_service -t flat_predict_api:1.0 .

Запуск из терминала корневой папки проекта, подключая переменные из .env:
docker run -d -p 8081:8081 --env-file .env flat_predict_api:1.0

ПРИМЕЧАНИЕ: порты одинаковы так как видела в уроке в теории что в продакшене так делают

Затем при запущенном контейнере запускаем следующий curl в терминале и нажимаем Enter чтобы получить результат:

curl -X POST 'http://localhost:8081/api/predict/' \
-H 'Content-Type: application/json' \
-d '{
    "id": 802,
    "flat_id": 0.0,
    "building_id": 6220.0,
    "floor": 9,
    "is_apartment": 0,
    "kitchen_area": 9.9,
    "living_area": 19.9,
    "rooms": 1,
    "studio": 0,
    "total_area": 35.1,
    "build_year": 1965,
    "building_type_int": 6,
    "latitude": 55.717113,
    "longitude": 37.781120,
    "ceiling_height": 2.64,
    "flats_count": 84,
    "floors_total": 12,
    "has_elevator": 1
}'


## С помощью Docker compose:
Собираем и запускаем одной командой
docker compose -f services/docker-compose.yaml up --build

Обращаемся к сервису: 
запускаем следующий curl в терминале и нажимаем Enter чтобы получить результат


curl -X POST 'http://localhost:8081/api/predict/' \
-H 'Content-Type: application/json' \
-d '{
    "id": 802,
    "flat_id": 0.0,
    "building_id": 6220.0,
    "floor": 9,
    "is_apartment": 0,
    "kitchen_area": 9.9,
    "living_area": 19.9,
    "rooms": 1,
    "studio": 0,
    "total_area": 35.1,
    "build_year": 1965,
    "building_type_int": 6,
    "latitude": 55.717113,
    "longitude": 37.781120,
    "ceiling_height": 2.64,
    "flats_count": 84,
    "floors_total": 12,
    "has_elevator": 1
}'



После запуска docker-compose сервисы находятся по следующим адресам после того как добавить в VisualStudio Code перенаправление портов 1702, 8081, 9090 через Ports в терминале:

Microservice: http://localhost:8081/docs
Prometheus metrics: http://localhost:9090/metrics
Prometheus UI: http://localhost:9090/
Grafana:

Завершить работу докера из корневой папки проекта:
docker compose -f services/docker-compose.yaml down