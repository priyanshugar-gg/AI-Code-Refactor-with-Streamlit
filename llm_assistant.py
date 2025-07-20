import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_suggestions(complexity_issues, security_issues):
    prompt = f"""
You are a code analysis assistant. Based on the following issues, suggest improvements:

🔧 Code Complexity Issues:
{complexity_issues}

🛡️ Security Vulnerabilities:
{security_issues}

Be detailed but concise. Give specific code-level suggestions.
"""
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful coding assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
    )
    return response.choices[0].message.content.strip()
