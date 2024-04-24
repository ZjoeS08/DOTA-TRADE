import random
import telebot
import py.config as cfg
import py.database as DataBase
import py.keyboards as Keyboards
import py.masters.parse_master as ParseMaster
import py.masters.photo_master as PhotoMaster


def start(bot: telebot.TeleBot, message):
    user_id = message.chat.id
    user_name = message.from_user.first_name

    if not DataBase.is_exist(user_id):
        DataBase.register(user_id, user_name)

    with open(cfg.START_PHOTO_PATH, 'rb') as photo:
        bot.send_photo(user_id, photo, f'Привет, {user_name}. Я помогу тебе узнать актуалбные цены на предметы dota. Чтобы начать работу, нажми "Парсинг"',
                       reply_markup=Keyboards.get_main())


def parse(bot: telebot.TeleBot, message):
    user = DataBase.get_user(message.chat.id)

    if user is None:
        return

    if user.status != cfg.UFREE:
        bot.send_message(user.user_id, "Я уже занят, дождитесь, когда я закончу работу!",
                         reply_markup=Keyboards.get_empty())
        return

    DataBase.update(user.user_id, status=cfg.UWORK)

    bot.send_message(user.user_id, "Начинаю сбор данных, пожалуйста, подождите...", reply_markup=Keyboards.get_empty())

    items = ParseMaster.get_items()

    DataBase.update(user.user_id, status=cfg.UFREE)

    if items is None:
        answer = f"Произошел сбой при попытке запросить данные... попробуйте еще раз"
        bot.send_message(user.user_id, answer, reply_markup=Keyboards.get_main())

    elif len(items) == 0:
        answer = f"Парсинг завершен. К сожалению, не удалось найти ни одного предмета..."
        bot.send_message(user.user_id, answer, reply_markup=Keyboards.get_main())

    else:
        count = len(items)

        excel = ParseMaster.get_excel(items)

        items = random.sample(items, 5)

        head_items = ""
        for i, item in enumerate(items):
            head_items += f"{i + 1}. {item['market_hash_name']}\n"

        if excel is not None:
            answer = f"Парсинг завершен.\n\nНайдено предметов: {count}\n\nСлучайные из них:\n{head_items}\nВы также можете скачать Excel файл, чтобы посмотреть информацию о всех предметах!"
            bot.send_document(user.user_id, excel, visible_file_name="items.xlsx", caption=answer,
                              reply_markup=Keyboards.get_main())

        else:
            answer = f"Парсинг завершен.\n\nНайдено предметов: {count}\n\nСлучайные из них:\n{head_items}\nК сожалению, мне не удалось создать таблицу excel из полученных предметов..."
            bot.send_message(user.user_id, answer, reply_markup=Keyboards.get_main())


def edit_photo(bot: telebot.TeleBot, message):
    user = DataBase.get_user(message.chat.id)

    if user is None:
        return

    if user.status != cfg.UFREE:
        bot.send_message(user.user_id, "Я уже занят, дождитесь, когда я закончу работу!", reply_markup=Keyboards.get_empty())
        return

    DataBase.update(user.user_id, status=cfg.UWORK)

    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    file_path = file_info.file_path

    bot.send_message(user.user_id, "Начинаю обработку фотографии... Пожалуйста, подождите",
                     reply_markup=Keyboards.get_empty())

    downloaded_file = bot.download_file(file_path)

    DataBase.update(user.user_id, status=cfg.UFREE)

    edited_photo = PhotoMaster.get_new_photo(downloaded_file)

    if edited_photo is None:
        answer = "К сожалению, не удалось обработать фотографию... Попробуйте еще раз"
        bot.send_message(user.user_id, answer, reply_markup=Keyboards.get_main())

    else:
        answer = "Ваша обработанная фотография"
        bot.send_photo(user.user_id, edited_photo, answer, reply_markup=Keyboards.get_main())


def content_text(bot: telebot.TeleBot, message):
    user_id = message.chat.id
    text = message.text

    if "парсинг" in text.lower():
        parse(bot, message)

    elif "ч/б" in text.lower():
        bot.send_message(user_id, "Отправь мне любую фотографию, а я преобразую ее в черно-белый формат!",
                         reply_markup=Keyboards.get_main())

    else:
        bot.send_message(user_id, "Не понимаю твою команду, попробуй другую :)", reply_markup=Keyboards.get_main())
