import requests
import json

# relative
from config.config import API_KEY_REF, MODEL_NAME


def api_call(SockAdapterOBJ, prompt="say your greetings in two languages"):
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

    for line in response.iter_lines():
        if line:
            line_str = line.decode("utf-8")
            if line_str.startswith("data: "):
                data = line_str[6:]
                # with open("log.txt", 'a')as file:
                #     file.write(data+ '\n')
                if data == "[DONE]":
                    break
                try:
                    parsed = json.loads(data)
                    # console.log(parsed)

                    if parsed["choices"]:
                        # I dont actually know what delta is but it contains content, role.
                        # delta = { content,role,reasoning,reasoning_details }
                        delta = parsed["choices"][0]["delta"]
                        role = delta.get("role")
                        content = delta.get("content")
                        reasoning = delta.get("reasoning")
                        isReasoning = False
                        if content:
                            isReasoning = False
                            # HERE

                            prepared_data = (role, content, isReasoning)
                            SockAdapterOBJ.send(str(prepared_data))
                        elif reasoning:
                            isReasoning = True
                            # yield (role, reasoning, isReasoning)
                except json.JSONDecodeError:
                    continue
