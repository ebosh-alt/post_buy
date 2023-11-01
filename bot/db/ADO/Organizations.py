from collections import namedtuple

from ..SQLite import Sqlite3_Database


class Organization:
    def __init__(self, id, **kwargs):
        self.id: int = id
        if len(kwargs):
            self.type: bool = kwargs.get('type')
            self.isOrs: bool = kwargs.get('isOrs')
            self.isRr: bool = kwargs.get('isRr')
            self.inn: str = kwargs.get('inn')
            self.name: str = kwargs.get('name')
            self.platforms: list = kwargs.get('platforms')
        else:
            self.type: bool = False
            self.isOrs: bool = False
            self.isRr: bool = False
            self.inn: str = ""
            self.name: str = ""
            self.name: str = ""
            self.platforms: list = list()

    def __iter__(self):
        dict_class = self.__dict__
        Result = namedtuple("Result", ["name", "value"])
        for attr in dict_class:
            if not attr.startswith("__"):
                if attr != "flag":
                    yield Result(attr, dict_class[attr])
                else:
                    yield Result(attr, dict_class[attr].value)


class Organizations(Sqlite3_Database):
    def __init__(self, db_file_name, table_name, *args) -> None:
        Sqlite3_Database.__init__(self, db_file_name, table_name, *args)
        self.len = len(self.get_keys())

    def add(self, obj: Organization) -> None:
        self.add_row(obj)
        self.len += 1

    def __len__(self):
        return self.len

    def __delitem__(self, key):
        self.del_instance(key)
        self.len -= 1

    def __iter__(self) -> Organization:
        keys = self.get_keys()
        for id in keys:
            user = self.get(id)
            yield user

    def get(self, id: int) -> Organization | bool:
        if id in self:
            obj_tuple = self.get_elem_sqllite3(id)
            obj = Organization(id=obj_tuple[0],
                               isOrs=obj_tuple[1],
                               isRr=obj_tuple[2],
                               inn=obj_tuple[3],
                               name=obj_tuple[4],
                               platforms=obj_tuple[5],
                               )
            return obj
        return False
