"""Pipeline de ingesta idempotente desde archivos CSV hacia DuckDB utilizando dlt."""

import csv
from pathlib import Path

import dlt

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = BASE_DIR / "data.duckdb"


def leer_csv(nombre_archivo: str):
    """Generador que lee un archivo CSV y produce diccionarios fila por fila."""
    ruta = DATA_DIR / nombre_archivo
    if not ruta.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {ruta}")
    with open(ruta, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        yield from reader


@dlt.resource(name="raw_productos", write_disposition="replace")
def cargar_productos():
    """Recurso dlt para productos."""
    yield from leer_csv("productos.csv")


@dlt.resource(name="raw_vendedores", write_disposition="replace")
def cargar_vendedores():
    """Recurso dlt para vendedores."""
    yield from leer_csv("vendedores.csv")


@dlt.resource(name="raw_compras", write_disposition="replace")
def cargar_compras():
    """Recurso dlt para compras."""
    yield from leer_csv("compras.csv")


@dlt.resource(name="raw_ventas", write_disposition="replace")
def cargar_ventas():
    """Recurso dlt para ventas."""
    yield from leer_csv("ventas.csv")


@dlt.resource(name="raw_movimientos_stock", write_disposition="replace")
def cargar_movimientos():
    """Recurso dlt para movimientos de stock."""
    yield from leer_csv("movimientos_stock.csv")


@dlt.source(name="fuente_minimercado")
def fuente_minimercado():
    """Fuente dlt que agrupa todos los recursos del minimercado."""
    return [
        cargar_productos(),
        cargar_vendedores(),
        cargar_compras(),
        cargar_ventas(),
        cargar_movimientos(),
    ]


def ejecutar_pipeline():
    """Ejecuta el pipeline de dlt hacia DuckDB."""
    print(f"Iniciando pipeline dlt hacia {DB_PATH.name}...")

    pipeline = dlt.pipeline(
        pipeline_name="minimercado_pipeline",
        destination=dlt.destinations.duckdb(str(DB_PATH)),
        dataset_name="raw_data",
    )

    info_carga = pipeline.run(fuente_minimercado())
    print("Carga dlt finalizada con éxito:")
    print(info_carga)
    return info_carga


if __name__ == "__main__":
    ejecutar_pipeline()
