import requests
from bs4 import BeautifulSoup
import sys


class Translator:

    def __init__(self):
        self.languages = {'1': 'Arabic',
                          '2': 'German',
                          '3': 'English',
                          '4': 'Spanish',
                          '5': 'French',
                          '6': 'Hebrew',
                          '7': 'Japanese',
                          '8': 'Dutch',
                          '9': 'Polish',
                          '10': 'Portuguese',
                          '11': 'Romanian',
                          '12': 'Russian',
                          '13': 'Turkish'}

        self.target_language = None
        self.source_language = None
        self.word_to_translate = None

    def hello(self):
        print("Hello, you're welcome to the translator. Translator supports: ")
        for k, v in self.languages.items():
            print(f'{k}. {v}')

    def set_source_language(self, lang=None):
        if lang is None:
            print('Type the number of your language:\n>')
            self.source_language = self.languages[input()]
        else:
            self.source_language = lang

        if self.source_language.capitalize() not in self.languages.values():
            print(f"Sorry, the program doesn't support {self.source_language.lower()}")
            exit()

    def set_target_language(self, lang=None):
        if lang is None:
            print('Type the number of language you want to translate to:\n>')
            language = input()
            if language != '0':
                self.target_language = self.languages[language]
            else:
                self.target_language = "0"
        else:
            self.target_language = lang

        if self.target_language.capitalize() not in self.languages.values() and \
                self.target_language != '0' and \
                self.target_language != 'all':
            print(f"Sorry, the program doesn't support {self.target_language.lower()}")
            exit()

    def simultaneous_translation(self):
        for v in self.languages.values():
            self.target_language = v
            if self.target_language.lower() != self.source_language.lower():
                words, examples = self.parse_data()

                with open(f"{self.word_to_translate}.txt", 'a') as output:
                    print(f'\n{self.target_language} Translations:')
                    output.write(f'\n{self.target_language} Translations:\n')

                    print(words[0])
                    output.write(words[0])

                    print(f'\n{self.target_language} Example:')
                    output.write(f'\n\n{self.target_language} Example:\n')

                    source_example, target_example = examples[0]
                    print(f'{source_example}:\n{target_example}')
                    output.write(f'{source_example}:\n{target_example}\n')

    def set_word_to_translate(self, word=None):
        if word is None:
            print('Type the word you want to translate:')
            self.word_to_translate = input()
        else:
            self.word_to_translate = word

    def get_data(self):
        headers = {'user-agent': 'Mozilla/5.0'}
        url = f"https://context.reverso.net/translation/{self.source_language.lower()}-{self.target_language.lower()}/{self.word_to_translate}"
        # print(url)
        response = requests.Session().get(url, headers=headers)

        # response = requests.get(url, headers=headers)
        # print(response.status_code, 'OK')
        if response.status_code == 404:
            print(f"Sorry, unable to find {self.word_to_translate}")
            exit()
        elif response.status_code != 200:
            print("Something wrong with your internet connection")
            exit()
        else:
            return response
        #     return response
        # else:
        #     print("Something wrong with your internet connection")

    def parse_data(self):
        data = self.get_data().content
        parser = 'html.parser'
        soup = BeautifulSoup(data, parser)
        words = soup.find(id='translations-content').text.split()
        # examples = [x.text.strip() for x in soup.find_all(class_=['src ltr', 'trg ltr'])]
        examples = [x.text.strip() for x in soup.find_all('div', class_=['src', 'trg'])]
        examples = list(zip(examples[::4], examples[1::4]))
        return words, examples

    def show_settings(self):
        print(f'You chose "{self.target_language}" as the language '
              f'to translate "{self.word_to_translate}" to.')

    def show_results(self, n=5):
        words, examples = self.parse_data()

        print(f'{self.target_language} Translations:')

        for word in words[:n]:
            print(word, end='\n')

        print(f'\n{self.target_language} Examples:')

        for i, j in examples[:n]:
            print(i, ":\n", j, sep="", end="\n\n")

    def main(self):

        if len(sys.argv) == 1:
            self.hello()
            self.set_source_language()
            self.set_target_language()
            self.set_word_to_translate()
            if self.target_language == '0':
                self.simultaneous_translation()
            else:
                # self.set_word_to_translate()
                self.show_settings()
                self.show_results()
        else:
            self.set_source_language(sys.argv[1])
            self.set_target_language(sys.argv[2])
            self.set_word_to_translate(sys.argv[3])
            if self.target_language == "all":
                self.simultaneous_translation()
            else:
                self.show_settings()
                self.show_results()


if __name__ == "__main__":
    translator = Translator()
    translator.main()
