from collections import namedtuple

from ..SQLite import Sqlite3_Database


class Platform:
    def __init__(self, id, **kwargs):
        self.id: int = id
        if len(kwargs):
            self.organizationId: str = kwargs.get("organizationId")
            self.isOwned: bool = kwargs.get("isOwned")
            self.type: str = kwargs.get("type")
            self.name: str = kwargs.get("name")
            self.url: str = kwargs.get("url")
        else:
            self.organizationId: str = ""
            self.isOwned: bool = False
            self.type: str = "apps"
            self.name: str = "Telegram"
            self.url: str = "https://web.telegram.org/"

    def __iter__(self):
        dict_class = self.__dict__
        Result = namedtuple("Result", ["name", "value"])
        for attr in dict_class:
            if not attr.startswith("__"):
                if attr != "flag":
                    yield Result(attr, dict_class[attr])
                else:
                    yield Result(attr, dict_class[attr].value)


class Platforms(Sqlite3_Database):
    def __init__(self, db_file_name, table_name, *args) -> None:
        Sqlite3_Database.__init__(self, db_file_name, table_name, *args)
        self.len = len(self.get_keys())

    def add(self, obj: Platform) -> None:
        self.add_row(obj)
        self.len += 1

    def __len__(self):
        return self.len

    def __delitem__(self, key):
        self.del_instance(key)
        self.len -= 1

    def __iter__(self) -> Platform:
        keys = self.get_keys()
        for id in keys:
            user = self.get(id)
            yield user

    def get(self, id: int) -> Platform | bool:
        if id in self:
            obj_tuple = self.get_elem_sqllite3(id)
            obj = Platform(id=obj_tuple[0],
                           organizationId=obj_tuple[1],
                           isOwned=obj_tuple[2],
                           type=obj_tuple[3],
                           name=obj_tuple[4],
                           url=obj_tuple[5],
                           )
            return obj
        return False
