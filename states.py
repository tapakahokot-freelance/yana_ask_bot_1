from aiogram.dispatcher.filters.state import State, StatesGroup


class Form(StatesGroup):
    waiting_inside = State()
    waiting_three_things = State()
