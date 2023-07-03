import json
import os
from dataclasses import dataclass


@dataclass
class DB:
    users: dict[str: 'User'] = None
    users_file: str = 'users.json'

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
    state: str = None

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
