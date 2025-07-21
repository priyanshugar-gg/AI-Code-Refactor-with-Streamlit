import os
import time
import nbconvert
import nbformat
import openai
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = "llama3-70b-8192"
REPO_DIR = "cloned_repo"
HEADERS = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

def convert_ipynb_to_py(ipynb_path):
    with open(ipynb_path, "r", encoding="utf-8") as f:
        nb = nbformat.read(f, as_version=4)
    exporter = nbconvert.PythonExporter()
    source, _ = exporter.from_notebook_node(nb)
    output_path = ipynb_path.with_suffix(".py")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(source)
    print(f"✅ Converted: {ipynb_path} → {output_path}")
    return output_path

def collect_python_files(directory):
    py_files = []
    for path in Path(directory).rglob("*.py"):
        if not path.name.endswith("_refactored.py"):
            py_files.append(path)
    return py_files

def call_groq_model(prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"
    data = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": "You are a code refactoring assistant. Clean, optimize, and document the code."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3
    }

    while True:
        response = requests.post(url, headers=HEADERS, json=data)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        elif response.status_code == 429:
            wait_time = response.json().get("error", {}).get("message", "")
            print(f"⚠️ Rate limit hit. Retrying: {wait_time}")
            time.sleep(20)
        else:
            print(f"❌ API Error: {response.status_code} → {response.text}")
            return None

def refactor_code(code):
    prompt = f"""Refactor the following Python code to improve readability, performance, and add comments where necessary:\n\n```python\n{code}\n```"""
    return call_groq_model(prompt)

def main():
    print("🚀 Script started!")

    # Step 1: Convert all notebooks to Python scripts
    for ipynb_file in Path(REPO_DIR).rglob("*.ipynb"):
        convert_ipynb_to_py(ipynb_file)

    # Step 2: Collect all .py files
    py_files = collect_python_files(REPO_DIR)
    print("\n✅ Files collected for analysis:")
    for file in py_files:
        print(f" - {file}")

    # Step 3: Analyze and refactor
    for file in py_files:
        print(f"\n🔍 Analyzing and refactoring: {file}")
        try:
            with open(file, "r", encoding="utf-8") as f:
                original_code = f.read()

            refactored_code = refactor_code(original_code)
            if refactored_code:
                output_path = file.with_name(file.stem + "_refactored.py")
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(refactored_code)
                print(f"💾 Refactored code saved to: {output_path}")
        except Exception as e:
            print(f"❌ Error processing {file}: {e}")

if __name__ == "__main__":
    main()
