import random

N_ITENS = 10
PESO_LIMIT = 25

TAM_POPULACAO = 30
N_GERACOES = 100
CHANCE_MUTACAO = 0.05

VALOR_MAX = 100
VALOR_MIN = 1
PESO_MAX = 10
PESO_MIN = 1

SEMENTE_ITEM = 399
SEMENTE_POPU = 400
SEMENTE_EXEC = 279

MOSTRA_POP = True
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

def valida_estado(e):
	if e is None:
		print("Estado parametro mal alocado")
		return None

	if e.peso_som > PESO_LIMIT:
		return 0

	return 1

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

def f_objetivo(e):
	if e is None:
		print("Estado parametro mal alocado")
		return None

	#return e.valor_som * (e.valor_som / e.peso_som)

	if e.valor_som == 0 or e.peso_som == PESO_LIMIT:
		return 0

	return e.valor_som * (e.valor_som / (PESO_LIMIT - e.peso_som))

def escolhe_prox(e):

	maior = Estado()
	define_Estado(maior, e.peso_som, e.valor_som, e.itens)
	atual = Estado()
	define_Estado(atual, e.peso_som, e.valor_som, e.itens)

	for i in range(N_ITENS):
		if (e.itens[i] == 0):
			add_Item(atual, i)
		else:
			ret_Item(atual, i)
		
		if (f_objetivo(atual) > f_objetivo(maior)):
			define_Estado(maior, atual.peso_som, atual.valor_som, atual.itens)

		if (e.itens[i] == 0):
			ret_Item(atual, i)
		else:
			add_Item(atual, i)
		
	return maior 


def main():
	inicializa_itens_ale()

	global lista_itens

	for item in lista_itens:
		print(item.valor, item.peso)
	
	random.seed(SEMENTE_EXEC)

	atual = Estado()
	prox = Estado()
	prox = escolhe_prox(atual)

	while (f_objetivo(prox) > f_objetivo(atual)):
		define_Estado(atual, prox.peso_som, prox.valor_som, prox.itens)
		prox = escolhe_prox(atual)
	define_Estado(atual, prox.peso_som, prox.valor_som, prox.itens)

	print(f"\nMelhor solução encontrada {atual.valor_som} / {atual.peso_som}, {f_objetivo(atual)} {atual.itens}")


if __name__ == "__main__":
	main()