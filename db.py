import json
import os
import pandas as pd
import numpy as np
from dataclasses import dataclass

base_dir = os.path.dirname(os.path.abspath(__file__))


@dataclass
class DB:
    users: dict[str: 'User'] = None
    users_file: str = base_dir + '/users.json'

    def load_data(self, json_file):
        if os.path.exists(json_file):
            with open(json_file, 'r') as file:
                return json.load(file)
        return {}

    def save_data(self, json_file, data):
        with open(json_file, 'w') as file:
            json.dump(data, file)

    def load_users(self):
        self.users = self.load_data(self.users_file)

    def save_users(self):
        self.save_data(self.users_file, self.users)

    def __post_init__(self):
        self.load_users()


db = DB()


@dataclass
class User:
    chat_id: int
    day_number: int = 1
    is_waiting_next_day: bool = False
    start_waiting_next_day_at: int = 0
    state: str = None
    phone_number: str = None
    inside: str = None
    lesson_benefits: str = None
    is_agree_with_free_cons: bool | None = None
    username: str = None

    @staticmethod
    def get_or_create(chat_id: int, **kwargs):
        if str(chat_id) in db.users:
            return User(**db.users[str(chat_id)])

        user = User(chat_id, **kwargs)
        user.save()

        return user

    @staticmethod
    def get_all():
        return [User(**u) for u in db.users.values()]

    def save(self):
        db.users[str(self.chat_id)] = self.__dict__
        db.save_users()

    @staticmethod
    def generate_excel():
        df = pd.read_json(db.users_file, orient='index').reset_index(drop=True)
        df = df.drop('state', axis=1).drop('is_waiting_next_day', axis=1).\
            drop('start_waiting_next_day_at', axis=1).drop('day_number', axis=1)

        all_users_count = len(df)
        agreed_users_count = len(df[df['is_agree_with_free_cons'] == True])

        def make_hyperlink(row):
            if 'username' in row and str(row['username']) != 'nan':
                return f'https://telegram.me/{row["username"]}'
            return f'tg://user?id={row["chat_id"]}'

        df['link'] = df.apply(make_hyperlink, axis=1)
        df.rename(
            columns={
                'phone_number': 'Номер телефона',
                'inside': 'Инсайт',
                'lesson_benefits': 'Польза от уроков',
                'is_agree_with_free_cons': 'Согласен на консультацию',
                'link': 'Ссылка'
            },
            inplace=True
        )
        df.to_excel(base_dir + '/files/users_info.xlsx')

        return all_users_count, agreed_users_count
