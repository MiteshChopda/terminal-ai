import requests
import json
from config import API_KEY_REF, MODEL_NAME
from rich.console import Console
from rich.markdown import Markdown


def main(prompt):
    console = Console()

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY_REF}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": f"{MODEL_NAME}",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant. Keep it short if possible.",
            },
            {"role": "user", "content": f"{prompt}"},
        ],
        "modalities": ["text"],
        "stream": True,
    }

    response = requests.post(url=url, headers=headers, json=payload, stream=True)

    last_response_by = ""
    for line in response.iter_lines():
        if line:
            line_str = line.decode("utf-8")
            if line_str.startswith("data: "):
                data = line_str[6:]
                if data == "[DONE]":
                    break
                try:
                    parsed = json.loads(data)
                    # console.log(parsed)
                    with open("logs.py", "a") as logs:
                        logs.write(json.dumps(parsed) + "\n")

                    if parsed["choices"]:
                        # I dont actually know what delta is but it contains content, role.
                        delta = parsed["choices"][0]["delta"]

                        content = delta["content"]
                        role = delta["role"]
                        last_response_by = role
                        if content:
                            if last_response_by == role:
                                console.print(content, end="")
                            else:
                                console.print(f"[bold]{role}:[/bold] {content}")
                except json.JSONDecodeError:
                    continue
