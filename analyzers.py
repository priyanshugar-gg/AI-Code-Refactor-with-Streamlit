import os
import subprocess
from radon.complexity import cc_visit

def analyze_complexity(path):
    results = {}
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith(".py"):
                try:
                    full_path = os.path.join(root, file)
                    with open(full_path, "r", encoding="utf-8") as f:
                        code = f.read()
                        blocks = cc_visit(code)
                        complex_funcs = [b for b in blocks if b.complexity > 10]
                        if complex_funcs:
                            results[full_path] = complex_funcs
                except:
                    continue
    return results

def analyze_security(path):
    result = subprocess.run(["bandit", "-r", path, "-f", "json"], capture_output=True, text=True)
    return result.stdout
