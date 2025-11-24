import requests
import os
from dotenv import load_dotenv

api_url = "https://api.groq.com/openai/v1/chat/completions"


load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
model = "meta-llama/llama-4-scout-17b-16e-instruct"
file_path = "E:/Shashank Singh/Nyaya/logs/out_text.txt"

def call_groq_summary(prompt):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": f"Read the following legal case document and summarize it in clear, factual bullet points. Use plain language that can be understood by a common person. Do not include legal jargon, interpretations, or formatting like asterisks or emojis. Give final output no prompt from your side. Just provide the facts clearly, section by section:\n\n{prompt}"}
        ]
    }
    response = requests.post(API_URL, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"].strip()
    else:
        print("Error:", response.status_code, response.text)
        return "[ERROR]"

with open(FILE_PATH, "r", encoding="utf-8") as f:
    text = f.read()

summary = call_groq_summary(text)
summaryFinal = summary.replace("*", "")
print(summaryFinal)
