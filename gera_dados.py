import subprocess
import argparse

parser = argparse.ArgumentParser(description='Gerador de testes para Problema da Mochila')
parser.add_argument('--tempera', type=int, default=1, help='Escolhe se é tempera (1) ou genético (0)')
parser.add_argument('--inicio', type=int, default=1, help='Inicio do range de iterações')
parser.add_argument('--fim', type=int, default=1000, help='Final do range de iterações')

args = parser.parse_args()

if(args.tempera):
    for i in range(args.inicio,args.fim):
        result = subprocess.run(["python3", "tempera.py", "--temp_ini", f"{i}"], capture_output=True, text=True)

for i in range(args.inicio,args.fim):
    result = subprocess.run(["python3", "genetico.py", "-t", f"{i}"], capture_output=True, text=True)
