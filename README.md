# 🔧 AI Code Refactoring & Vulnerability Detection Assistant

This project analyzes GitHub repositories to automatically **suggest code improvements** and detect **potential vulnerabilities** using Large Language Models (LLMs).

---

## 🚀 Features
- GitHub repo scraping
- Code parsing and analysis
- AI-powered refactoring suggestions
- Vulnerability detection
- Option to apply changes locally

---

## 📦 Installation

```bash
git clone https://github.com/priyanshugar-gg/ai-code-refactor.git
cd ai-code-refactor
pip install -r requirements.txt

🛠️ Usage
1. Create a .env file and add your OpenAI key:

OPENAI_API_KEY=your_api_key_here

2. Run the tool:

python main.py

3. Follow the CLI instructions to:

Enter a GitHub repo URL

See suggested improvements

Approve/refuse applying changes

🔒 Warning
Keep your .env file private and never push it to GitHub. We've added it to .gitignore for safety.

👨‍💻 Contributors
Priyanshu Garg (@priyanshugar-gg)

📄 License
This project is licensed under the MIT License.

---

### ✅ Finally, commit and push the README:

```bash
git add README.md
git commit -m "Added README with installation and usage instructions"
git push origin main

📸 **SAMPLE OUTPUT**: A screenshot of the program's output is available in the `assets` folder as `output.png`.