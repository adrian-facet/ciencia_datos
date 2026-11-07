"""Módulo de generación de datos sintéticos reproducibles para el Minimercado."""

import csv
import random
from datetime import date, timedelta
from pathlib import Path

# Semilla fija para garantizar reproducibilidad exacta
SEED = 42
random.seed(SEED)

DATA_DIR = Path(__file__).resolve().parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)


def generar_productos():
    """Genera 20 productos representativos de un minimercado."""
    categorias = {
        "Bebidas": [
            ("Gaseosa Coca-Cola 1.5L", 900.0, 1500.0, 60),
            ("Agua Mineral 2L", 400.0, 750.0, 80),
            ("Cerveza Pilsen 1L", 1100.0, 1800.0, 50),
            ("Jugo Frutika 1L", 700.0, 1200.0, 40),
        ],
        "Almacén": [
            ("Fideos Spaghetti 500g", 500.0, 850.0, 100),
            ("Arroz 1kg", 650.0, 1100.0, 90),
            ("Aceite de Girasol 900ml", 1200.0, 2000.0, 45),
            ("Harina de Trigo 000 1kg", 450.0, 750.0, 70),
            ("Azúcar Común 1kg", 550.0, 900.0, 65),
            ("Café Molido 250g", 1800.0, 2900.0, 30),
        ],
        "Lácteos": [
            ("Leche Entera 1L", 600.0, 1000.0, 80),
            ("Yogurt Trébol 1L", 950.0, 1600.0, 35),
            ("Queso Cremoso 500g", 2200.0, 3500.0, 25),
            ("Manteca 200g", 1100.0, 1750.0, 30),
        ],
        "Limpieza": [
            ("Detergente Vajilla 500ml", 800.0, 1350.0, 50),
            ("Lavandina Común 1L", 500.0, 850.0, 60),
            ("Jabón Líquido Ropa 800ml", 1500.0, 2400.0, 30),
            ("Papel Higiénico 4u", 900.0, 1450.0, 75),
        ],
        "Golosinas": [
            ("Alfajor", 350.0, 600.0, 120),
            ("Galletitas Rellenas 150g", 600.0, 1050.0, 85),
        ],
    }

    productos = []
    prod_id = 1
    for cat, items in categorias.items():
        for nombre, costo, precio, stock in items:
            productos.append(
                {
                    "id": prod_id,
                    "nombre": nombre,
                    "categoria": cat,
                    "costo_unitario": costo,
                    "precio_venta": precio,
                    "stock_inicial": stock,
                }
            )
            prod_id += 1
    return productos


def generar_vendedores():
    """Genera 5 vendedores asignados a sucursales."""
    return [
        {"id": 1, "nombre": "Carlos Gómez", "sucursal": "Centro", "fecha_alta": "2026-01-10"},
        {"id": 2, "nombre": "María Rodríguez", "sucursal": "Centro", "fecha_alta": "2026-01-15"},
        {"id": 3, "nombre": "Lucas Fernández", "sucursal": "Norte", "fecha_alta": "2026-02-01"},
        {"id": 4, "nombre": "Sofía Martínez", "sucursal": "Norte", "fecha_alta": "2026-02-10"},
        {"id": 5, "nombre": "Javier López", "sucursal": "Sur", "fecha_alta": "2026-02-20"},
    ]


def generar_compras_ventas_movimientos(productos, vendedores, fecha_inicio, dias=90):
    """Genera compras, ventas y trazabilidad de movimientos de stock con consistencia temporal."""
    proveedores = ["Distribuidora Central", "Molinos del Plata", "Lácteos del Sur", "Química Total"]
    compras = []
    ventas = []
    movimientos = []

    compra_id = 1
    venta_id = 1
    mov_id = 1

    stock_actual = {p["id"]: p["stock_inicial"] for p in productos}
    mapa_costos = {p["id"]: p["costo_unitario"] for p in productos}
    mapa_precios = {p["id"]: p["precio_venta"] for p in productos}

    # Registro de stock inicial en movimientos
    for p in productos:
        movimientos.append(
            {
                "id": mov_id,
                "fecha": fecha_inicio.isoformat(),
                "producto_id": p["id"],
                "tipo_movimiento": "STOCK_INICIAL",
                "cantidad": p["stock_inicial"],
                "referencia_id": 0,
            }
        )
        mov_id += 1

    for dia_idx in range(dias):
        fecha_actual = fecha_inicio + timedelta(days=dia_idx)
        fecha_str = fecha_actual.isoformat()

        # Efecto fin de semana
        es_fin_de_semana = fecha_actual.weekday() in [4, 5, 6]
        num_ventas_dia = random.randint(7, 12) if es_fin_de_semana else random.randint(4, 8)

        # 1. Compras cada 3 días
        if dia_idx % 3 == 0:
            productos_a_comprar = random.sample(productos, k=random.randint(3, 5))
            for p in productos_a_comprar:
                cant_compra = random.randint(20, 50)
                costo = mapa_costos[p["id"]]
                prov = random.choice(proveedores)

                compras.append(
                    {
                        "id": compra_id,
                        "fecha": fecha_str,
                        "producto_id": p["id"],
                        "cantidad": cant_compra,
                        "costo_unitario": costo,
                        "proveedor": prov,
                    }
                )
                stock_actual[p["id"]] += cant_compra

                movimientos.append(
                    {
                        "id": mov_id,
                        "fecha": fecha_str,
                        "producto_id": p["id"],
                        "tipo_movimiento": "ENTRADA_COMPRA",
                        "cantidad": cant_compra,
                        "referencia_id": compra_id,
                    }
                )
                mov_id += 1
                compra_id += 1

        # 2. Ventas del día
        for _ in range(num_ventas_dia):
            prod = random.choice(productos)
            p_id = prod["id"]
            if stock_actual[p_id] <= 0:
                continue

            cant_maxima = min(stock_actual[p_id], 6)
            if cant_maxima < 1:
                continue
            cant_venta = random.randint(1, cant_maxima)

            vendedor = random.choice(vendedores)
            precio_base = mapa_precios[p_id]
            descuento = (
                round(precio_base * random.choice([0.05, 0.10]), 2)
                if random.random() < 0.15
                else 0.0
            )

            ventas.append(
                {
                    "id": venta_id,
                    "fecha": fecha_str,
                    "producto_id": p_id,
                    "cantidad": cant_venta,
                    "precio_unitario": precio_base,
                    "descuento": descuento,
                    "vendedor_id": vendedor["id"],
                }
            )
            stock_actual[p_id] -= cant_venta

            movimientos.append(
                {
                    "id": mov_id,
                    "fecha": fecha_str,
                    "producto_id": p_id,
                    "tipo_movimiento": "SALIDA_VENTA",
                    "cantidad": cant_venta,
                    "referencia_id": venta_id,
                }
            )
            mov_id += 1
            venta_id += 1

    return compras, ventas, movimientos


def guardar_csv(nombre_archivo, lista_dicts):
    """Guarda una lista de diccionarios en formato CSV."""
    if not lista_dicts:
        return
    ruta = DATA_DIR / nombre_archivo
    claves = lista_dicts[0].keys()
    with open(ruta, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=claves)
        writer.writeheader()
        writer.writerows(lista_dicts)
    print(f"Generado: {ruta.name} ({len(lista_dicts)} registros)")


def main():
    """Punto de entrada principal para generar los datos sintéticos."""
    print("Iniciando generación de datos sintéticos con semilla fija...")
    fecha_inicio = date(2026, 8, 1)

    productos = generar_productos()
    vendedores = generar_vendedores()
    compras, ventas, movimientos = generar_compras_ventas_movimientos(
        productos, vendedores, fecha_inicio, dias=90
    )

    guardar_csv("productos.csv", productos)
    guardar_csv("vendedores.csv", vendedores)
    guardar_csv("compras.csv", compras)
    guardar_csv("ventas.csv", ventas)
    guardar_csv("movimientos_stock.csv", movimientos)

    print("\nResumen generado:")
    print(f"- Productos: {len(productos)} (requerido: 20)")
    print(f"- Vendedores: {len(vendedores)} (requerido: 5)")
    print(f"- Compras: {len(compras)} (requerido: >= 100)")
    print(f"- Ventas: {len(ventas)} (requerido: >= 500)")
    print(f"- Movimientos: {len(movimientos)}")


if __name__ == "__main__":
    main()
