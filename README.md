Deployment Link: https://priyanshugar-gg-ai-code-refactor-with-streamlit-app-9dxurr.streamlit.app/
## 🎥 If by any chance Deployment link has any issue then please watch the Demo Video.
📽️ Demo Link: https://drive.google.com/file/d/16HIB6Ldeo4X5P7P9TOWBoAAFiukxghOx/view?usp=sharing

# 🧠 AI Code Refactor with Streamlit

This project is a **Streamlit-based web app** that allows users to upload Python files or enter a GitHub repository URL. It automatically analyzes the code and performs **code refactoring** using **Groq LLM (LLaMA-3 / GPT-4o)** behind the scenes.

---

## 🚀 Features

- 🔗 Accepts both GitHub repo URL and local `.py` / `.ipynb` file uploads
- 🧠 Uses Groq's high-speed LLMs to analyze and refactor code
- 📁 Converts `.ipynb` files to `.py` scripts
- 📊 Displays refactored output with download option
- 💻 Easy to use via interactive Streamlit frontend

---

## 📦 Technologies Used

- [Streamlit](https://streamlit.io/)
- [Python](https://www.python.org/)
- [Groq API](https://groq.com/)
- [LangChain](https://www.langchain.com/)
- [GitPython](https://gitpython.readthedocs.io/)
- `nbconvert` for converting notebooks to Python scripts

---

## ⚙️ How to Run Locally

1. **Clone the repo**

   git clone https://github.com/priyanshugar-gg/AI-Code-Refactor-with-Streamlit.git
   cd AI-Code-Refactor-with-Streamlit
   
2. **Create and activate a virtual environment (optional but recommended)**

   python -m venv venv
   source venv/bin/activate    # On Windows: venv\Scripts\activate
   
3. **Get your Groq API Key**
   
   Create a .env file in the root directory:
   GROQ_API_KEY=your_groq_api_key_here
   
   Or export it as an environment variable:
   export GROQ_API_KEY=your_groq_api_key_here

4. **Run the Streamlit app**
  
   streamlit run app.py

## 📌 Notes
This project uses the Groq Cloud API with models like LLaMA-3 and GPT-4o, which are very fast and cost-efficient.

Make sure you don’t upload .env or secrets to GitHub (GitHub will block it).

If you're facing any rate-limit issues, reduce token usage or add delay between multiple requests.

## 📄 License
MIT License © Priyanshu Garg
Feel free to fork, improve, and use this project in your own apps!

---

### 🔧 Next Step

1. Save this file as `README.md` in your project root.
2. If you want help embedding the screen recording as a **GIF** or **video** in GitHub, upload it and I’ll help you embed it properly.
3. Need a **requirements.txt** generator? Just ask!

Let me know once you upload the demo video — I’ll help format the link properly in the README.
