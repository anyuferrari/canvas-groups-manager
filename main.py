import csv
from datetime import datetime

import yaml

from Controllers.canvas_controller import Canvas
from category_creator import CategoriesCreator
from groups_assigner import GroupsAssigner
from groups_creator import GroupsCreator

with open("credentials.yml", 'r') as file:
    credentials = yaml.safe_load(file)

if __name__ == '__main__':
    print("Iniciando la asignación de grupos")
    canvas = Canvas()
    i = 0
    with open('input.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        headers = next(reader)
        courses = [row[0] for row in reader]
    ping = datetime.now()
    print("Paso 1: creando categorías de grupos")
    categories = CategoriesCreator(courses)
    print(f"Se crearon {categories.i} categorías")
    print("Paso 2: creando grupos vacíos")
    created_groups = GroupsCreator(courses)
    print(f"Se crearon {created_groups.i} grupos")
    print("Paso 3: Asignando grupos")
    assigned = GroupsAssigner(courses)
    i += assigned.m
    print(f'Se han asignado {i} alumnos a sus grupos')
    pong = datetime.now()
    delta = pong - ping
    print(f'Tiempo de ejecución: {(pong - ping).seconds} segundos')
