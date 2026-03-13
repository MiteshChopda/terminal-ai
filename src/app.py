import time

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
                yield Markdown("", classes="reasoning_md")
                yield Markdown("", classes="response_md")
            with Horizontal(id="input_container"):
                yield Input(
                    placeholder="Hey, what's on your mind?", name="input", id="input"
                )
                yield Button("Send", id="btn_send")
    
    async def on_input_submitted(self, event: Input.Submitted):
        await self.stream_response(event.value)
    
    response_buffer = ""
    reasoning_md_buffer = ""
    async def stream_response(self, prompt):
        output_container = self.query_one("#output_container", Vertical)
        response_md = self.query_one(".response_md", Markdown)
        reasoning_md = self.query_one(".reasoning_md", Markdown)
        last_update_time = 0
        def update_periodically(
                func,
                arg,
                current_time,
                last_update_time=last_update_time,
                updation_delay=0.2, 
            ):
            if last_update_time - current_time > updation_delay:
                func(arg)
                last_update_time = current_time
            elif last_update_time==0:
                func(arg)
                last_update_time = current_time
        for role, content, isReasoning in api_call(prompt):
            if isReasoning:
                self.reasoning_md_buffer += content # pyright: ignore[reportPossiblyUnboundVariable]
                update_periodically(reasoning_md.update, self.reasoning_md_buffer, current_time=time.time(), last_update_time=last_update_time,updation_delay=0.05)
            else:
                self.response_buffer += content # pyright: ignore[reportPossiblyUnboundVariable]
                update_periodically(response_md.update, self.response_buffer, current_time=time.time(), last_update_time=last_update_time)
            output_container.scroll_end(animate=False)
            output_container.scroll_down(animate=False)
            output_container.scroll_page_down(animate=False)

    def on_button_pressed(self, event: Button.Pressed):
        pass

    def on_mount(self):
        self.screen.styles.background = "#212121"


app = MyApp()
app.run()
