import pandas
import matplotlib
import csv
import os

def salva_parametros_resultados(data, filename, headers=None):
    file_exists = os.path.exists(filename)
    file_empty = not file_exists or os.path.getsize(filename) == 0
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        if headers and file_empty:
            writer.writerow(headers)
        writer.writerows(data)

def carrega_dados_csv(filename):
    return pandas.read_csv(filename)
    