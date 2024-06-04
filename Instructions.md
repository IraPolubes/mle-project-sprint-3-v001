# Инструкции по запуску микросервиса

### 1. FastAPI микросервис в виртуальном окружение

python3 -m venv venv
source venv/bin/activate/
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8081 --host 0.0.0.0

curl -X 'POST' \
  'http://0.0.0.0:8081/api/predict/' \
  -H 'accept: application/json' \
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
}
'

### 2. FastAPI микросервис в Docker-контейнере
## С помощью Dockerfile:

Строим образ:
docker image build . --tag flat_predict_api:1.0

Запуск:
docker container run \
--publish 8081:8081 \
--volume=./models:/flat_predict_api/models \
--env-file .env \
flat_predict_api:1.0

ПРИМЕЧАНИЕ: мне удобней локально работать у себя а не на VM
поэтому порты не отличаются, но оставила в команде для наглядности, что если что - можно менять

## С помощью Docker compose:
Собираем и запускаем одной командой
docker compose up flat_predict_app --build

Обращаемся к сервису:  !!!!!!!!!!!!!!!! какой порт тут указать??
curl -X 'POST' \
  'http://localhost:4649/api/predict/' \
  -H 'accept: application/json' \
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
}
'