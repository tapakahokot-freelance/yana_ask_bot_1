from aiogram import types
from aiogram.types import InputFile
from aioschedule import (
    every as schedule_every,
    run_pending as schedule_run_pending,
)
from asyncio import sleep as asleep

import callbacks
import states
from settings import settings
from db import User


async def answer_photo(message: types.Message, file_key, caption, **kwargs):
    file = settings.files[file_key]
    if file['id'] is None:
        input_file = InputFile(file['path'])
    else:
        input_file = file['id']

    message: types.Message = await message.answer_photo(input_file, caption=caption, **kwargs)
    if file['id'] is None:
        file['id'] = message.photo[0].file_id


async def answer_file(message: types.Message, file_key, caption, **kwargs):
    file = settings.files[file_key]
    if file['id'] is None:
        input_file = InputFile(file['path'])
    else:
        input_file = file['id']

    message: types.Message = await message.answer_document(input_file, caption=caption, **kwargs)
    if file['id'] is None:
        file['id'] = message.document.file_id


async def run_schedule():
    schedule_every().day.at("12:30").do(day_2_hi_message)
    schedule_every().day.at("12:31").do(day_2_lesson_message)
    schedule_every().day.at("12:55").do(day_2_ask_message)

    schedule_every(15).minutes.do(remember)

    schedule_every().day.at("12:30").do(day_3_hi_message)
    schedule_every().day.at("12:31").do(day_3_hi_message_2)
    schedule_every().day.at("12:32").do(day_3_hi_message_3)

    while True:
        await schedule_run_pending()
        await asleep(15)


async def day_2_hi_message():
    for user in User.get_all():
        if user.day_number == 1 and user.is_waiting_next_day:
            await settings.bot.send_message(
                chat_id=user.chat_id,
                text="Привет-привет, будущий студент зарубежного университета! Как твои дела? "
                     "Продолжаем наше секретное задание 😉 надеюсь, ты полон сил!"
            )


async def day_2_lesson_message():
    for user in User.get_all():
        if user.day_number == 1 and user.is_waiting_next_day:
            await settings.bot.send_message(
                chat_id=user.chat_id,
                text="А вот уже готовый второй урок на очереди."
            )
            await settings.bot.send_message(
                chat_id=user.chat_id,
                text="Я рада поделиться своей историей и надеюсь, что вскоре ты сможешь также делиться своей! "
                     "На самом деле, поступить за границу бесплатно вполне реально, и я точно уверена, что у тебя "
                     "тоже получится! Скорее переходи и смотри",
                reply_markup=callbacks.link_kb('Ссылка', 'https://youtu.be/h4qsFt1g20Y')
            )


async def day_2_ask_message():
    for user in User.get_all():
        if user.day_number == 1 and user.is_waiting_next_day:
            await settings.bot.send_message(
                chat_id=user.chat_id,
                text="Ну как? Удалось посмотреть мое видео? Точно смотрел внимательно?",
                reply_markup=callbacks.ok_kb(day=2, step=4)
            )
            user.day_number = 2
            user.is_waiting_next_day = False
            user.save()


async def remember():
    for user in User.get_all():
        if user.day_number == 2 and user.state in (str(states.Form.waiting_inside), str(states.Form.waiting_three_things)):
            await settings.bot.send_message(
                chat_id=user.chat_id,
                text="Так-так, не вижу твоего инсайта :( неужели тебе не интересно, что ждет тебя в конце?",
            )
        if user.day_number == 1 and user.state == str(states.Form.waiting_form):
            await settings.bot.send_message(
                chat_id=user.chat_id,
                text="Не забыл? Поставь +, когда заполнишь анкету",
                reply_markup=callbacks.ok_kb(day=1, step="10.1")
            )


async def day_3_hi_message():
    for user in User.get_all():
        if user.day_number == 2 and user.state is None and user.is_waiting_next_day:
            await settings.bot.send_message(
                chat_id=user.chat_id,
                text="Ну что, я посмотрела твое домашнее задание! Ты действительно усвоил материал, но, конечно, "
                     "есть много чего, что можно подкорректировать!"
            )
            await settings.bot.send_message(
                chat_id=user.chat_id,
                text="Во-первых, не забывай, что твой план поступления должен начинаться с выстраивания целостной "
                     "стратегии, куда включены таблица со всеми дедлайнами, дорожная карта пути, полный аудит и анализ "
                     "программ и стипендий, а также денежная декомпозиция ! Как раз все это - наш фундамент в "
                     "работе с клиентами."
            )


async def day_3_hi_message_2():
    for user in User.get_all():
        if user.day_number == 2 and user.state is None and user.is_waiting_next_day:
            await settings.bot.send_message(
                chat_id=user.chat_id,
                text="Во-вторых, сделай упор на свой личный бренд. Тут хорошо бы иметь не только академический "
                     "достижения, но и социо-культурные. Например, тут можно начать  вести свой блог, заняться "
                     "волонтерством, запустить свой проект и много чего еще."
            )


async def day_3_hi_message_3():
    for user in User.get_all():
        if user.day_number == 2 and user.state is None and user.is_waiting_next_day:
            await settings.bot.send_message(
                chat_id=user.chat_id,
                text="Если ты заинтересовался и хочешь действительно углубится в этот процесс и осуществить свою "
                     "мечту, то приглашаю тебя на БЕСПЛАТНУЮ консультацию, где наш менеджер сможет оценить твои "
                     "шансы и рассказать подробнее про наши услуги! ну как, интересно ли тебе предложение, напарник?",
                reply_markup=callbacks.yes_no_kb(day=3, step=6)
            )
            user.is_waiting_next_day = False
            user.save()
