import spacy
import os
from langdetect import detect
import re


# Загрузка модели английского языка
try:
    nlp_en = spacy.load("en_core_web_sm")
except OSError:
    os.system("python -m spacy download en_core_web_sm")


# Загрузка модели для русского языка
try:
    nlp_ru = spacy.load("ru_core_news_sm")
except OSError:
    os.system("python -m spacy download ru_core_news_sm")



# Считываем стоп-слова - я буду работать со скачанными с сайтов списками, потому что у spacy, по моему мнению, недостаточно
# большие и полные списки стоп-слов
    
# английский
with open('project_bot/stopwords.txt', 'r') as file:
    # файл взят отсюда: https://www.kaggle.com/datasets/rowhitswami/stopwords?resource=download
    words = file.readlines()

# русский
with open('project_bot/stopwords-ru.txt', 'r') as file:
    # файл взят отсюда: https://github.com/stopwords-iso/stopwords-ru/blob/master/stopwords-ru.txt
    words1 = file.readlines()

english_stopwords = [word.strip() for word in words]
russian_stopwords = [word.strip() for word in words1]


# Делаем функцию, которая будет обрабатывать каждое слово и возвращать список
# токенизированных и лемматизированных слов
def process(text):
    text = re.sub(r'[^\w\s]', ' ', text)  # удаляем знаки препинания, заменяя их пробелами (которые мы потом тоже удалим)

    # удаляем смайлики
    emoji_pattern = re.compile("["
                            u"\U0001F600-\U0001F64F"
                            u"\U0001F300-\U0001F5FF"
                            u"\U0001F680-\U0001F6FF"
                            u"\U0001F1E0-\U0001F1FF"
                            "❤️"
                            "]+", flags=re.UNICODE)

    text = emoji_pattern.sub(r'', text)
    text = text.lower()
    # приступаем к работе с самими словами
    language = detect(text)
    if language == "ru":
        doc = nlp_ru(text)
        result = [i.lemma_ for i in doc if i.lemma_ not in russian_stopwords]
    else:
        doc = nlp_en(text)
        result = [i.lemma_ for i in doc if i.lemma_ not in english_stopwords]
    
    result = [item for item in result if item.strip() != '']  # удаляем все элементы-пробелы в списке

    return result


# проверка на то, состоит ли сообщение только из смайликов - если состоит, мы не должны заносить его в базу данных
def only_emojis(text):
    emoji_pattern = re.compile("["
                            u"\U0001F600-\U0001F64F"
                            u"\U0001F300-\U0001F5FF"
                            u"\U0001F680-\U0001F6FF"
                            u"\U0001F1E0-\U0001F1FF"
                            "❤️"
                            "]+", flags=re.UNICODE)
    if emoji_pattern.match(text):
        return True
    else:
        return False