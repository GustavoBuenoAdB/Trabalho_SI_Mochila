import random
import resultados
import time
import argparse


parser = argparse.ArgumentParser(description='Algoritmo Genético para Problema da Mochila')
parser.add_argument('-t', type=int, default=30, help='Tamanho da população')
parser.add_argument('-ng', type=int, default=10, help='Número de gerações')
parser.add_argument('-cm', type=float, default=0.1, help='Chance de mutação')
parser.add_argument('-si', type=int, default=399, help='Semente para itens')
parser.add_argument('-sp', type=int, default=420, help='Semente para população')
parser.add_argument('-sx', type=int, default=6975, help='Semente para execução')

args = parser.parse_args()

TAM_POPULACAO = args.t
N_GERACOES = args.ng
CHANCE_MUTACAO = args.cm
SEMENTE_ITEM = args.si
SEMENTE_POPU = args.sp
SEMENTE_EXEC = args.sx

N_ITENS = 10
PESO_LIMIT = 10

VALOR_MAX = 10
VALOR_MIN = 1
PESO_MAX = 10
PESO_MIN = 1

MOSTRA_POP = 1
MOSTRA_MEL_GER = True 
PROB_50_50 = True

class Item:
	def __init__(self):
		self.peso = 0
		self.valor = 0

class Estado:
	def __init__(self):
		self.peso_som = 0
		self.valor_som = 0
		self.itens = [0] * N_ITENS

# lista global de todos os itens
lista_itens = None
populacao = None

def inicializa_itens_ale():
	global lista_itens

	#valida a existencia da lista ou a inicializa
	if lista_itens is None or len(lista_itens) == 0:
		lista_itens = [Item() for _ in range(N_ITENS)]

	random.seed(SEMENTE_ITEM)

	for it in lista_itens:
		it.valor = random.randint(VALOR_MIN, VALOR_MAX - 1)
		it.peso = random.randint(PESO_MIN, PESO_MAX - 1)

	return lista_itens

def define_Estado(e, peso_som, valor_som, itens):
	if e is None:
		print("Estado parametro mal alocado")
		return

	e.itens = itens.copy()
	e.peso_som = peso_som
	e.valor_som = valor_som

def add_Item(e, id_item):
	global lista_itens

	if e is None:
		print("Estado parametro mal alocado")
		return

	if lista_itens is None:
		print("Lista de Itens mal alocada")
		return

	if e.itens[id_item] == 0:
		e.itens[id_item] = 1
		e.valor_som += lista_itens[id_item].valor
		e.peso_som += lista_itens[id_item].peso
	else:
		print("Tentou adicionar item ja adicionado")

def ret_Item(e, id_item):
	global lista_itens

	if e is None:
		print("Estado parametro mal alocado")
		return

	if lista_itens is None:
		print("Lista de Itens mal alocada")
		return

	if e.itens[id_item] == 1:
		e.itens[id_item] = 0
		e.valor_som -= lista_itens[id_item].valor
		e.peso_som -= lista_itens[id_item].peso
	else:
		print("Tentou retirar item não adicionado")

def mutacao(e):
	if e is None:
		print("Estado parametro mal alocado")
		return None

	if (random.random() < CHANCE_MUTACAO):
		item_ale = random.randint(0, N_ITENS - 1)

		if e.itens[item_ale] == 0:
			add_Item(e, item_ale)
		elif e.itens[item_ale] == 1:
			ret_Item(e, item_ale)
		else:
			print(f"Estado com item {item_ale} invalido")

def f_objetivo(e):
	if e is None:
		print("Estado parametro mal alocado")
		return None

	#if e.peso_som == 0:
		return 0

	#return e.valor_som * (e.valor_som / e.peso_som)

	if e.valor_som == 0:
		return 0
	resultados.salva_parametros_resultados([[e.valor_som * (e.valor_som / (PESO_LIMIT + 1 - e.peso_som))]], "funcoes_objetivo.csv", ["F(x)"])
	return e.valor_som * (e.valor_som / (PESO_LIMIT + 1 - e.peso_som))

def valida_estado(e):
	if e is None:
		print("Estado parametro mal alocado")
		return None

	if e.peso_som > PESO_LIMIT:
		return 0

	return 1

def f_fitness(e):

	if (valida_estado(e)):
		return f_objetivo(e) #tem que retornar entre 0 e 1?
	return  (PESO_LIMIT / e.peso_som) * (e.valor_som * (e.valor_som / (e.peso_som)))

def sortear_estado():
	global populacao

	som_chances = 0
	for e in populacao:
		som_chances += f_fitness(e)
	
	sorteado = (random.random() * som_chances)

	for e in populacao:
		sorteado -= f_fitness(e)
		if (sorteado <= 0):
			return e

def cruza_estados(e1, e2, ef):

	if (PROB_50_50):
		prob = 0.5
	elif ((f_fitness(e1) + f_fitness(e2)) == 0):
		prob = 0.5
	else:
		prob = f_fitness(e1) / (f_fitness(e1) + f_fitness(e2)) #entre 0 e 1

	for i in range(N_ITENS):
		if (e1.itens[i] != e2.itens[i]):
			if (random.random() < prob):
				ef.itens[i] = e1.itens[i]
			else:
				ef.itens[i] = e2.itens[i]
		else:
			if (random.random() < CHANCE_MUTACAO):
				ef.itens[i] = random.randint(0,1)
			else:
				ef.itens[i] = e1.itens[i]
	atualiza_soma_estado(ef)

def inicializa_populacao_ale():
	global populacao

	#valida a existencia da lista ou a inicializa
	if populacao is None or len(populacao) == 0:
		populacao = [Estado() for _ in range(TAM_POPULACAO)]

	random.seed(SEMENTE_POPU)

	e_vaz = Estado()
	e_che = Estado()
	for i in range(N_ITENS):
		e_che.itens[i] = 1
	atualiza_soma_estado(e_che)

	for e in populacao:
		
		cruza_estados(e_vaz, e_che, e)

		for i in range(N_ITENS):
			e.itens[i] = random.randint(0, 1)
		atualiza_soma_estado(e)

def atualiza_soma_estado(e):
	global lista_itens
	
	som_peso = 0
	som_valor =0
	for i in range(N_ITENS):
		if e.itens[i] == 1:
			som_peso += lista_itens[i].peso
			som_valor += lista_itens[i].valor
	e.valor_som = som_valor
	e.peso_som = som_peso

def main():
	inicializa_itens_ale()
	inicializa_populacao_ale()
	t_inicial = time.time()
	global lista_itens

	for item in lista_itens:
		print(item.valor, item.peso)
	
	global populacao
	nova_populacao = [Estado() for _ in range(TAM_POPULACAO)]
	melhor = Estado()

	if (MOSTRA_POP):
		for e in populacao:
			print(e.valor_som, e.peso_som, e.itens, f_fitness(e))
	
	random.seed(SEMENTE_EXEC)

	for i in range(N_GERACOES):
		for e in nova_populacao:
			e1 = sortear_estado()
			populacao.remove(e1)
			e2 = sortear_estado()
			populacao.append(e1)

			cruza_estados(e1,e2, e)
			mutacao(e)
			if (valida_estado(e)):
				if (f_fitness(e) > f_fitness(melhor)):
					melhor.itens = e.itens.copy()
					melhor.peso_som = e.peso_som
					melhor.valor_som = e.valor_som
		populacao = [e for e in nova_populacao]
		
		if (MOSTRA_POP):
			for e in populacao:
				print(e.valor_som, e.peso_som, e.itens, f_fitness(e))
		if (MOSTRA_MEL_GER):
			print(f"Melhor estado na geração {i}: {melhor.valor_som} / {melhor.peso_som}, {f_fitness(melhor)} {melhor.itens}")
	
	print(f"\nMelhor solução encontrada {melhor.valor_som} / {melhor.peso_som}, {f_fitness(melhor)} {melhor.itens}")
	t_final = time.time()
	tempo_execucao = t_final - t_inicial
	resultados.salva_parametros_resultados([[TAM_POPULACAO, melhor.valor_som, tempo_execucao]],"tampop_tempo_qual.csv",["Tamanho População", "Solução", "Tempo de execução"])

if __name__ == "__main__":
	main()