import time

from textual import work
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Button, Markdown
from textual.widgets import Input, Static, Label
from api.api_call import api_call


class MyApp(App):
    CSS_PATH = "styles.tcss"

    def compose(self) -> ComposeResult:
        with Vertical(id="root"):
            with Vertical(id="output_container"):
                yield Markdown("", classes="reasoning_md")
                yield Markdown("", classes="response_md")
            with Horizontal(id="input_container"):
                yield Input(
                    placeholder="Hey, what's on your mind?", name="input", id="input"
                )
                yield Button("Send", id="btn_send")

    def on_input_submitted(self, event: Input.Submitted):
        await self.stream_response(event.value)

    def stream_response(self, prompt):
        output_container = self.query_one("#output_container", Vertical)
        response_md = self.query_one(".response_md", Markdown)
        reasoning_md = self.query_one(".reasoning_md", Markdown)

    def on_button_pressed(self, event: Button.Pressed):
        pass

    def on_mount(self):
        self.screen.styles.background = "#212121"


app = MyApp()
app.run()
