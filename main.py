import requests
from bs4 import BeautifulSoup


class LanguageNotFoundError(Exception):
    def __init__(self, language):
        self.language = language

    def __str__(self):
        return f"Sorry the program doesn't support {self.language}"


class InternetConnectionError(Exception):
    def __str__(self):
        return "Something wrong with your internet connection"


class WordNotFoundError(Exception):
    def __init__(self, word):
        self.word = word

    def __str__(self):
        return f"Sorry, unable to find {self.word}"


print('Hello, welcome to the translator. Translator supports:')
languages = ['Arabic', 'German', 'English', 'Spanish', 'French', 'Hebrew', 'Japanese', 'Dutch', 'Polish',
             'Portuguese', 'Romanian', 'Russian', 'Turkish']
for i, j in enumerate(languages):
    print(str(i + 1) + ". " + str(j))

your_language = input("Enter your language from the list above:\n").title()
target_language = input(
    "Enter the language you would like to translate to or type 'all' to get all translations:\n").title()
word_input = input("Type the word you want to translate:\n").lower()

translate_to = []
try:
    if your_language not in languages:
        raise LanguageNotFoundError(your_language)

    if target_language in languages:  # Checks for your language in the languages list
        translate_to.append(target_language)
    elif target_language == 'All':
        translate_to.extend([i for i in languages])
        translate_to.remove(your_language)
    else:
        raise LanguageNotFoundError(target_language)  # Raise error if language not found

    # create file and add translation
    with open(f"{word_input}.txt", mode='w', encoding='utf-8') as trans:
        # Translate all in the languages in translate_to list
        for i in translate_to:

            # Get the translation page
            headers = {'User-Agent': 'Mozilla/5.0'}
            s = requests.session()
            url = "https://context.reverso.net/translation/" + your_language.lower() + "-" + i.lower() + \
                  "/" + word_input
            page = s.get(url, headers=headers)

            if page.status_code == 404:  # Check word can be translated
                raise WordNotFoundError(word_input)
            elif page.status_code != 200:  # Check internet connection
                raise InternetConnectionError

            # Remove spaces from the beginning of the fle
            if i == translate_to[0]:
                trans.write(f"{i} Translations:\n")
            else:
                trans.write(f"\n\n\n{i} Translations:\n")

            # Beautifulsoup
            soup = BeautifulSoup(page.content, "html.parser")
            translate = soup.findAll('span', {'class': 'display-term'})
            translation = [x.text for x in translate]
            if translate_to == "All":
                for word in translation[:1]:
                    trans.write(word + "\n\n")
            else:
                for word in translation[:5]:
                    trans.write(word + "\n")
                trans.write("\n")

            # Examples
            use_case = soup.find('section', {'id': 'examples-content'}).findAll('span', {'class': 'text'})
            examples = [x.text.strip() for x in use_case]

            trans.write(f"{i} Examples:\n")
            for j in range(len(examples[:4])):
                if j % 2 == 0:
                    trans.write(examples[j] + ":" + "\n")
                else:
                    trans.write(examples[j] + "\n\n")

    with open(f"{word_input}.txt", mode='r', encoding='utf-8') as file:
        file_content = file.read()
        print(file_content)

except LanguageNotFoundError as err:
    print(err)

except InternetConnectionError as err:
    print(err)

except WordNotFoundError as err:
    print(err)
