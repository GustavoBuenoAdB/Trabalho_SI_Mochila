import subprocess

for i in range(1,1000):
    result = subprocess.run(["python3", "tempera.py", "--peso_limit", f"{i}"], capture_output=True, text=True)
