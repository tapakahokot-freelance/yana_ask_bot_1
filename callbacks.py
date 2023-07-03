from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData


def base_data(name, *args) -> CallbackData:
    return CallbackData(name, *args)


def base_kb(btns: [[{}]], data) -> InlineKeyboardMarkup:
    inline = InlineKeyboardMarkup()
    for row in btns:
        inline_row = []
        for btn in row:
            if 'callback_data' in btn:
                btn['callback_data'] = data.new(**btn['callback_data'])
            inline_row.append(InlineKeyboardButton(**btn))
        inline.row(*inline_row)
    return inline


def ok_data() -> CallbackData:
    return base_data('ok', 'day', 'step')


def ok_kb(day, step):
    return base_kb(
        [[{'text': '✅', 'callback_data': {'day': str(day), 'step': str(step)}}]],
        ok_data()
    )


def yes_no_data() -> CallbackData:
    return base_data('yes_no', 'action', 'day', 'step')


def yes_no_kb(day, step):
    return base_kb(
        [[
            {'text': '✅', 'callback_data': {'action': 'yes', 'day': str(day), 'step': str(step)}},
            {'text': '❌', 'callback_data': {'action': 'no', 'day': str(day), 'step': str(step)}},
        ]],
        yes_no_data()
    )


def link_data() -> CallbackData:
    return base_data('link')


def link_kb(text, url):
    return base_kb(
        [[{'text': text, 'url': url}]],
        link_data()
    )
