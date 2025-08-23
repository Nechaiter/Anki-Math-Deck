import subprocess

for opt in range(1, 5):
    print(f"Running CreateDeck.py with option {opt}...")
    process = subprocess.Popen(
        ["python", "CreateDeck.py"],
        stdin=subprocess.PIPE,
        text=True
    )
    process.communicate(input=str(opt) + "\n")