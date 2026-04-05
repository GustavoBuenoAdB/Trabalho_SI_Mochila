import random

N_ITENS = 5
PESO_LIMIT = 10

TAM_POPULACAO = 4
N_GERACOES = 10
CHANCE_MUTACAO = 0.05

VALOR_MAX = 10
VALOR_MIN = 1
PESO_MAX = 10
PESO_MIN = 1

SEMENTE = 100

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

	if e.peso_som > PESO_LIMIT:
		return 0

	return 1

def f_fitness(e):

	if (valida_estado(e)):
		return f_objetivo(e) #tem que retornar entre 0 e 1?
	return 0

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

	if ((f_fitness(e1) + f_fitness(e2)) == 0):
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
			ef.itens[i] = e1.itens[i]
	atualiza_soma_estado(ef)

def inicializa_populacao_ale():
	global populacao

	#valida a existencia da lista ou a inicializa
	if populacao is None or len(populacao) == 0:
		populacao = [Estado() for _ in range(TAM_POPULACAO)]

	random.seed(SEMENTE)

	for e in populacao:
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

	global lista_itens

	for item in lista_itens:
		print(item.valor, item.peso)
	
	global populacao
	nova_populacao = [Estado() for _ in range(TAM_POPULACAO)]
	melhor = Estado()

	for i in range(N_GERACOES):
		for e in nova_populacao:
			cruza_estados(sortear_estado(), sortear_estado(), e)
			mutacao(e)
			if (valida_estado(e)):
				if (f_fitness(e) > f_fitness(melhor)):
					melhor.itens = e.itens.copy()
					melhor.peso_som = e.peso_som
					melhor.valor_som = e.valor_som
		populacao = [e for e in nova_populacao]
		
		for e in populacao:
			print(e.valor_som, e.peso_som, e.itens)
		print(f"Melhor solução encontrada {melhor.valor_som} / {melhor.peso_som} \n")
		print(f"obtida levando {melhor.itens}")

if __name__ == "__main__":
    main()