# Terminal AI

Talk to LLMs via openrouter api key in command line interface

### prerequisites:
* uv (0.9.26 or up)
* python (3.12 or up)

to run:
```bash
git clone https://github.com/MiteshChopda/terminal-ai.git
cd terminal-ai
uv sync
cd src
```
run socket server and app:
```bash
uv run -m api.sock_server && uv run -m ui.app
```
