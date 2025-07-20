from github_utils import clone_repo
from analyzers import analyze_complexity, analyze_security
from llm_assistant import get_suggestions

if __name__ == "__main__":
    repo_url = input("Enter GitHub repo URL: ")
    local_path = clone_repo(repo_url)

    print("\n🔍 Analyzing code complexity...")
    complexity_issues = analyze_complexity(local_path)

    print("\n🔐 Analyzing security vulnerabilities...")
    security_issues = analyze_security(local_path)

    print("\n🤖 Getting suggestions from GPT-4o...")
    suggestions = get_suggestions(str(complexity_issues), security_issues)

    print("\n💡 AI Suggestions:\n")
    print(suggestions)
