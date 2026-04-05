import random

N_ITENS = 10
PESO_LIMIT = 10
TEMP_INI = 100
TEMP_DEC = 1

VALOR_MAX = 10
VALOR_MIN = 1
PESO_MAX = 10
PESO_MIN = 1

SEMENTE = 10

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

# inicializa os valores dos itens do problema em valores randomicos entre MIN e MAX definidos nas macros
def inicializa_itens_ale():
	global lista_itens

	#valida a existencia da lista ou a inicializa
	if lista_itens is None or len(lista_itens) == 0:
		lista_itens = [Item() for _ in range(N_ITENS)]

	random.seed(SEMENTE)

	for it in lista_itens:
		it.valor = random.randint(VALOR_MIN, VALOR_MAX - 1)
		it.peso = random.randint(PESO_MIN, PESO_MAX - 1)

	return lista_itens

def inicializa_estado_aleatorio(e):
	random.seed(SEMENTE)

	for i in range(N_ITENS):
		e.itens[i] = random.randint(0, 1)
	atualiza_soma_estado(e)

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

def vizinho(e):
	if e is None:
		print("Estado parametro mal alocado")
		return None

	viz = Estado()
	define_Estado(viz, e.peso_som, e.valor_som, e.itens)

	item_ale = random.randint(0, N_ITENS - 1)

	if e.itens[item_ale] == 0:
		add_Item(viz, item_ale)
	elif e.itens[item_ale] == 1:
		ret_Item(viz, item_ale)
	else:
		print(f"Estado com item {item_ale} invalido")
		return None

	return viz

def f_objetivo(e):
	if e is None:
		print("Estado parametro mal alocado")
		return None

	if e.peso_som == 0:
		return 0

	return e.valor_som * (e.valor_som / e.peso_som)

	#if e.valor_som == 0:
		#return 0

	#return e.peso_som * (e.peso_som // e.valor_som)

def valida_estado(e):
	if e is None:
		print("Estado parametro mal alocado")
		return None

	if e.peso_som >= PESO_LIMIT:
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

def prob_troca(e_at, viz, temp):
	if (f_objetivo(e_at) < f_objetivo(viz)):
		return 1.0
	return (temp /TEMP_INI )

def main():
	inicializa_itens_ale()
	e_atual = Estado()
	inicializa_estado_aleatorio(e_atual)

	global lista_itens

	for item in lista_itens:
		print(item.valor, item.peso)
	
	melhor = Estado()

	temperatura = TEMP_INI
	while (temperatura > 0):
		viz = vizinho(e_atual)
		if (random.random() <= prob_troca(e_atual, viz, temperatura)):
			e_atual.itens = viz.itens.copy()
			e_atual.peso_som = viz.peso_som
			e_atual.valor_som = viz.valor_som
		temperatura -= TEMP_DEC

		if (valida_estado(e_atual)):
			if (f_objetivo(e_atual) > f_objetivo(melhor)):
				melhor.itens = e_atual.itens.copy()
				melhor.peso_som = e_atual.peso_som
				melhor.valor_som = e_atual.valor_som
	
	print(f"Melhor solução encontrada {melhor.valor_som} / {melhor.peso_som} \n")
	print(f"obtida levando {melhor.itens}")

if __name__ == "__main__":
    main()