import time

from textual import work
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical, Container
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
            yield Vertical(id="chat_container")

            with Horizontal(id="input_container"):
                yield Input(placeholder="Hey, what's on your mind?", name="input", id="input")
                yield Button("Send", id="btn_send")

    def on_input_submitted(self, event: Input.Submitted):
        if not event.value:
             return
        user_input = Static(f"{event.value}", classes="user_input")
        
        chat_container = self.query_one("#chat_container")
        chat_container.mount(user_input)
        chat_container.scroll_end(animate=True)
        
        self.sc.send(event.value)

    def stream_response(self, content, isReasoning=False):
        chat_container = self.query_one("#chat_container")

        last_child = None
        if chat_container.children:
             last_child = chat_container.children[-1]

        if isReasoning:
            if last_child.has_class("reasoning"):
                self.call_from_thread(last_child.append, content)   
            elif last_child.has_class("user_input"):
                reasoning = Markdown(f"{content}", classes="reasoning")
                self.call_from_thread(chat_container.mount, reasoning)        
            else:
                return  
        else:
            if last_child.has_class("reasoning"):
                response = Markdown(f"{content}", classes="response")
                self.call_from_thread(chat_container.mount, response)
            elif last_child.has_class("response"):
                self.call_from_thread(last_child.append, content)   
        
        chat_container.scroll_end(animate=True)


    def on_button_pressed(self, event: Button.Pressed):
        pass

    def on_mount(self):
        self.screen.styles.background = "#212121"

app = MyApp()
app.run()
