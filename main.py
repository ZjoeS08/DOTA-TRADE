import os
import telebot
import py.config as cfg
import py.database as DataBase
import py.bot_handlers as BHandlers



def start_bot():
    bot = telebot.TeleBot(cfg.TELEGRAM_BOT_TOKEN)
    print("[BOT] Бот успешно запущен!")
    
    try:
        @bot.message_handler(commands = ["start"])
        def start(message):
            BHandlers.start(bot, message)

        @bot.message_handler(commands = ["parse"])
        def parse(message):
            BHandlers.parse(bot, message)    

        @bot.message_handler(content_types=['photo'])
        def handle_photo(message):
            BHandlers.edit_photo(bot, message)     

        @bot.message_handler(content_types=["text"])
        def content_text(message):
            BHandlers.content_text(bot, message) 

    except Exception as e:
        print(f"[BOT] Произошла ошибка: {e}")
              
    bot.infinity_polling()



def main():

    DataBase.create()
    DataBase.reset_status()

    start_bot()



if __name__ == "__main__":
    main()
