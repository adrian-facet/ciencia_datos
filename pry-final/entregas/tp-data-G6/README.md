# Pipeline analítico de un minimercado

## Equipo tp-data-G6

- mellojorgepy
- 1534393
- adrian-facet

## Objetivo

Construir un pipeline reproducible que genere datos sintéticos de un minimercado, los cargue en DuckDB y permita analizarlos mediante modelos dbt.

## Instalación en Windows

Se requiere Python 3.11 o superior.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"

## Ejecución

```powershell
python generar_datos.py
python pipeline.py
python run_dbt.py build
pytest -q
dagster dev -f orchestration/definitions.py
```

## Rama y entrega

La rama de trabajo es `pyt/tp-data-G6`. Cada integrante registrará al menos tres commits significativos desde su propia cuenta. El equipo abrirá un Pull Request hacia `main`.
