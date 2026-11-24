
import os
from pathlib import Path
from contextlib import asynccontextmanager

import mlflow.sklearn
import numpy as np
import yaml
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from src import db

SCIEZKA_KONFIGURACJI = Path(__file__).resolve().parent.parent / "config.yaml"

with open(SCIEZKA_KONFIGURACJI, encoding="utf-8") as plik:
    KONFIGURACJA = yaml.safe_load(plik)

MLFLOW_URI = os.getenv(
    "MLFLOW_URI", KONFIGURACJA["mlflow"]["tracking_uri"]
)
NAZWA_MODELU = KONFIGURACJA["model"]["nazwa"]
ALIAS_MODELU = KONFIGURACJA["model"]["alias"]
LICZBA_CECH = KONFIGURACJA["model"]["liczba_cech"]

class ZadaniePredykcji(BaseModel):
    cechy: list[float] = Field(
        ...,
        min_length=LICZBA_CECH,
        max_length=LICZBA_CECH,
        description="Wektor cech pojedynczej obserwacji",
    )

class OdpowiedzPredykcji(BaseModel):
    klasa: int = Field(description="Przewidziana etykieta klasy")
    prawdopodobienstwo: float = Field(
        ge=0.0,
        le=1.0,
        description="Prawdopodobienstwo przewidzianej klasy",
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    mlflow.set_tracking_uri(MLFLOW_URI)

    app.state.model = mlflow.sklearn.load_model(
        f"models:/{NAZWA_MODELU}@{ALIAS_MODELU}"
    )

    app.state.db_dsn = db.pobierz_dsn()

    if app.state.db_dsn:
        db.inicjalizuj_baze(app.state.db_dsn)
    else:
        print(
            "Ostrzezenie: brak DATABASE_URL, "
            "historia predykcji nie bedzie zapisywana"
        )

    yield

    app.state.model = None

app = FastAPI(
    title="API projektu semestralnego",
    description="Serwowanie modelu klasyfikacyjnego z rejestru MLflow",
    version="1.0.0",
    lifespan=lifespan,
)

@app.get("/health")
def health():
    model_zaladowany = getattr(app.state, "model", None) is not None
    return {"status": "ok", "model_zaladowany": model_zaladowany}


@app.post("/predict", response_model=OdpowiedzPredykcji)
def predict(zadanie: ZadaniePredykcji):
    obserwacja = np.array(zadanie.cechy).reshape(1, -1)

    klasa = int(app.state.model.predict(obserwacja)[0])
    prawdopodobienstwa = app.state.model.predict_proba(obserwacja)[0]

    if app.state.db_dsn:
        db.zapisz_predykcje(
            app.state.db_dsn, zadanie.cechy, klasa
        )

    return OdpowiedzPredykcji(
        klasa=klasa,
        prawdopodobienstwo=float(prawdopodobienstwa[klasa]),
    )

@app.get("/history")
def historia(limit: int = 10):
    if not app.state.db_dsn:
        raise HTTPException(
            status_code=503,
            detail="Baza danych nie jest skonfigurowana",
        )

    return {
        "rekordy": db.pobierz_historie(app.state.db_dsn, limit)
    }