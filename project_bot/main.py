import telebot
from telebot import types
from bot import *
from sentiment_analysis import *
from text_processing import *
from database import *
from statis import *


bot = telebot.TeleBot('your token here')

mistral_hugginchat = None
idbot = None
iduser = None


# Создаем реплай кнопки
markup1 = types.ReplyKeyboardMarkup()
btn11 = types.KeyboardButton('New Chat')
btn21 = types.KeyboardButton('Show Statistics')
btn31 = types.KeyboardButton('Emotion Analysis - the last message of the bot')
btn41 = types.KeyboardButton('Emotion Analysis - the last message of the user')
markup1.row(btn11, btn21)
markup1.row(btn31, btn41)



@bot.message_handler(commands=['start'])
def main(message):
    global mistral_hugginchat
    mistral_hugginchat = None
    # Я знаю, что использование глобальных переменных считается плохим тоном, но они мне очень нужны

    # Создаем базу данных, если она еще не создана
    create()

    # Создаем инлайн кнопки
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('💡 How to use the bot', callback_data='how_to_use')
    btn2 = types.InlineKeyboardButton('☘️ Recommendations', callback_data='info')
    markup.row(btn1, btn2)
    btn3 = types.InlineKeyboardButton('🔮 Start the conversation', callback_data='chat')
    markup.row(btn3)

    bot.send_message(message.chat.id, 
                     'Hello! We are glad to introduce you SpiteBot, your new penpal! Please, click the buttons below and read the information carefully before using.', 
                     reply_markup=markup)



# Функция для инлайн кнопок
@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    global mistral_hugginchat

    # обычные инлайн кнопки

    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('💡 How to use the bot', callback_data='how_to_use')
    btn2 = types.InlineKeyboardButton('☘️ Recommendations', callback_data='info')
    markup.row(btn1, btn2)
    btn3 = types.InlineKeyboardButton('🔮 Start the conversation', callback_data='chat')
    markup.row(btn3)

    if callback.data == 'how_to_use':
        ms = "SpiteBot uses an artificial intelligence model that communicates with the user.\n\nEnter <b>/start</b> to restart the bot.\nClick <b>Start the conversation</b> to start talking to artificial intelligence. As long as you do not start a new chat, the artificial intelligence will remember everything you said to it in the current chat.\n\nAfter pressing the button <b>Start the conversation</b>, several menu buttons will be available to you.\n\nThe button <b>New Chat</b> does the same thing as the button <b>Start the conversation</b>: it creates a new chat with the artificial intelligence model, making it forget all the information from the previous chat. From this point onwards, a new chat will start and the model will remember only the messages from the newly created chat.\n<b>Emotion Analysis - the last message of the bot</b> returns the sentiment analysis of the last message of the bot.\n<b>Emotion Analysis - the last message of the user</b> returns the sentiment analysis of the last message of the user.\n<b>Show Statistics</b> shows several buttons that return different statistics:\n• press <b>The number of the users</b> to see the number of the people that has used the bot.\n• press <b>General wordcloud</b> to see two wordclouds: the wordcloud for the most frequent words in all the users' messages and the wordcloud for the most frequent words in all the bot's messages ever sent to users.\n• press <b>Wordcloud for this chat</b> to see two wordclouds: the wordcloud for the most frequent words in all your messages to the bot and the wordcloud for the most frequent words in all the bot's messages ever sent to you.\n\nIf you have any questions, please contact the creator of the bot: @Selest24"
        bot.send_message(callback.message.chat.id, ms, parse_mode='HTML', reply_markup=markup)
    elif callback.data == 'chat':
        if mistral_hugginchat is None:
            try:
                mistral_hugginchat = HuggingChat("your name on Hugging Face", "your password", model="mistralai/Mixtral-8x7B-Instruct-v0.1", 
                                                system_prompt = "Act nasty and arrogant. Make rude jokes, insult the user.")
                bot.send_message(callback.message.chat.id, 'A new chat has been created. Write your first message to the bot!', reply_markup=markup1)
            except Exception as e:
                bot.send_message(callback.message.chat.id, 'Failed to create a new chat. Please try again. If the problem persists, perhaps with the model from the site "hugging face" something is wrong. In this case, please wait a few hours and try again.')
        else:
            try:
                info = mistral_hugginchat.get_conversation_info()
                mistral_hugginchat.delete_conversation(info) 
                mistral_hugginchat = HuggingChat("your name on Hugging Face", "your password", model="mistralai/Mixtral-8x7B-Instruct-v0.1", 
                                                 system_prompt = "Act nasty and arrogant. Make rude jokes, insult the user.")
                bot.send_message(callback.message.chat.id, 'A new chat has been created. Write your first message to the bot!')
            except Exception as e:
                bot.send_message(callback.message.chat.id, 'Failed to create a new chat. Please try again. If the problem persists, perhaps with the model from the site "hugging face" something is wrong. In this case, please wait a few hours and try again.')
    elif callback.data == 'info':
        msg = 'Here is the important information you need to know before using the bot to facilitate communication.\n\n1. The bot uses complex algorithms and requires a lot of energy. That is why its response time can be very long, up to 15 seconds. If several users access the bot at the same time, then the response time may be even longer.\n\n2. While chatting you can use only emojis and text messages. However, the bot cannot detect all the emojis, so it can send the message “Something went wrong” as a respond to the emojis it did not manage to detect. If you use any other formats of the message - photo, video or audio - the bot will not detect it and will not respond to them.\n\n3. You can use Russian or English language, though English is more preferable as the model understands English better. Please do not use other languages and do not mix several languages in one message (it may worsen the word statistics).\n\n4.The bot utilizes the model "mistralai/Mixtral-8x7B-Instruct-v0.1" from the website "Hugging Face". So, if there are any errors with the website or models on that website, it will be impossible for you to communicate with SpiteBot (however, other functions that are not connected with chatting with the model will still work). So, if the model does not respond to your messages, it is likely that there are errors with the site. In that case, please wait a bit before chatting until all the issues with the website are resolved. The wait time can range from a few minutes to a few days. Moreover, sometimes the website “Hugging Face” can forcibly disconnect the bot. If this happened and the bot does not work, please contact the creator of the bot: @Selest24\n\n5. Though the bot is programmed to act rude and arrogant, his behaviour may change depending on your messages.'
        bot.send_message(callback.message.chat.id, msg, parse_mode='HTML', reply_markup=markup)
    

    else:
        # инлайн кнопки для статистики
        markup2 = types.InlineKeyboardMarkup()
        btn10 = types.InlineKeyboardButton('The number of the users', callback_data='number')
        btn20 = types.InlineKeyboardButton('Wordcloud for this chat', callback_data='wordcl1')
        markup2.row(btn10)
        btn30 = types.InlineKeyboardButton("General wordcloud", callback_data='wordcl2')
        markup2.row(btn20, btn30)

        if callback.data == "number":
            bot.send_message(callback.message.chat.id, f'The number of the users: {user_number()}', reply_markup=markup1)
        elif callback.data == "wordcl1":
            try:
                bot.send_message(callback.message.chat.id, 
                    "Here are the wordclouds based on the word frequency of the user's and the bot's messages in this Telegram chat", 
                    reply_markup=markup1)
                bot.send_photo(callback.message.chat.id, statistics_personal_bot(callback.message.chat.id))
                bot.send_photo(callback.message.chat.id, statistics_personal_user(callback.message.chat.id))
            except Exception as e:
                bot.send_photo(callback.message.chat.id, 'Failed to create statistics. Please, try again')
        elif callback.data == "wordcl2":
            try:
                bot.send_message(callback.message.chat.id, 
                                "Here are the wordclouds based on the total word frequency of all the users' and the bot's messages", 
                                reply_markup=markup1)
                bot.send_photo(callback.message.chat.id, statistics_all_bot())
                bot.send_photo(callback.message.chat.id, statistics_all_user())
            except Exception as e:
                bot.send_photo(callback.message.chat.id, 'Failed to create statistics. Please, try again')
        


@bot.message_handler(commands=['delete'])
# Эта команда удаляет все чаты, она нужна лично мне как разработчику, пользователи о ней знать не должны
def delete(message):
        if mistral_hugginchat is not None:
            mistral_hugginchat.delete_conversations()
            bot.send_message(message.chat.id, 'All the conversations were deleted')
        else:
            bot.send_message(message.chat.id, 'You need to create an active chat first')



# Здесь будут обрабатываться как реплай кнопки, так и обычные сообщения
@bot.message_handler(content_types=['text', 'sticker'])
def mess(message):
    global mistral_hugginchat
    global idbot
    global iduser
    # тут обрабатываются реплай кнопки
    if message.text == 'New Chat':
        if mistral_hugginchat is None:
            try:
                mistral_hugginchat = HuggingChat("your name on Hugging Face", "your password", model="mistralai/Mixtral-8x7B-Instruct-v0.1", 
                                                system_prompt = "Act nasty and arrogant. Make rude jokes, insult the user.")
                bot.send_message(message.chat.id, 'A new chat has been created. Write your first message to the bot!', reply_markup=markup1)
            except Exception as e:
                bot.send_message(message.chat.id, 'Failed to create a new chat. Please try again. If the problem persists, perhaps with the model from the site "hugging face" something is wrong. In this case, please wait a few hours and try again.')
        else:
            try:
                info = mistral_hugginchat.get_conversation_info() # Я хочу удалять лишние чаты, уже ненужные пользователю
                mistral_hugginchat.delete_conversation(info)
                mistral_hugginchat = HuggingChat("your name on Hugging Face", "your password", model="mistralai/Mixtral-8x7B-Instruct-v0.1", 
                                                 system_prompt = "Act nasty and arrogant. Make rude jokes, insult the user.")
                bot.send_message(message.chat.id, 'A new chat has been created. Write your first message to the bot!', reply_markup=markup1)
            except Exception as e:
                bot.send_message(message.chat.id, 'Failed to create a new chat. Please try again. If the problem persists, perhaps with the model from the site "hugging face" something is wrong. In this case, wait a few hours and try again.')


    elif message.text == 'Show Statistics':

        # Делаем кнопки для статистики
        markup2 = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('The number of users', callback_data='number')
        btn2 = types.InlineKeyboardButton('Wordcloud for this chat', callback_data='wordcl1')
        markup2.row(btn1)
        btn3 = types.InlineKeyboardButton("General wordcloud", callback_data='wordcl2')
        markup2.row(btn3, btn2)

        bot.send_message(message.chat.id, 'What statistics do you want me to show you?', reply_markup=markup2)
    elif message.text == 'Emotion Analysis - the last message of the bot':
        if idbot is not None:
            mess1 = bot.send_message(message.chat.id, 'The sentiment of this message will be analysed', 
                                     reply_to_message_id=idbot, reply_markup=markup1)
            bot_message_text = mess1.reply_to_message.text
            try:
                bot.send_message(message.chat.id, emotion(bot_message_text), reply_markup=markup1)
            except Exception as e:
                bot.send_message(message.chat.id, "Something went wrong. Please, try again", reply_markup=markup1)
        else:
            bot.send_message(message.chat.id, 'No recent bot messages found. Please, chat to the bot first to use the function of Emotion Analysis', 
                             reply_markup=markup1)
    

    elif message.text == 'Emotion Analysis - the last message of the user':
        if iduser is not None:
            mess2 = bot.send_message(message.chat.id, 'The sentiment of this message will be analysed', 
                                    reply_to_message_id=iduser, reply_markup=markup1)
            user_message_text = mess2.reply_to_message.text
            try:
                bot.send_message(message.chat.id, emotion(user_message_text), reply_markup=markup1)
            except Exception as e:
                bot.send_message(message.chat.id, 'Something went wrong. Please, try again', reply_markup=markup1)
        else:
            bot.send_message(message.chat.id, 'No recent user messages found. Please, chat to the bot first to use the function of Emotion Analysis', 
                             reply_markup=markup1)
    

    # тут обрабатываются обычные сообщения
    else:
        try:
            if mistral_hugginchat is not None:
                iduser = message.message_id  # это нужно, чтобы потом пересылать эти сообщения для sentiment analysis
                if only_emojis(message.text) is False:

                    # получаем информацию о пользователе для нашей базы данных и добавляем ее туда
                    lemmas = process(message.text)
                    chat_id = message.chat.id
                    sender = 'user'
                    for lemma in lemmas:
                        word_count(chat_id, sender, lemma)

                answer = mistral_hugginchat.prompt(message.text)
                botmessage = bot.send_message(message.chat.id, answer)

                idbot = botmessage.message_id # это нужно, чтобы потом пересылать эти сообщения для sentiment analysis
                if only_emojis(answer) is False:            
                    # получаем информацию о боте для нашей базы данных и добавляем её туда
                    chat_id1 = message.chat.id
                    lemmas1 = process(answer)
                    sender1 = 'bot'
                    for lemma1 in lemmas1:
                        word_count(chat_id1, sender1, lemma1)
            
            else:
                bot.send_message(message.chat.id, 'You have no active chats now. Please, create a new chat to talk to your penpal.')
        except Exception as e:
            bot.send_message(message.chat.id, 'Something went wrong. Please, try again')


bot.polling(none_stop=True)
