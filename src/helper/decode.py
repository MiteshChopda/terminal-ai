import base64
import secrets


def generate_hex_string(length=6):
    return secrets.token_hex(length)


def decode(base64_string: str):
    decoded_bytes = base64.b64decode(base64_string)
    filename = generate_hex_string()
    with open(f"../images/{filename}.png", "wb") as file:
        file.write(decoded_bytes)
    return f"images/{filename}.png"
