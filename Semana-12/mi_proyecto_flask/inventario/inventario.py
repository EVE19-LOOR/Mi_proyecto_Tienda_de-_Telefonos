import os
import json
import csv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

TXT_FILE = os.path.join(DATA_DIR, "datos.txt")
JSON_FILE = os.path.join(DATA_DIR, "datos.json")
CSV_FILE = os.path.join(DATA_DIR, "datos.csv")


def guardar_txt(producto):

    with open(TXT_FILE, "a", encoding="utf-8") as f:
        f.write(
            f"{producto['nombre']},{producto['marca']},{producto['precio']},{producto['cantidad']}\n"
        )


def guardar_json(producto):

    datos = []

    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            try:
                datos = json.load(f)
            except json.JSONDecodeError:
                datos = []

    datos.append(producto)

    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)


def guardar_csv(producto):

    archivo_vacio = (not os.path.exists(CSV_FILE)) or os.path.getsize(CSV_FILE) == 0

    with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:

        writer = csv.writer(f)

        if archivo_vacio:
            writer.writerow(["nombre", "marca", "precio", "cantidad"])

        writer.writerow(
            [
                producto["nombre"],
                producto["marca"],
                producto["precio"],
                producto["cantidad"],
            ]
        )


def leer_txt():

    if not os.path.exists(TXT_FILE):
        return []

    with open(TXT_FILE, "r", encoding="utf-8") as f:
        return f.readlines()


def leer_json():

    if not os.path.exists(JSON_FILE):
        return []

    with open(JSON_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def leer_csv():

    if not os.path.exists(CSV_FILE):
        return []

    datos = []

    with open(CSV_FILE, "r", encoding="utf-8") as f:

        reader = csv.DictReader(f)

        for fila in reader:
            datos.append(fila)

    return datos