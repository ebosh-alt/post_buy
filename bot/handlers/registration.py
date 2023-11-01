from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from bot import keyboards as kb
from bot.config import bot
from bot.const import Profile
from bot.db import users, User
from bot.utils.GetMessage import get_mes
from bot.states import States

router = Router()


@router.callback_query(F.data == "change_profile")
async def change_profile(call: CallbackQuery, state: FSMContext):
    id = call.from_user.id
    await state.set_state(States.profile)
    await state.update_data(profile=Profile())
    await state.update_data(message_id=call.message.message_id)
    await bot.edit_message_text(chat_id=id,
                                message_id=call.message.message_id,
                                text=get_mes("greeting_new_user"))


@router.message(States.profile)
async def register(message: Message, state: FSMContext):
    id = message.from_user.id
    data = await state.get_data()
    profile: Profile = data.get("profile")
    message_id = data.get("message_id")
    await bot.delete_message(chat_id=id, message_id=message.message_id)
    if profile.name_organization == "Unknown":
        profile.name_organization = message.text
        mes = f"Наименование организации: {profile.name_organization}\nВведите номер телефона:\n\n" \
              f"Пример: +7(999)8887766"
        await bot.edit_message_text(chat_id=id,
                                    message_id=message_id,
                                    text=mes)
        await state.update_data(profile=profile)
    elif profile.number_phone == "Unknown":
        profile.number_phone = message.text
        await state.update_data(profile=profile)
        mes = f"Наименование организации: {profile.name_organization}\nНомер телефона: {profile.number_phone}\n" \
              f"Введите ИНН:"
        await bot.edit_message_text(chat_id=id,
                                    message_id=message_id,
                                    text=mes)
    elif profile.inn == "Unknown":
        profile.inn = message.text

        mes = get_mes("profile", firstname=message.from_user.first_name,
                      name_organization=profile.name_organization, number_phone=profile.number_phone, inn=profile.inn)
        await bot.edit_message_text(chat_id=id,
                                    message_id=message_id,
                                    text=mes,
                                    reply_markup=kb.change_profile_kb)

        user = User(id=id)
        user.name_organization = profile.name_organization
        user.number_phone = profile.number_phone
        user.inn = profile.inn
        if id in users:
            users.update(user)
        else:
            users.add(user)
            await bot.send_message(chat_id=id,
                                   text=get_mes("greeting"),
                                   reply_markup=kb.greeting_kb)
        await state.clear()


registration_rt = router
