from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from bot.db import channels
import datetime


def create_keyboard(name_buttons: list | dict, *sizes) -> types.InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    for name_button in name_buttons:
        if type(name_buttons[name_button]) is tuple:
            if len(name_buttons[name_button]) == 2:
                keyboard.button(
                    text=name_button, url=name_buttons[name_button][0], callback_data=name_buttons[name_button][1]
                )
            else:
                if "http" in name_buttons[name_button]:
                    keyboard.button(
                        text=name_button, url=name_button
                    )
                keyboard.button(
                    text=name_button, callback_data=name_button
                )

        else:

            if "http" in str(name_buttons[name_button]):
                keyboard.button(
                    text=name_button, url=name_buttons[name_button]
                )
            else:
                keyboard.button(
                    text=name_button, callback_data=name_buttons[name_button]
                )
    if len(sizes) == 0:
        sizes = (1,)
    elif type(sizes[0]) is list:
        sizes = sizes[0]
    keyboard.adjust(*sizes)
    return keyboard.as_markup(resize_keyboard=True, one_time_keyboard=True)


def create_reply_keyboard(name_buttons: list, one_time_keyboard: bool = False, request_contact: bool = False,
                          *sizes) -> types.ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()

    for name_button in name_buttons:
        if name_button is not tuple:
            keyboard.button(
                text=name_button,
                request_contact=request_contact
            )
        else:
            keyboard.button(
                text=name_button,
                request_contact=request_contact

            )
    if len(sizes) == 0:
        sizes = (1,)
    keyboard.adjust(*sizes)
    return keyboard.as_markup(resize_keyboard=True, one_time_keyboard=one_time_keyboard)


def keyboard_channel_category() -> types.InlineKeyboardMarkup:
    all_category = channels.get_category()
    keyboard = create_keyboard(all_category)
    return keyboard


def button_date() -> dict:
    now = datetime.datetime.now()
    buttons = {f"Сегодня ({now.strftime('%d/%m')})": now.strftime('%d/%m'),
               f"Завтра ({(now + datetime.timedelta(days=1)).strftime('%d/%m')})":
                   (now + datetime.timedelta(days=1)).strftime('%d/%m')
               }
    for i in range(2, 7):
        date = (now + datetime.timedelta(days=i)).strftime('%d/%m')
        buttons.update({date: date})

    # keyboard = create_keyboard(buttons)
    return buttons


def get_channel_category(category) -> types.InlineKeyboardMarkup:
    if "без категории" in category:
        city = category.split(' ')[0]
        district = "без категории"
    else:
        city, district = category.split(" ")

    all_name = channels.get_name(city, district)
    keyboard = create_keyboard(all_name)
    return keyboard


greeting_kb = create_reply_keyboard(["Прайс-лист", "Купить рекламу"], True, False, 2)
buy_advertisement_kb = create_keyboard({"Купить рекламу": "buy_advertisement"})
document_kb = create_keyboard({"Подтвердить": "continue",
                               "Вернуться в начало": "buy_advertisement"})
fix_button = {
    "Не нужно закреплять": "no_fixing",
    "1 сутки": "1_day",
    "5 суток": "5_day",
    "7 суток": "7_day",
    "30 суток": "30_day",
}
fixing_kb = create_keyboard(fix_button)
# update_content = {
#     "Направить новую информацию": "continue",
#     "Вернуться в начало": "buy_advertisement"
# }
kb_by_time = create_keyboard({"Вернуться к выбору даты": "next_step_2"})
cancel_post_kb = create_keyboard({"Направить новую информацию": "continue",
                                  "Вернуться в начало": "buy_advertisement"})
success_payment_kb_user = create_keyboard({
    "Подтвердить": "ready_post",
    "Изменить содержимое поста": "continue",
    "Изменить дату публикации": "next_step_2"
})
check_pay_kb = create_keyboard({"Готово": "check_pay"})
admin_kb = create_keyboard({"Рассылка": "mailing", "Открепить все сообщения": "unfix_all"})
change_profile_kb = create_keyboard({"Изменить данные": "change_profile"})
del_mes_kb = create_keyboard({"Удалить сообщение": "del_messages"})
