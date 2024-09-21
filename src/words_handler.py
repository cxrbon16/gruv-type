from typing import List


class word_handler():
    def __init__(self, num_word) -> None:
       self.num_word = num_word
       self.words = self.fetch_words()
       self.current_word = 0
       self.current_in_word = 0
       self.done = False

    def fetch_words(self) -> List[str]:
        pseudo_db = [
        "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s",
        "Bonjour",
        "Guten tag",
        "Salve",
        "Nǐn hǎo",
        "Olá",
        "Asalaam alaikum",
        "Konnichiwa",
        "Anyoung haseyo",
        "Zdravstvuyte",
        "Hello",
        ]

        if self.num_word < len(pseudo_db):
            return pseudo_db[0:self.num_word]

        return []

    def get_current_word(self) -> str:
        return self.words[self.current_word]

    def get_current_char(self) -> str:
        return self.words[self.current_word][self.current_in_word]
    
    def increase_cur(self):
        self.current_in_word = (self.current_in_word + 1) % (len(self.words[self.current_word]))
        if self.current_in_word == 0:
            self.current_word += 1
        if self.current_word == self.num_word:
            self.done = True 


    def decrase_cur(self):
        self.current_in_word = (self.current_in_word - 1)

        if self.current_in_word == -1:
            self.current_word -= 1
            self.current_in_word = len(self.words[self.current_word]) - 1 


    def __str__(self) -> str:
        return ' '.join(self.words)

    
