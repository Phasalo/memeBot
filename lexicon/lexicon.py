import json
import os

LEXICON_RU = {}
with open(f'{os.path.dirname(__file__)}/lexicon_ru.json', 'r', encoding='utf-8') as file:
    LEXICON_RU = json.load(file)
