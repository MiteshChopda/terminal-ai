from api_call import main
from rich.console import Console

console = Console()
console.rule("Welcome!")
prompt = console.input("[bold blue]Enter the prompt:\n---> ")
main(prompt)


