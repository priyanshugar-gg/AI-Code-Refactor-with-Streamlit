import os
import git
import subprocess

def clone_repo(repo_url, clone_dir="cloned_repo"):
    if os.path.exists(clone_dir):
        subprocess.run(["rm", "-rf", clone_dir])
    git.Repo.clone_from(repo_url, clone_dir)
    return clone_dir

def analyze_complexity(repo_path):
    result = subprocess.run(["radon", "cc", "-s", "-a", repo_path], capture_output=True, text=True)
    return result.stdout

def analyze_security(repo_path):
    result = subprocess.run(["bandit", "-r", repo_path], capture_output=True, text=True)
    return result.stdout
