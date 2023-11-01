from collections import namedtuple

from .SQLite import Sqlite3_Database


class Price:
    def __init__(self, id, **kwargs):
        self.id: int = id
        if len(kwargs):
            self.district: str | None = kwargs.get('district')
            self.count_user: int | None = kwargs.get('count_user')
            self.count_chat: int | None = kwargs.get('count_chat')
            self.price_publication: int | None = kwargs.get('price_publication')
            self.price_fixing: int | None = kwargs.get('price_fixing')
        else:
            self.district: str | None = None
            self.count_user: int | None = None
            self.count_chat: int | None = None
            self.price_publication: int | None = None
            self.price_fixing: int | None = None

    def __iter__(self):
        dict_class = self.__dict__
        Result = namedtuple("Result", ["name", "value"])
        for attr in dict_class:
            if not attr.startswith("__"):
                if attr != "flag":
                    yield Result(attr, dict_class[attr])
                else:
                    yield Result(attr, dict_class[attr].value)


class Prices(Sqlite3_Database):
    def __init__(self, db_file_name, table_name, *args) -> None:
        Sqlite3_Database.__init__(self, db_file_name, table_name, *args)
        self.len = len(self.get_keys())

    def add(self, obj: Price) -> None:
        self.add_row(obj)
        self.len += 1

    def __len__(self):
        return self.len

    def __delitem__(self, key):
        self.del_instance(key)
        self.len -= 1

    def __iter__(self) -> Price:
        keys = self.get_keys()
        for id in keys:
            obj = self.get(id)
            yield obj

    def get_price_publication(self, district: str):
        ans = self.get_by_other_field(district, "district", ["price_publication"])
        return ans[0][0]

    def get_price_fixing(self, district: str):
        ans = self.get_by_other_field(district, "district", ["price_fixing"])
        return ans[0][0]

    def get_prices_list(self):
        text = ""
        for price in self:
            text += (f'Район: {price.district} | Количество пользователей: {price.count_user} | '
                     f'Количество чатов: {price.count_chat} | Стоимость публикации: {price.price_publication} | '
                     f'Стоимость закрепления: {price.price_fixing}\n\n')
        return text

    def get(self, id: int) -> Price | bool:
        if id in self:
            obj_tuple = self.get_elem_sqllite3(id)
            obj = Price(id=obj_tuple[0],
                        district=obj_tuple[1],
                        count_user=obj_tuple[2],
                        count_chat=obj_tuple[3],
                        price_publication=obj_tuple[4],
                        price_fixing=obj_tuple[5],
                        )
            return obj
        return False
