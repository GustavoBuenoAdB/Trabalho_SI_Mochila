import pandas
import matplotlib.pyplot as plt
import seaborn
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


def gera_grafico_tempo_pesoLimite(df):
    plt.figure(figsize=(10,5))
    plt.plot(df['Peso Máximo'], df['Tempo de execução'], marker='o')
    plt.xlabel('Peso Máximo')
    plt.ylabel('Tempo de execução')
    plt.title('Comparação: Tempo de Execução vs Peso Máximo')
    plt.grid(True)
    plt.savefig('line_chart.png')
    plt.close()
    print("Line chart saved as line_chart.png")

def main():
    gera_grafico_tempo_pesoLimite(carrega_dados_csv("./Resultados/tempera.csv"))

if __name__ == "__main__":
    main()
    