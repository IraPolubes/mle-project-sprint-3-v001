import requests
import random
import time

url = 'http://localhost:8081/api/predict/'

def generate_random_data():
    """ Генерация случайных данных в формате ввода для предсказания. """
    return {
        "id": random.randint(1, 1000),
        "flat_id": random.uniform(0, 1),
        "building_id": random.uniform(1000, 7000),
        "floor": random.randint(1, 30),
        "is_apartment": random.choice([0, 1]),
        "kitchen_area": random.uniform(5, 20),
        "living_area": random.uniform(10, 50),
        "rooms": random.randint(1, 5),
        "studio": random.choice([0, 1]),
        "total_area": random.uniform(20, 100),
        "build_year": random.randint(1900, 2022),
        "building_type_int": random.randint(1, 10),
        "latitude": random.uniform(55.0, 56.0),
        "longitude": random.uniform(37.0, 38.0),
        "ceiling_height": random.uniform(2.0, 3.5),
        "flats_count": random.randint(1, 100),
        "floors_total": random.randint(1, 30),
        "has_elevator": random.choice([0, 1])
    }


def simulate_load(number_of_requests, delay_between_requests=0):
    """Отправка запросов в указанном количестве. """
    for _ in range(number_of_requests):
        data = generate_random_data()
        response = requests.post(url, json=data)
        print(f'Status Code: {response.status_code}, Prediction: {response.json()}')
        if delay_between_requests > 0:
            time.sleep(delay_between_requests)


if __name__ == '__main__':
    simulate_load(20,1)