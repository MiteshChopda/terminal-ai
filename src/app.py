from textual import work
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Button, Markdown
from textual.widgets import Input, Static, Label
from api_call import api_call


class MyApp(App):
    CSS_PATH = "styles.tcss"

    def compose(self) -> ComposeResult:
        with Vertical(id="root"):
            with Vertical(id="output_container"):
                yield Markdown("Hey I am the response from AI", id="output_md")
            with Horizontal(id="input_container"):
                yield Input(
                    placeholder="Hey, what's on your mind?", name="input", id="input"
                )
                yield Button("Send", id="btn_send")
    
    def on_input_submitted(self, event: Input.Submitted):
        self.stream_response(event.value)
        
    def stream_response(self, prompt):
        output_md = self.query_one("#output_md", Markdown)
        buffer = ""
        for role, content in api_call(prompt):
            buffer += content
            output_md.update(buffer)

    def on_button_pressed(self, event: Button.Pressed):
        pass

    def on_mount(self):
        self.screen.styles.background = "#212121"


app = MyApp()
app.run()
