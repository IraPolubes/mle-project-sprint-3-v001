import os
from joblib import load
import pandas as pd
from .constants import MODEL_PATH, REQUIRED_MODEL_PARAMS


class FlatPriceHandler:
    """
    Класс Handler, который обрабатывает запрос и возвращает предсказание.
    Пользовательский ввод проходит ту же обработку что и тренировочные данные через загруженный пайплайн.
    """
    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.pipeline_model_path = os.path.abspath(os.path.join(base_dir, MODEL_PATH))
        self.pipeline_model = None # инициализация

        # По результатам EDA нам не нужен studio, is_apartment, rooms, living_area, оставляем только те что использованы в обучении
        self.required_model_params = REQUIRED_MODEL_PARAMS
        self.num_cols = list(set(self.required_model_params) - set(['has_elevator']))
        self.load_model()

    def load_model(self):
        """Метод загрузки модели и пайплайна"""
        try:
            self.pipeline_model = load(self.pipeline_model_path)
        except ValueError as e:
            print(f"Failed to load model: {e}")

    def validate_query_params(self, query_params: dict):
        """Метод проверки есть ли все поля в запросе необходимые для модели"""
        required_params = set(self.required_model_params)
        given_params = set(query_params.keys())
        if required_params <= given_params:  # required_model_params is a subset of query_params
            return True
        else:
            raise ValueError(f"Missing parameters: {required_params - given_params}")


    def keep_training_params(self, user_params):
        """
        По итогам EDA 2го задания не все признаки из изначального сета использовались в тренировке модели.
        Выберем из нового пользовательского ввода только те что пригодились в тренировке.
        """
        selected_keys = [key for key in self.required_model_params if key in user_params]
        data = {key: [user_params[key]] for key in selected_keys}
        df = pd.DataFrame(data, columns=selected_keys)
        return df

    def handle(self, params):
        try:
            self.validate_query_params(params)
        except ValueError as e:
            print(f"Parameters do not correspond to expected.: {e}")
            return {'error': str(e)}
        
        model_params_df = self.keep_training_params(params)
        # Обработка входящих данных должна следовать пайплайну обработки тренировочных
        model_params_df[self.num_cols] = self.remove_outliers(model_params_df)  
        price_prediction = self.pipeline_model.predict(model_params_df)
        y_pred = price_prediction[0]
        response = {'predicted price':y_pred}
        return response
    
    def remove_outliers(self, df):
        threshold = 1.5
        df_num = df[self.num_cols].copy()
        for col in self.num_cols:
            Q1 = df_num[col].quantile(0.25)
            Q3 = df_num[col].quantile(0.75)
            IQR = Q3 - Q1
            margin = threshold * IQR
            lower = Q1 - margin
            upper = Q3 + margin
            mask = df_num[col].between(lower, upper)
            df_num = df_num[mask]
        return df_num


if __name__ == '__main__':
    # тестовый запрос
    data = {
        'id': 802,
        'flat_id': 0.0,
        'building_id': 6220.0,
        'floor': 9,
        'is_apartment': 0,
        'kitchen_area': 9.9,
        'living_area': 19.9,
        'rooms': 1,
        'studio': 0,
        'total_area': 35.1,
        'build_year': 1965,
        'building_type_int': 6,
        'latitude': 55.717113,
        'longitude': 37.781120,
        'ceiling_height': 2.64,
        'flats_count': 84,
        'floors_total': 12,
        'has_elevator': 1
    }

    # обработчик запросов для API
    handler = FlatPriceHandler()

    # делаем тестовый запрос
    response = handler.handle(data)
    print(f"Response: {response}")
