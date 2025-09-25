from fastapi import FastAPI, Header, HTTPException, Depends
import joblib
from sklearn.neighbors import NearestNeighbors
import numpy
import pandas as pd
from pydantic import BaseModel
import os

API_KEY = os.environ['API_KEY']

def verify_api_key(x_api_key : str = Header(None, alias="X-API-KEY")):
    if API_KEY is None:
        # no API key configured, open mode for dev, or you can force error here
        return
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Forbidden")

class Item(BaseModel):
    inp: list

app = FastAPI()

knn = joblib.load('knn.pkl')

@app.post("/predict")
def predict(data : Item, _=Depends(verify_api_key)):
    columnNames = ['popularity', 'duration_ms', 'explicit', 'danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'time_signature']
    s = pd.Series(data.inp, index=columnNames)
    dists, indices = knn.kneighbors([s], n_neighbors=9)
    return {"output": indices[0].tolist()}

@app.post("/test")
def test(a : int, _=Depends(verify_api_key)):
    return a+5