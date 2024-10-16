from functools import total_ordering
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical 
from textual.reactive import reactive
from textual.widgets import Static
from textual import events
from time import monotonic
import words_handler


class Timer(Static):
    start_time = reactive(monotonic)
    time = reactive(0)

    def on_mount(self):
        self.update_timer = self.set_interval(1 / 60, self.update_time)
        
    def update_time(self):
        self.time = (monotonic() - self.start_time)
        self.update(f"{self.time: .0f}")


class PrideApp(App):
    CSS_PATH = "style.tcss"

    def __init__(self, driver_class = None, css_path = None, watch_css: bool = False, num_words = 20):
        super().__init__(driver_class, css_path, watch_css)

        self.handler = words_handler.word_handler(num_words)
        self.val = ""
        self.record = []
        self.done = False
        self.finish_time = 0
        
        for _ in range(num_words * 2 - 1):
            self.record.append([])


    def compose(self) -> ComposeResult:
        with Vertical(id = "content"):
            yield Static(self.richen(), id = "content-label")
            yield Timer(id = "timer")
            yield Static("0 / 26", id = "ratio")


    def on_mount(self):
       self.query_one(Vertical).border_title = "gruv-type"
       self.val = self.richen() 
        
    def on_key(self, event: events.Key):
        if self.done:
            return 
        if event.key == "backspace":
            self.backspace()

        elif event.key != self.handler.get_current_char():
            self.record[self.handler.current_word].append(self.handler.current_in_word)
            self.handler.increase_cur()
            self.query_one("#content-label").update(self.richen())

        else:
            self.handler.increase_cur()
            self.query_one("#content-label").update(self.richen())

        if self.handler.done:
            self.done = True 
            self.query_one("#ratio").update('')
            self.query_one("#timer").update('')
            self.query_one("#timer").update_timer.pause()
            self.finish_time = self.query_one("#timer").time

        if not self.done:
            self.query_one("#ratio").update(f"{(self.handler.current_word + 1) // 2}/{(self.handler.num_word + 1) // 2}")
        else:
            num_wrong_chars = sum([len(word_record) for word_record in self.record])
            total_chars = self.handler.num_char
            percent = (total_chars - (num_wrong_chars)) * 100 / total_chars
            self.query_one("#content-label").update(f"Correct chars percent: {percent:.2f} \n WPM: {(self.handler.num_word / self.finish_time) * 60 * percent / 100:.2f}")

    
    def backspace(self):
        self.handler.decrase_cur()
        for ind, contid in enumerate(self.record[self.handler.current_word]):
            if self.handler.current_in_word == contid:
                del self.record[self.handler.current_word][ind]
        self.query_one(Static).update(self.richen())

    def richen(self):
        words = self.handler.words
        output = ""
        
        if self.handler.current_word != 0 or self.handler.current_in_word != 0:
            output += "[bold]"

        for word_index, word in enumerate(words):
            for character_index, character in enumerate(word):
                if word_index == self.handler.current_word and character_index == self.handler.current_in_word:
                    if self.handler.current_word != 0 or self.handler.current_in_word != 0:
                        output += "[/bold]" 
                
                is_red = character_index in self.record[word_index]
                is_current = character_index == self.handler.current_in_word and word_index == self.handler.current_word
                if is_red:
                    output += f"[red]{str(character)}[/red]"
                elif is_current:
                    output += f"[reverse]{str(character)}[/reverse]"
                elif is_red and is_current:
                    output += f"[reverse][red]{str(character)}[/red][/reverse]"
                else:
                    output += str(character) 
                
        return output
                

if __name__ == "__main__":
    app = PrideApp()
    app.run()
    print(app.record)
