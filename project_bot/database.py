import sqlite3
import os


# функция для создания базы данных
def create():
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(basedir, 'chat_data.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Создаем таблицу, если она еще не существует
    c.execute('''CREATE TABLE IF NOT EXISTS message_counts
                (chat_id INTEGER, sender TEXT, lemma TEXT, count INTEGER DEFAULT 0)''')
    

# функция для записи и учета новых слов в базе данных
def word_count(chat_id, sender, lemma):
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(basedir, 'chat_data.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''UPDATE message_counts 
                 SET count = count + 1 
                 WHERE chat_id = ? AND sender = ? AND lemma = ?''',
              (chat_id, sender, lemma))
    # Если ни одна запись не была обновлена (т.е. не было найдено соответствующих записей),
    # тогда мы должны вставить новую запись
    if c.rowcount == 0:  # если количество строк, затронутых нашим последним запросом - 0
        c.execute('''INSERT INTO message_counts (chat_id, sender, lemma, count)
                     VALUES (?, ?, ?, 1)''', (chat_id, sender, lemma))
    # Фиксируем изменения в базе данных
    conn.commit()