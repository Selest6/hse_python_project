# SpiteBot
Ссылка на бота: https://t.me/Spite8_bot <br>
Выложен на pythonanywhere, но с урезанными функциями (в связи с ограничениями на занимаемый объем памяти).<br>
Для полноценной работы его необходимо запустить локально.
<br>

### План readme:
### 1. Общее описание бота
### 2. Описание функционала и кнопок
### 3. Особенности работы бота
### 4. Структура проекта и запуск

<br>

# 1. Общее описание бота
SpiteBot - это телеграм бот, который может делать следующее:

1. Переписываться с моделью "mistralai/Mixtral-8x7B-Instruct-v0.1" с сайта "Hugging Face". Он получает доступ к этой модели через API, с помощью библиотеки hugchat, и по сути своей переносит интерфейс "чатов" с моделями на hugging face (см. https://huggingface.co/chat/) в телеграмм. Так, например, в телеграмме можно создавать новые чаты с моделью точно так же, как и на сайте (и на сайте в этот момент создастся новый чат от лица моего аккаунта).
2. Анализировать сообщения и возвращать как общий "настрой" сообщения (negative, positive, neutral), так и конкретные эмоции, содержащиеся в нём. Для этого используются соответствующие модели hugging face.
ВНИМАНИЕ! ЭТА ФУНКЦИЯ РАБОТАЕТ ТОЛЬКО НА ЛОКАЛЬНОМ КОМПЬЮТЕРЕ, НА СЕРВЕРЕ ОНА УРЕЗАНА ИЗ-ЗА БОЛЬШОГО ОБЪЕМА ПАМЯТИ.
3. Делать вордклауды, обкачивая информацию из базы данных. В свою очередь, в базу данных помещаются леммы всех слов из всех сообщений как пользователя, так и бота, и пишется, сколько раз у конкретного пользователя была употреблена та или иная лемма.
ВНИМАНИЕ! ЭТА ФУНКЦИЯ ТОЖЕ РАБОТАЕТ ТОЛЬКО НА ЛОКАЛЬНОМ КОМПЬЮТЕРЕ, НА СЕРВЕРЕ ОНА УРЕЗАНА ИЗ-ЗА БОЛЬШОГО ОБЪЕМА ПАМЯТИ.

# 2. Описание функционала и кнопок
(я скопирую сюда информацию из бота и отмечу те кнопки, которые из-за проблем с объемом памяти работают только на локальном компьютере, а не в ограниченном пространстве pythonanywhere)

SpiteBot uses an artificial intelligence model that communicates with the user.

Enter /start to restart the bot.
Click Start the conversation to start talking to artificial intelligence. As long as you do not start a new chat, the artificial intelligence will remember everything you said to it in the current chat.

After pressing the button Start the conversation, several menu buttons will be available to you.

The button New Chat does the same thing as the button Start the conversation: it creates a new chat with the artificial intelligence model, making it forget all the information from the previous chat. From this point onwards, a new chat will start and the model will remember only the messages from the newly created chat.<br>
Emotion Analysis - the last message of the bot returns the sentiment analysis of the last message of the bot. (ДОСТУПНО ТОЛЬКО НА ЛОКАЛЬНОМ КОМПЬЮТЕРЕ)<br>
Emotion Analysis - the last message of the user returns the sentiment analysis of the last message of the user. (ДОСТУПНО ТОЛЬКО НА ЛОКАЛЬНОМ КОМПЬЮТЕРЕ)<br>
Show Statistics shows several buttons that return different statistics: (ЭТА ФУНКЦИЯ И ФУНКЦИИ НИЖЕ ДОСТУПНЫ ТОЛЬКО НА ЛОКАЛЬНОМ КОМПЬЮТЕРЕ)<br>
• press The number of the users to see the number of the people that has used the bot.<br>
• press General wordcloud to see two wordclouds: the wordcloud for the most frequent words in all the users' messages and the wordcloud for the most frequent words in all the bot's messages ever sent to users.<br>
• press Wordcloud for this chat to see two wordclouds: the wordcloud for the most frequent words in all your messages to the bot and the wordcloud for the most frequent words in all the bot's messages ever sent to you.<br>

If you have any questions, please contact the creator of the bot: @Selest24

# 3. Особенности работы бота (вся информация продублирована из инструкций к боту)
Here is the important information you need to know before using the bot to facilitate communication.

1. The bot uses complex algorithms and requires a lot of energy. That is why its response time can be very long, up to 15 seconds. If several users access the bot at the same time, then the response time may be even longer.

2. While chatting you can use only emojis and text messages. However, the bot cannot detect all the emojis, so it can send the message “Something went wrong” as a respond to the emojis it did not manage to detect. If you use any other formats of the message - photo, video or audio - the bot will not detect it and will not respond to them.

3. You can use Russian or English language, though English is more preferable as the model understands English better. Please do not use other languages and do not mix several languages in one message (it may worsen the word statistics).

4. The bot utilizes the model "mistralai/Mixtral-8x7B-Instruct-v0.1" from the website "Hugging Face". So, if there are any errors with the website or models on that website, it will be impossible for you to communicate with SpiteBot (however, other functions that are not connected with chatting with the model will still work). So, if the model does not respond to your messages, it is likely that there are errors with the site. In that case, please wait a bit before chatting until all the issues with the website are resolved. The wait time can range from a few minutes to a few days. Moreover, sometimes the website “Hugging Face” can forcibly disconnect the bot. If this happened and the bot does not work, please contact the creator of the bot: @Selest24

5. Though the bot is programmed to act rude and arrogant, his behaviour may change depending on your messages.

# 4. Структура проекта и запуск

Чтобы запустить бота, запустите файл main.py.Для корректной работы нужно установить следующие библиотеки:<br><br>
pip install pyTelegramBotAPI<br>
pip install hugchat<br>
pip install transformers<br>
pip install matplotlib<br>
pip install wordcloud<br>
pip install spacy<br>
pip install langdetect<br><br>
Версии библиотек указаны в файле requirements.txt. Также будьте готовы к тому, что при первом запуске кода на компьютер будет загружено 4 модели (2 с hugging face, 2 - из spacy).<br><br>
Структура проекта:
<br>

bot.py - здесь находятся функции для вызова непосредственно Mixtral с hugging face по API (в качестве API-токенов используется логин и пароль от hugging face)<br><br>
chat_data.db - база данных, куда сохраняются: id чата (для идентификации и подсчёта пользователей + для подсчёта сообщений внутри чата), тип отправителя (человек или робот, иными словами, устанавливаем, кому сообщение принадлежит), лемма того или иного слова, количество раз, которое это слово было употрблено в чате с конкретным id. В базе данных собираются леммы всех сообщений, когда-либо сгенерированных ботом и пользователями.<br><br>
database.py - там собраны функции, работающие с базой данных: создание базы данных, а также запись и учёт новых слов.<br><br>
main.py - непосредственно бот со всеми кнопками и их функциями<br><br>
sentiment_analysis.py - там загружаются 2 модели с hugging face для распознавания эмоций в тексте и его общего настроения, всё это обкачивается и возвращается функцией в красивом виде.<br><br>
statis.py - там собраны функции для генерации вордклаудов по отдельными частям-таблицам базы данных.<br><br>
text_processing.py - там собраны функции для обкачивания сообщений, т.е. для токенизации и лемматизации текста. Отдельное внимание уделено смайликам в сообщениях, каждый текст анализируется на предмет их наличия, и, если они есть, они оттуда удаляются (в том числе и потому, что результат работы функции лемматизации передается в базу данных).

