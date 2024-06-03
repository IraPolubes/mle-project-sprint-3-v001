from fastapi import FastAPI, Body
from .flat_price_handler import FlatPriceHandler


app =FastAPI()

app.handler = FlatPriceHandler()

@app.post('/api/predict/')
def get_prediction(model_params: dict):
    return app.handler.handle(model_params)
