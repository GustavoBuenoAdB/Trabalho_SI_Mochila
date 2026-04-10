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

def qualidade_da_solucao():
    print('a')
    #semente mesma e o limite é o mesmo -> reultado tem que ser o memo
    #testar tam pop, tempo de execução

def temperatura_limite(df):
    plt.figure(figsize=(10,5))
    plt.plot(df['Temp inicial'], df['Melhor Escolha'], marker='o')
    plt.xlabel('Temperatura')
    plt.ylabel('Soluções')
    plt.title('Comparação: Tempo de Execução vs Peso Máximo')
    plt.grid(True)
    plt.savefig('line_chart2.png')
    plt.close()
    print("Line chart saved as line_chart.png")
    print('média da função de objetivo de uma população')

def media_funcao_objetivo(df):
    mean = df['F(x)'].mean()
    print(f"Média da função objetivo: {mean}")
    return mean

def grafico_duas_linhas(df1, df2, col_x1, col_y1, col_x2, col_y2):
    plt.figure(figsize=(10,5))
    plt.plot(df1[col_x1], df1[col_y1], color='blue', label=f'{col_y1} (linha azul)')
    plt.plot(df2[col_x2], df2[col_y2], color='red', label=f'{col_y2} (linha vermelha)')
    plt.xlabel('Eixo X')
    plt.ylabel('Eixo Y')
    plt.title('Gráfico com Duas Linhas')
    plt.legend()
    plt.grid(True)
    plt.savefig('duas_linhas.png')
    plt.close()
    print("Gráfico com duas linhas salvo como duas_linhas.png")
    plt.close()

def funcoes_prob_troca(df):
    plt.figure(figsize=(10,5))
    plt.plot(df['id'],df['g(x)'])
    plt.xlabel('Tempo')
    plt.ylabel('Probabilidade de Piora')
    plt.title('Valor da probabilidade de Piora ao longo da execução Antiga')
    plt.grid(True)
    plt.savefig('line_chart_nova.png')
    plt.close()
    print("Line chart saved as line_chart.png")
    print('média da função de objetivo de uma população')
    print('a')

def grafico_duas_linhas(df, x_col, y1_col, y2_col):
    df = df.sort_values(by=x_col)  # Ordenar pelo eixo X para conectar os pontos corretamente
    fig, ax1 = plt.subplots(figsize=(10, 5))

    # Eixo Y esquerdo para Solução (azul)
    ax1.plot(df[x_col], df[y1_col], color='blue', marker='o', label='Solução')
    ax1.set_xlabel(x_col)
    ax1.set_ylabel(y1_col, color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')

    # Eixo Y direito para Tempo de execução (vermelho)
    ax2 = ax1.twinx()
    ax2.plot(df[x_col], df[y2_col], color='red', marker='s', label='Tempo de execução')
    ax2.set_ylabel(y2_col, color='red')
    ax2.tick_params(axis='y', labelcolor='red')

    plt.title('Tamanho da População vs Solução e Tempo de Execução')
    fig.tight_layout()
    plt.savefig('grafico_populacao.png')
    plt.close()
    print("Gráfico salvo como grafico_populacao.png")

def main():
    #gera_grafico_tempo_pesoLimite(carrega_dados_csv("./Resultados/tempera.csv"))    df1 = carrega_dados_csv("./Resultados/temp_MelhorEscolha.csv")
    #df2 = carrega_dados_csv("tampop_tempo_qual.csv")
    #grafico_duas_linhas(df2, 'Tamanho População', 'Solução', 'Tempo de execução')    #media_funcao_objetivo(carrega_dados_csv("funcoes_objetivo.csv"))
    #funcoes_prob_troca(carrega_dados_csv("funcoes_prob_troca.csv"))
    #desenho_do_aumento_detemp(carrega_dados_csv("./Resultados/temp_MelhorEscolha.csv"))
    temperatura_limite(carrega_dados_csv('./Resultados/temp_MelhorEscolha.csv'))

if __name__ == "__main__":
    main()
    