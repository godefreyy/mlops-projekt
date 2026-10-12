
# MLOps Projekt

Przedmiot: Infrastruktura i architektura chmurowa dla systemów sztucznej inteligencji

Numer albumu: 99801

## Laboratorium 1

Organizacja projektu uczenia maszynowego:
zarządzanie środowiskiem i wersjonowanie danych.

### Ćwiczenie samodzielne 1 – Porównanie narzędzi

| Narzędzie | Czas | Plik zależności | Odtworzenie | Zastosowanie |
|---|---|---|---|---|
| venv + pip | 26,38 s | requirements.txt | `python -m venv .venv`, `pip install -r requirements.txt` | Proste projekty Python |
| UV | 3,88 s | requirements.txt | `uv venv`, `uv pip install -r requirements.txt` | Szybka instalacja pakietów |
| Conda | 5,62 s | environment.yml | `conda env create -f environment.yml` | Projekty ML i zależności systemowe |
| DVC | – | .dvc | `dvc pull` | Wersjonowanie danych |

**Wnioski:**

UV był najszybszy podczas testów. Przy ponownej instalacji z cache uzyskał 1,30 s. Conda również korzystała z cache, więc czasy są orientacyjne.

Venv jest prosty w użyciu, a Conda przydaje się w bardziej rozbudowanych projektach ML. DVC służy do wersjonowania danych, natomiast Git do wersjonowania kodu i plików opisujących dane.