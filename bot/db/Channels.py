import logging
from collections import namedtuple

from .SQLite import Sqlite3_Database


class Channel:
    def __init__(self, id, **kwargs):
        self.id: int = id
        if len(kwargs):
            self.id_telegram: int | None = kwargs.get("id_telegram")
            # self.city: str | None = kwargs.get("city")
            self.district: str | None = kwargs.get("district")
            self.name: str | None = kwargs.get("name")
        else:
            self.id_telegram: int | None = None
            # self.name: str | None = None
            self.district: str | None = None
            self.name: str | None = None

    def __iter__(self):
        dict_class = self.__dict__
        Result = namedtuple("Result", ["name", "value"])
        for attr in dict_class:
            if not attr.startswith("__"):
                if attr != "flag":
                    yield Result(attr, dict_class[attr])
                else:
                    yield Result(attr, dict_class[attr].value)


class Channels(Sqlite3_Database):
    def __init__(self, db_file_name, table_name, *args) -> None:
        Sqlite3_Database.__init__(self, db_file_name, table_name, *args)
        self.len = len(self.get_keys())

    def add(self, obj: Channel) -> None:
        self.add_row(obj)
        self.len += 1

    def __len__(self):
        return self.len

    def __delitem__(self, key):
        self.del_instance(key)
        self.len -= 1

    def __iter__(self) -> Channel:
        keys = self.get_keys()
        for id in keys:
            obj = self.get(id)
            yield obj

    def get_name(self, district):
        conn = self.sqlite_connect()
        curs = conn.cursor()
        curs.execute(f'''SELECT name from {self.table_name} where district = '{district}' ''')
        answer = curs.fetchall()
        conn.close()
        name_channel = dict()
        for name in answer:
            name_channel.update({name[0]: name[0]})
        return name_channel

    def get_all_name(self):
        all_name = self.get_attribute("name")
        ind = all_name.index("Доска объявлений")
        del all_name[ind]
        return all_name

    def get_id_by_name(self, name):
        ans = self.get_by_other_field(name, "name", ["id_telegram"])
        return ans[0][0]

    def get_channel_category(self, category: str):
        ans = self.get_by_other_field(category, "district", ["name"])
        return ans

    def get_category(self):
        all_category = {}
        for channel in self:
            match channel.district:
                case "Весь город":
                    category = "Весь город"
                case "Доска объявлений":
                    category = "Доска объявлений"
                case _:
                    category = channel.district
            if category not in all_category.keys():
                all_category.update({category: category})
        all_category.update({"Весь город": "Весь город"})
        all_category.update({"1 любой чат": "1 любой чат"})
        # all_category.update({"Вернуться в начало": "buy_advertisement"})
        return all_category

    def get_all_district(self):
        ans = self.get_attribute("district")
        return ans

    def get(self, id: int) -> Channel | bool:
        if id in self:
            obj_tuple = self.get_elem_sqllite3(id)
            obj = Channel(id=obj_tuple[0],
                          id_telegram=obj_tuple[1],
                          district=obj_tuple[2],
                          name=obj_tuple[3])
            return obj
        return False


def insert():
    with open("./bot/db/chats.csv", "r", encoding="windows-1251") as f:
        data = f.read()
    data = data.split("\n")
    for line in data:
        if len(line) > 0:
            line = line.split(";")
            id = line[0]
            id_telegram = line[5]
            district = line[1]
            name = line[2]
            if id_telegram != '' and id != "№ п/п":
                channels = Channels(db_file_name="bot/db/database", table_name="channel")
                channels.add(Channel(id=int(id), id_telegram=int(id_telegram), name=name, district=district))


if __name__ == "__main__":
    print(insert())
