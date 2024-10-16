from typing import List
import random


class word_handler():
    def __init__(self, num_word) -> None:
       self.num_word = num_word
       self.num_char = 0
       self.words = self.fetch_words()
       self.current_word = 0
       self.current_in_word = 0
       self.done = False
       self.lens_words = []
       self.in_space = False

       for word in self.words:
            self.lens_words.append(len(word))
    
    def pick_word(self, lemmas: List[str]):
        return lemmas[random.randint(0, len(lemmas) - 1)].strip()

    def fetch_words(self) -> List[str]:
        file_path = "data/lemmas.txt"
        words = []

        with open(file_path, 'r', encoding="UTF-8") as f:
            lemmas = f.readlines()

        for _ in range(self.num_word):
            picked_word = self.pick_word(lemmas).lower()
            self.num_char += len(picked_word) + 1
            words.append(self.pick_word(lemmas).lower())
            words.append(" ")
        self.num_char -= 1
        words.pop()
        self.num_word = self.num_word * 2 - 1
        return words 

    def get_current_word(self) -> str:
        return self.words[self.current_word]

    def get_current_char(self) -> str:
        return self.words[self.current_word][self.current_in_word]
    
    def increase_cur(self):
        # step forward the cursor.
        if self.lens_words[self.current_word] == self.current_in_word + 1:
            if self.num_word != self.current_word + 1:
                self.current_word += 1
                self.current_in_word = 0
            else:
                self.done = True

        else:
            self.current_in_word += 1
        

    def decrase_cur(self):
        # step back the cursor.
        if self.current_in_word == 0:
            if self.current_word != 0:
                self.current_word -= 1
                self.current_in_word = self.lens_words[self.current_word] - 1
        else:
            self.current_in_word -= 1

