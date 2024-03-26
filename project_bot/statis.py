import sqlite3
import io
from collections import defaultdict
import os
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import warnings

# Отключеним все предупреждения (предварительно их прочитав)
warnings.filterwarnings("ignore")


def statistics_all_bot():

    # Работаем с сообщениями для бота

    # Сначала работаем с базой данных

    basedir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(basedir, 'chat_data.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Берём то, что писал бот, группируем всё по леммам и складываем числа, у которых леммы одинаковые.
    # Это нужно, чтобы количество одних и тех же слов, употребленных в разных чатах, сложилось
    # Т.е. если у нас есть "cry", употребленное 5 раз в одном чате, и "cry", употребленное 2 раза в другом чате
    # на выходе получится "cry" со значением 7, потому что мы сгруппировали всё по леммам и сложили
    c.execute('''SELECT lemma, SUM(count) FROM message_counts WHERE sender = 'bot' GROUP BY lemma''')
    data = defaultdict(int)  # Создаем словарь

    # Добавляем в него данные
    for row in c.fetchall():
        # c.fetchall() возвращает список всех строк нашей новой таблицы. Каждая строка представляется в виде кортежа
        word, count = row
        data[word] += count

    conn.close()
    d = dict(data)  # Превращаем defaultdict в обычный словарь


    # Теперь работаем с визуализацией
    wordcloud_bot = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(d)

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud_bot, interpolation='bilinear')
    plt.axis('off')
    plt.title("Wordcloud for the most frequent words in the bot's messages")
    plt.tight_layout()

    # Сохраняем изображение в переменную
    image_bot = io.BytesIO()
    plt.savefig(image_bot, format='png')
    image_bot.seek(0)

    return image_bot



def statistics_all_user():
    # Теперь делаем всё то же самое, но с сообщениями пользователя
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(basedir, 'chat_data.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute('''SELECT lemma, SUM(count) FROM message_counts WHERE sender = 'user' GROUP BY lemma''')
    data = defaultdict(int)  # Создаем словарь

    # Добавляем в него данные
    for row in c.fetchall():
        # c.fetchall() возвращает список всех строк нашей новой таблицы. Каждая строка представляется в виде кортежа
        word, count = row
        data[word] += count

    conn.close()
    da = dict(data)  # Превращаем defaultdict в обычный словарь


    # Теперь работаем с визуализацией
    wordcloud_user = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(da)

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud_user, interpolation='bilinear')
    plt.axis('off')
    plt.title("Wordcloud for the most frequent words in the users' messages")
    plt.tight_layout()

    # Сохраняем изображение в переменную
    image_user = io.BytesIO()
    plt.savefig(image_user, format='png')
    image_user.seek(0)

    return image_user



def statistics_personal_bot(chat_id):

    # Работаем с сообщениями для бота

    # Сначала работаем с базой данных

    basedir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(basedir, 'chat_data.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute('''SELECT lemma, SUM(count) FROM message_counts WHERE sender = 'bot' AND chat_id = ? GROUP BY lemma''', (chat_id,))
    data = defaultdict(int)  # Создаем словарь

    # Добавляем в него данные
    for row in c.fetchall():
        # c.fetchall() возвращает список всех строк нашей новой таблицы. Каждая строка представляется в виде кортежа
        word, count = row
        data[word] += count

    conn.close()
    d = dict(data)  # Превращаем defaultdict в обычный словарь


    # Теперь работаем с визуализацией
    wordcloud_bot = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(d)

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud_bot, interpolation='bilinear')
    plt.axis('off')
    plt.title("Wordcloud for the most frequent words in the bot's messages that were sent to you")
    plt.tight_layout()

    # Сохраняем изображение в переменную
    image_bot = io.BytesIO()
    plt.savefig(image_bot, format='png')
    image_bot.seek(0)

    return image_bot



def statistics_personal_user(chat_id):
    # Теперь делаем всё то же самое, но с сообщениями пользователя
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(basedir, 'chat_data.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute('''SELECT lemma, SUM(count) FROM message_counts WHERE sender = 'user' AND chat_id = ? GROUP BY lemma''', (chat_id,))
    data = defaultdict(int)  # Создаем словарь

    # Добавляем в него данные
    for row in c.fetchall():
        # c.fetchall() возвращает список всех строк нашей новой таблицы. Каждая строка представляется в виде кортежа
        word, count = row
        data[word] += count

    conn.close()
    da = dict(data)  # Превращаем defaultdict в обычный словарь


    # Теперь работаем с визуализацией
    wordcloud_user = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(da)

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud_user, interpolation='bilinear')
    plt.axis('off')
    plt.title("Wordcloud for the most frequent words in your messages")
    plt.tight_layout()

    # Сохраняем изображение в переменную
    image_user = io.BytesIO()
    plt.savefig(image_user, format='png')
    image_user.seek(0)

    return image_user


def user_number():
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(basedir, 'chat_data.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''SELECT COUNT(DISTINCT chat_id) FROM message_counts''')

    result = c.fetchone()[0]
    return result

