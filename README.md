
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





### Ćwiczenie samodzielne 2 – DVC Remote

Utworzono drugi magazyn DVC na Dysku Google o nazwie `google-drive`.

Do wersjonowania dodano zbiór `iris.csv` za pomocą `dvc add data/iris.csv`.

Dane przesłano poleceniem `dvc push data/iris.csv.dvc -r google-drive`.

Przesyłanie zakończyło się sukcesem (`1 file pushed`). Ponowne wykonanie polecenia zwróciło `Everything is up to date`.




### Ćwiczenie samodzielne 3 – Odtworzenie projektu

W ramach testu sklonowano własne repozytorium do folderu `mlops-test`.

Środowisko odtworzono za pomocą:
- `uv venv --python 3.12`
- `uv pip install -r requirements.txt`

Zainstalowano 124 pakiety. Następnie odtworzono dane `housing.csv` i `iris.csv` za pomocą `dvc pull`.

**Napotkane problemy:** Początkowo UV korzystał z niewłaściwego środowiska. Rozwiązaniem było wskazanie interpretera przez `--python`. Dostęp do Google Drive wymagał również lokalnej konfiguracji OAuth.

Ostatecznie środowisko i oba zbiory danych zostały poprawnie odtworzone.