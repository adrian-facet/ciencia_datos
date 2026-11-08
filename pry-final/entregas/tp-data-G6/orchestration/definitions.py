"""Assets de Dagster para el pipeline del minimercado."""
import os
import subprocess
import sys
from pathlib import Path

import duckdb
from dagster import Definitions, asset

BASE_DIR = Path(__file__).resolve().parents[1]
DBT_DIR = BASE_DIR / "dbt_project"
DB_PATH = BASE_DIR / "data.duckdb"


def ejecutar(
    comando: list[str],
    directorio: Path,
    context,
    entorno: dict[str, str] | None = None,
) -> None:
    """Ejecuta un comando y detiene el asset si ocurre un error."""
    context.log.info(f"Ejecutando: {' '.join(comando)}")
    subprocess.run(
        comando,
        cwd=directorio,
        check=True,
        env=entorno,
    )


@asset
def generar_datos_asset(context) -> str:
    """Genera los archivos CSV sintéticos."""
    ejecutar(
        [sys.executable, "generar_datos.py"],
        BASE_DIR,
        context,
    )
    return "CSV generados en data/"


@asset
def ingesta_dlt_asset(context, generar_datos_asset: str) -> str:
    """Carga los CSV en DuckDB mediante dlt."""
    ejecutar(
        [sys.executable, "pipeline.py"],
        BASE_DIR,
        context,
    )
    return str(DB_PATH)


@asset
def dbt_transformations_asset(
    context,
    ingesta_dlt_asset: str,
) -> str:
    """Ejecuta los modelos y pruebas de dbt."""
    entorno = os.environ.copy()
    entorno["DUCKDB_PATH"] = str(DB_PATH)

    ejecutar(
        [
            "dbt",
            "build",
            "--project-dir",
            str(DBT_DIR),
            "--profiles-dir",
            str(DBT_DIR),
        ],
        BASE_DIR,
        context,
        entorno=entorno,
    )
    return "Modelos y pruebas de dbt ejecutados"


@asset
def reporte_calidad_asset(
    context,
    dbt_transformations_asset: str,
) -> dict[str, int]:
    """Comprueba que existan las tablas requeridas y que tengan datos."""
    if not DB_PATH.exists():
        raise FileNotFoundError(f"No se encontró la base DuckDB: {DB_PATH}")

    tablas_requeridas = {
        ("raw_data", "raw_productos"),
        ("raw_data", "raw_vendedores"),
        ("raw_data", "raw_compras"),
        ("raw_data", "raw_ventas"),
        ("raw_data", "raw_movimientos_stock"),
        ("marts", "mart_ventas_diarias"),
        ("marts", "mart_rentabilidad_productos"),
        ("marts", "mart_rotacion_inventario"),
        ("marts", "mart_desempeno_vendedores"),
    }

    conexion = duckdb.connect(str(DB_PATH), read_only=True)

    try:
        tablas_disponibles = {
            (fila[0].lower(), fila[1].lower())
            for fila in conexion.execute(
                """
                SELECT table_schema, table_name
                FROM information_schema.tables
                """
            ).fetchall()
        }

        faltantes = tablas_requeridas - tablas_disponibles
        if faltantes:
            nombres = [f"{esquema}.{tabla}" for esquema, tabla in sorted(faltantes)]
            raise ValueError(
                f"Faltan tablas en DuckDB: {', '.join(nombres)}"
            )

        conteos = {}
        for esquema, tabla in sorted(tablas_requeridas):
            cantidad = conexion.execute(
                f'SELECT COUNT(*) FROM "{esquema}"."{tabla}"'
            ).fetchone()[0]

            if cantidad == 0:
                raise ValueError(f"La tabla {esquema}.{tabla} está vacía")

            conteos[f"{esquema}.{tabla}"] = cantidad
    finally:
        conexion.close()

    context.log.info(f"Control de calidad aprobado: {conteos}")
    return conteos


defs = Definitions(
    assets=[
        generar_datos_asset,
        ingesta_dlt_asset,
        dbt_transformations_asset,
        reporte_calidad_asset,
    ]
)