import asyncio
import re

from aiogram import types
from aiogram.dispatcher import FSMContext

from settings import settings
from db import User

from services import answer_photo, answer_file
import callbacks, states, filters, services
from datetime import datetime as dt


@settings.dp.message_handler(commands=["start"])
async def start_cmd(message: types.Message):
    await message.answer(
        "Привет, будущий студент вуза мечты!\n"
        "Решение поступить в зарубежный ВУЗ Европы, Азии или США - одно из лучших твоих решений 🔥 "
        "Я верю, что у тебя все получится, и ты сможешь осуществить свою мечту!"
    )
    await answer_photo(
        message=message,
        file_key='day_1_step_2',
        caption="Сейчас ты в игровой воронке от C.Academy, которая помогла мне и другим студентам поступить в их вузы "
                "мечты за границей по стипендии!\n"
                "Тот, кто пройдёт все до конца и выполнит все домашние задания - получит наши подарки в виде "
                "чек-листов и гайдов по поступлению, а также информацию о топ-100 университетов мира!"
    )
    await asyncio.sleep(7)
    await answer_photo(
        message=message,
        file_key='day_1_step_3',
        caption="Проходи, добро пожаловать!"
    )
    await message.answer(
        "Кто-нибудь знает, что ты здесь?)",
        reply_markup=callbacks.ok_kb(day=1, step=3)
    )


@settings.dp.callback_query_handler(callbacks.ok_data().filter(day='1', step='3'))
async def ok_day_1_step_4(call: types.CallbackQuery):
    await answer_photo(
        message=call.message,
        file_key='day_1_step_4',
        caption="Тогда будем действовать быстро"
    )
    await call.message.answer(
        "Меня зовут Бадди, и я твой напарник. Сейчас мы будем выполнять секретную миссию, чтобы получить доступ "
        "к нашим сокровищам, которые уже ждут тебя на этом пути и в самом конце!"
    )
    await call.message.answer(
        "Обещаешь дойти до конца?",
        reply_markup=callbacks.ok_kb(day=1, step=4)
    )


@settings.dp.callback_query_handler(callbacks.ok_data().filter(day='1', step='4'))
async def ok_day_1_step_5(call: types.CallbackQuery):
    await call.message.answer("Это правильный ответ!")
    await call.message.answer(
        "А я в свою очередь гарантирую, что ты сможешь поступить в университет за границей "
        "по стипендии даже если сейчас:\n\n"
        "❌ Не знаешь, с чего начать\n"
        "❌ Боишься действовать\n"
        "❌ У тебя нет денег\n"
        "❌ Твои оценки далеки от идеальных\n"
        "❌ У тебя мало достижений\n\n"
        "Это получится сделать за счет:\n"
        "✅ нашей уникальной системы из 3 шагов\n"
        "✅ нашей поддержке\n"
        "✅ 5-летнему опыту и сотни кейсов\n"
        "✅ твоему большому желанию\n"
    )
    await asyncio.sleep(60)
    await answer_photo(
        message=call.message,
        file_key='day_1_step_5',
        caption="Думаешь, все так просто?"
    )
    await call.message.answer("Чтобы получить доступ к сокровищам, тебе нужно пройти проверку на секретность.")
    await call.message.answer("У тебя мало времени, действуй быстро.")
    await call.message.answer("Для начала нужно написать свой номер телефона  - проверка на секретность!")

    state = states.Form.waiting_phone
    await state.set()


@settings.dp.message_handler(
    state=states.Form.waiting_phone,
    regexp=re.compile('^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$')
)
async def enter_phone_number(message: types.Message, user: User, state: FSMContext):
    await state.finish()

    user.phone_number = message.text
    user.save()

    await message.answer(
        "Проверка пройдена, вот это крутой номер! Поэтому доступ к урокам открыт. "
        "Всего за 2 урока ты поймёшь пошаговый план, как поступить в вуз за границей и "
        "получить стипендию! Без сложных схем. Без запутанных шагов. Без стресса."
    )
    await message.answer(
        "ЖМИ НА КНОПКУ и переходи к вводному уроку",
        reply_markup=callbacks.link_kb('ССЫЛКА', 'https://youtu.be/6idCQ_8itiI')
    )
    await message.answer(
        "Скорее смотри 1ую часть видео, чтобы узнать больше про наши ценности и процесс поступления.\n"
        "Дальше будет только интереснее 🚀 и поставь галочку, когда посмотришь его.",
        reply_markup=callbacks.ok_kb(day=1, step=10)
    )


@settings.dp.message_handler(
    state=states.Form.waiting_phone,
    content_types=['any']
)
async def wrong_enter_phone_number(message: types.Message):
    await message.answer("Такими темпами ты не пройдешь проверку на секретность((\nЛучше напиши свой номер телефона :)")


@settings.dp.callback_query_handler(callbacks.ok_data().filter(day='1', step='10'))
async def ok_day_1_step_10(call: types.CallbackQuery, user: User):
    await call.message.answer("Ты крутой!")
    await call.message.answer(
        "А вот и первое домашнее задание - его важно выполнить, пусть это будет твой первый небольшой шаг на пути "
        "к большой мечте. Здесь ты ставишь свое намерение на поступление, “озвучиваешь” его, а значит, твой мозг "
        "воспринимает это не как что-то абстрактное, а тоже видит конкретную цель.\n"
        "После выполнения ты получишь чек-лист “8 шагов к поступлению за границу”:"
    )
    await call.message.answer(
        "Тебе нужно заполнить маленькую анкету, действуй\n",
        reply_markup=callbacks.link_kb('Анкета', 'https://forms.gle/rbdn2XE2qDgxCfLM9')
    )
    await call.message.answer(
        "Поставь +, когда заполнишь анкету",
        reply_markup=callbacks.ok_kb(day=1, step="10.1")
    )
    state = states.Form.waiting_form
    await state.set()

    user.state = str(states.Form.waiting_form)
    user.save()


@settings.dp.callback_query_handler(callbacks.ok_data().filter(day='1', step='10.1'), state=states.Form.waiting_form)
@settings.dp.callback_query_handler(callbacks.ok_data().filter(day='1', step='10.1'))
async def ok_day_1_step_10_1(call: types.CallbackQuery, user: User, state: FSMContext):
    await state.finish()

    user.state = None
    user.save()

    await call.message.answer(
        "Ну как? выполнил? Точно-точно выполнил?",
        reply_markup=callbacks.ok_kb(day=1, step=11)
    )


@settings.dp.callback_query_handler(callbacks.ok_data().filter(day='1', step='11'))
async def ok_day_1_step_11(call: types.CallbackQuery, user: User):
    await answer_file(
        message=call.message,
        file_key='day_1_step_11',
        caption="Ты молодец, что сделал шаг вперед - пока ничего сложного, правда же? За это я как и обещала, присылаю "
        "тебе гайд и на сегодня мы отдыхаем, до новых встреч завтра!",
    )
    if user.day_number == 1:
        user.is_waiting_next_day = True
        user.start_waiting_next_day_at = dt.now().timestamp()
        user.save()


@settings.dp.callback_query_handler(callbacks.ok_data().filter(day='2', step='4'))
async def ok_day_2_step_4(call: types.CallbackQuery, user: User):
    await call.message.answer("Сейчас проверим это 👩‍🎓 Напиши в одном сообщении свой главный инсайт и пользу после "
                              "просмотра этого видео")

    state = states.Form.waiting_inside
    await state.set()

    user.state = str(states.Form.waiting_inside)
    user.save()


@settings.dp.message_handler(state=states.Form.waiting_inside)
async def enter_inside(message: types.Message, user: User, state: FSMContext):
    await state.finish()

    user.state = None
    user.inside = message.text
    user.save()

    await message.answer(
        "Вот это да! Вижу, ты действительно внимательно смотрел, а значит, ты еще ближе на пути к поступлению! "
        "Ура!\nМы с тобой на одной волне!",
        reply_markup=callbacks.ok_kb(day=2, step=6)
    )


@settings.dp.callback_query_handler(callbacks.ok_data().filter(day='2', step='6'))
async def ok_day_2_step_6(call: types.CallbackQuery, user: User):
    await call.message.answer(
        "Ну что - готов к выполнению нового домашнего задания? Тогда напиши в одном сообщении 3 вещи, которые ты "
        "собираешься делать на пути к поступлению, и какую последовательность действий выбираешь?"
    )

    state = states.Form.waiting_three_things
    await state.set()

    user.state = str(states.Form.waiting_three_things)
    user.save()


@settings.dp.message_handler(state=states.Form.waiting_three_things)
async def enter_three_things(message: types.Message, user: User, state: FSMContext):
    await state.finish()

    user.state = None
    user.lesson_benefits = message.text
    user.save()

    await message.answer(
        "Вот это мощно! Ты большой молодец, твои старания видны невооруженным взглядом, завтра я пришлю тебе "
        "обратную связь. И знай, что я очень поддерживаю тебя!"
    )
    await answer_file(
        message=message,
        file_key='day_2_step_8',
        caption="А потому направляю следующее сокровище - гайд “как усилить личный бренд”",
    )
    await asyncio.sleep(60 * 10)
    await message.answer("Между прочим , лето - самое удачное время для того, чтобы усиливать свой личный бренд! "
                         "Это твой фундамент для поступления, который позволит сделать из тебя идеального кандидата, "
                         "даже если твои оценки далеки от идеала 🚀")
    await asyncio.sleep(60)
    await message.answer("Интересно узнать подробнее про процесс поступления и про усиления личного бренда? "
                         "Тогда приглашаю тебя в наш тг-канал, где я как раз поднимаю все эти темы и где ты найдешь "
                         "такое же заряженное окружение: https://t.me/+bAXZl02t3aAwODA6   💗 а все мы знаем, как "
                         "важна поддержка на этом пути, так что жду тебя, мой дорогой шпион! Ну и жду тебя завтра, "
                         "в этом же месте, в это же время!")

    if user.day_number == 2:
        user.is_waiting_next_day = True
        user.start_waiting_next_day_at = dt.now().timestamp()
        user.save()


@settings.dp.callback_query_handler(callbacks.yes_no_data().filter(action='yes', day='3', step='6'))
async def yes_day_3_step_6(call: types.CallbackQuery, user: User):
    await call.message.answer("Отлично! Ты сделал правильный выбор, у тебя впереди просто огромное будущее, я уже "
                              "это чувствую 🚀🚀🚀 ты сделал больше, чем бОльшая часть людей, кто тоже мечтает учиться "
                              "за границей, а значит, все преграды нипочем, верно?\n"
                              "Скоро с тобой свяжется моя команда, ожидай ✨")

    await call.message.answer("За твои честные старания и неподдельный интерес я отправляю тебе еще 2 наших "
                              "сокровища! И ты собираешь целую коллекцию!!\n"
                              "Мне даже страшно, от такого напора и скорости 🚀")

    await answer_file(
        message=call.message,
        file_key='day_3_step_6_1'
    )

    await answer_file(
        message=call.message,
        file_key='day_3_step_6_2'
    )

    user.is_agree_with_free_cons = True
    user.day_number = 3
    user.save()


@settings.dp.callback_query_handler(callbacks.yes_no_data().filter(action='no', day='3', step='6'))
async def no_day_3_step_6(call: types.CallbackQuery, user: User):
    await call.message.answer("Очень жаль, что ты не хочешь идти дальше :( Консультация ни к чему не обязывает, и ты "
                              "всегда можешь написать нам:  https://t.me/CAcademy_team Но несмотря на это, ты уже "
                              "прошел большой путь и стал моим напарником 😉 а значит, как и обещала, "
                              "ты достоин еще 2ух сокровищ 🔥")

    await call.message.answer("За твои честные старания и неподдельный интерес я отправляю тебе еще 2 наших "
                              "сокровища! И ты собираешь целую коллекцию!!\n"
                              "Мне даже страшно, от такого напора и скорости 🚀")

    await answer_file(
        message=call.message,
        file_key='day_3_step_6_1'
    )

    await answer_file(
        message=call.message,
        file_key='day_3_step_6_2'
    )

    user.day_number = 3
    user.save()


@settings.dp.message_handler(filters.IsAdminFilter(), commands=['run_schedule'])
async def run_schedule(message: types.Message):
    await message.answer('Начинаю запуск тасков')

    await services.day_2_hi_message()
    await services.day_2_lesson_message()
    await services.day_2_ask_message()

    await services.remember()

    await services.day_3_hi_message()
    await services.day_3_hi_message_2()
    await services.day_3_hi_message_3()

    await message.answer('Такси выполнены')
