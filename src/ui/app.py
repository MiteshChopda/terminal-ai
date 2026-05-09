import time

from textual import work
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Button, Markdown
from textual.widgets import Input, Static, Label
from ui.sock_client import SockAdapterClient


class MyApp(App):
    CSS_PATH = "styles.tcss"

    def __init__(self):
        super().__init__()
        self.sc = SockAdapterClient(textual_obj=self)

    def compose(self) -> ComposeResult:
        with Vertical(id="root"):
            with Vertical(id="output_container"):
                yield Markdown("", classes="reasoning_md")
                yield Markdown("", classes="response_md", id="test")
            with Horizontal(id="input_container"):
                yield Input(placeholder="Hey, what's on your mind?", name="input", id="input")
                yield Button("Send", id="btn_send")

    def on_input_submitted(self, event: Input.Submitted):
        self.sc.send(event.value)

    def stream_response(self, md_content):
        response_md = self.query_one("#test", Markdown)
        self.call_from_thread(response_md.append, md_content)

        output_container = self.query_one("#output_container", Vertical)
        output_container.scroll_end(animate=True)


    def on_button_pressed(self, event: Button.Pressed):
        pass

    def on_mount(self):
        self.screen.styles.background = "#212121"

app = MyApp()
app.run()
