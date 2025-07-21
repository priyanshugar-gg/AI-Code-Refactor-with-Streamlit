import os
from groq import Groq

# Initialize Groq client
client = Groq(api_key=os.getenv("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"))  # Make sure to set this in your terminal

def get_suggestions(complexity_issues, security_issues):
    messages = [
        {
            "role": "system",
            "content": "You are a senior AI assistant helping developers refactor code and improve security."
        },
        {
            "role": "user",
            "content": f"""I have the following complexity issues in the code: {complexity_issues}.

And these are the security issues: {security_issues}.

Suggest detailed improvements for both and provide specific changes in code where possible.
"""
        }
    ]

    # Send request to Groq with LLaMA 3 model
    response = client.chat.completions.create(
        model="llama3-70b-8192",  # You can change this to another supported model
        messages=messages,
        temperature=0.7
    )

    return response.choices[0].message.content
