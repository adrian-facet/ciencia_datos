import pipeline
import pytest


def test_leer_csv_devuelve_filas_como_diccionarios(tmp_path, monkeypatch):
    archivo = tmp_path / "productos.csv"
    archivo.write_text(
        "producto_id,nombre\n1,Leche\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(pipeline, "DATA_DIR", tmp_path)

    filas = list(pipeline.leer_csv("productos.csv"))

    assert filas == [{"producto_id": "1", "nombre": "Leche"}]


def test_leer_csv_avisa_si_no_existe_el_archivo(tmp_path, monkeypatch):
    monkeypatch.setattr(pipeline, "DATA_DIR", tmp_path)

    with pytest.raises(FileNotFoundError, match="No se encontró el archivo"):
        list(pipeline.leer_csv("inexistente.csv"))