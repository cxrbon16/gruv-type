from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.widgets import Static, RichLog
from textual import events
import words_handler



class KeyLogger(RichLog):
    def on_key(self, event: events.Key) -> None:
        self.write(event)


class PrideApp(App):
    CSS_PATH = "style.tcss"

    def __init__(self, driver_class = None, css_path = None, watch_css: bool = False, num_words = 5):
        super().__init__(driver_class, css_path, watch_css)

        self.handler = words_handler.word_handler(num_words)
        self.val = self.handler.get_current_word()
        self.record = []
        self.done = False
        
        for w_ind in range(num_words):
            self.record.append([])
    


    def compose(self) -> ComposeResult:
        with Vertical(id = "content"):
            yield Static(self.val)

    def on_mount(self):
       self.query_one(Vertical).border_title = "gruv-type"
        
    def on_key(self, event: events.Key):
        if event.key == "backspace":
            self.backspace()

        elif event.key != self.handler.get_current_char():
            self.record[self.handler.current_word].append(self.handler.current_in_word)
            self.handler.increase_cur()
            self.query_one(Static).update(self.richen())

        else:
            self.handler.increase_cur()
            self.query_one(Static).update(self.richen())

        if self.handler.done:
            self.done = True 
            print('ist done')
            exit()               
    
    def backspace(self):
        self.handler.decrase_cur()
        for ind, contid in enumerate(self.record[self.handler.current_word]):
            if self.handler.current_in_word == contid:
                del self.record[self.handler.current_word][ind]
        self.query_one(Static).update(self.richen())

    def richen(self) -> str:
        word = self.handler.get_current_word()
        curr_ind = self.handler.current_in_word
        curr_word_ind = self.handler.current_word
        richen_text = ""
        
        if curr_ind != 0:
            richen_text += "[bold]"

        for ind, chr in enumerate(word):
            if ind in self.record[curr_word_ind]:
                richen_text += f"[red]{str(chr)}[/red]"

            else:
                richen_text += str(chr)
            
            if ind == curr_ind-1 and curr_ind != 0:
                richen_text += "[/bold]"
            
            richen_text += "[sub]"

        richen_text += "[/sub]"
        return richen_text 



if __name__ == "__main__":
    app = PrideApp()
    app.run()
    print(app.record)
