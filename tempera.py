import random

N_ITENS = 10
PESO_LIMIT = 10
TEMP_INI = 1000
TEMP_DEC = 1

VALOR_MAX = 30
VALOR_MIN = 1
PESO_MAX = 30
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

def temp_decai(temperatura):
	temperatura[0] -= TEMP_DEC

def valida_estado(e):
	if e is None:
		print("Estado parametro mal alocado")
		return None

	if e.peso_som > PESO_LIMIT:
		return 0

	return 1