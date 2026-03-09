import requests
from config import API_KEY_REF, MODEL_NAME
from rich.console import Console
from rich.markdown import Markdown


def main(prompt):
    console = Console()

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY_REF}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": f"{MODEL_NAME}",
        "messages": [
            {
                "role": "user",
                "content": f"{prompt}"
            }
        ],
        "modalities": ["text"]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        result = response.json()

        for choice in result["choices"]:
            content = choice["message"]["content"]
            md = Markdown(content)
            print("---RESPONSE---")
            console.print(md)
            # print(content)
            print("---RESPONSE-END---")
            with open("response.md",'a') as response_file:
                response_file.write(content + "\n")

    except Exception as e:
        print(e)
