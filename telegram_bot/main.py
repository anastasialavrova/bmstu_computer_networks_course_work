import telebot
from agegender_demo import main_module
from telebot import types

TOKEN = "1302614481:AAE746treHjT9MUCr7bh_d7FdOQGF-lCL8g"

knownUsers = []
userStep = {}

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id
    if cid not in knownUsers:
        knownUsers.append(cid)
        userStep[cid] = 0
        bot.send_message(cid,
                         "Привет! Я вижу ты тут впервые! Загрузи фотографию и узнай возраст и пол человека на ней :)")
    else:
        bot.send_message(cid,
                         "Ух ты! А мы раньше не встречались? Загрузи фотографию и узнай возраст и пол человека на ней :)")


@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_default(m):
    bot.send_message(m.chat.id, "Попробуй еще раз! Загрузи фотографию и узнай возраст и пол человека на ней :)")


@bot.message_handler(func=lambda message: True, content_types=['photo'])
def photo(message):
    print('message.photo =', message.photo)

    if message.photo is not None:
        fileID = message.photo[-1].file_id
        print('fileID =', fileID)
        file_info = bot.get_file(fileID)
        print('file.file_path =', file_info.file_path)
        downloaded_file = bot.download_file(file_info.file_path)

        with open("image.jpg", 'wb') as new_file:
            new_file.write(downloaded_file)

        res_age, res_gender = main_module("image.jpg")

        if (res_age == 0):
            bot.reply_to(message, "Я тебя не вижу! Попробуй еще раз!")
            return
        print("RES: ", res_age, res_gender)
        k = res_age % 10
        if (res_age > 9) and (res_age < 20) or (res_age > 110) or (k > 4) or (k == 0):
            res_age_word = ' лет'
        else:
            if k == 1:
                res_age_word = ' год'
            else:
                res_age_word = ' года'
        res_str = "Ты " + str(res_gender) + ". " + "Тебе " + str(res_age) + res_age_word + "."
        bot.reply_to(message, res_str)
    else:
        return


bot.polling(none_stop=True)

while True:
    pass
