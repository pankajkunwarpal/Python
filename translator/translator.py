import sys
import requests
from bs4 import BeautifulSoup as b

types = ['', 'Arabic', 'German', 'English', 'Spanish', 'French',
         'Hebrew', 'Japanese', 'Dutch', 'Polish', 'Portuguese',
         'Romanian', 'Russian', 'Turkish']

if len(sys.argv) == 0:
    print('Hello, you\'re welcome to the translator. Translator supports:')
    for i in range(1, 14):
        print(str(i)+'. '+types[i])

    print('Type the number of your language:')
    from_lang = int(input())

    print('Type the number of language you want to translate to or \'0\' to translate to all languages:')
    to_lang = int(input())

    print('Type the word you want to translate:')
    word = input()

else:
    from_lang, to_lang= None, None
    try:
        from_lang, to_lang = types.index(sys.argv[1].capitalize()), 0 if sys.argv[2] == 'all' else types.index(sys.argv[2].capitalize())
    except ValueError:
        print('Sorry, the program doesn\'t support {}'.format(sys.argv[1] if sys.argv[1].capitalize() not in types else sys.argv[2]))
        sys.exit()
    word = sys.argv[3]

lang = (types[1:from_lang] + types[from_lang+1:]) if to_lang == 0 else [types[to_lang]]

with open(f'{word}.txt', 'w+', encoding='utf-8') as f:

    num = 1 if sys.argv[2] == 'all' else 5

    s = requests.Session()
    s.headers.update({"User-Agent": 'Chrome/87.0.4280.88'})

    try:
        for t in lang:

            html = s.get(f"https://context.reverso.net/translation/{types[from_lang].lower()}-{t.lower()}/{word}")

            soup = b(html.content, 'lxml')
            if html.status_code == 404:
                raise Exception

            words = [_.text.strip() for _ in soup.find_all('a', {'class': 'dict'})[:num]]
            examples = [":\n".join([s.text.strip(), t.text.strip()]) for s, t in zip(
                        soup.find_all('div', {'class': 'src ltr'})[:num],
                            soup.select('.example > .trg')[:num])]

            # print(t_word, src_exmp, trg_exmp, sep='\n')

            print("{} Translations:".format(t), *words, sep='\n', file=f)
            print("{} Translations:".format(t), *words, sep='\n')

            print("{} Examples:".format(t), *examples, sep='\n', file=f)
            print("{} Examples:".format(t), *examples, sep='\n')

    except ConnectionError :
        print('Something wrong with your internet connection')
    except Exception:
        print('Sorry, unable to find {}'.format(word))

