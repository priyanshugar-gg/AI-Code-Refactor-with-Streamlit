import streamlit as st
from utils import clone_repo, analyze_complexity, analyze_security
from llm_assistant import get_suggestions

st.set_page_config(page_title="AI Code Refactor", layout="wide")

st.title("🧠 AI Code Refactoring & Vulnerability Detector")

repo_url = st.text_input("🔗 Enter GitHub Repo URL")

if st.button("Analyze"):
    with st.spinner("Cloning and analyzing..."):
        repo_path = clone_repo(repo_url)

        complexity_report = analyze_complexity(repo_path)
        security_report = analyze_security(repo_path)
        
        st.subheader("📊 Code Complexity Report")
        st.code(complexity_report, language="text")
        
        st.subheader("🔐 Security Vulnerability Report")
        st.code(security_report, language="text")

        with st.spinner("💡 Getting GPT-4o Suggestions..."):
            suggestions = get_suggestions(complexity_report, security_report)
            st.subheader("🤖 AI Suggestions")
            st.markdown(suggestions)
