from collections import namedtuple

from ..SQLite import Sqlite3_Database


class Creative:
    def __init__(self, id, **kwargs):
        self.id: int = id
        if len(kwargs):
            self.contractId: str = kwargs.get("contractId")
            self.textData: str = kwargs.get("textData")
            self.description: str = kwargs.get("description")
            self.isSocial: bool = kwargs.get("isSocial")
        else:
            self.contractId: str = ""
            self.textData: str = ""
            self.description: str = ""
            self.isSocial: bool = True

    def __iter__(self):
        dict_class = self.__dict__
        Result = namedtuple("Result", ["name", "value"])
        for attr in dict_class:
            if not attr.startswith("__"):
                if attr != "flag":
                    yield Result(attr, dict_class[attr])
                else:
                    yield Result(attr, dict_class[attr].value)


class Creatives(Sqlite3_Database):
    def __init__(self, db_file_name, table_name, *args) -> None:
        Sqlite3_Database.__init__(self, db_file_name, table_name, *args)
        self.len = len(self.get_keys())

    def add(self, obj: Creative) -> None:
        self.add_row(obj)
        self.len += 1

    def __len__(self):
        return self.len

    def __delitem__(self, key):
        self.del_instance(key)
        self.len -= 1

    def __iter__(self) -> Creative:
        keys = self.get_keys()
        for id in keys:
            user = self.get(id)
            yield user

    def get(self, id: int) -> Creative | bool:
        if id in self:
            obj_tuple = self.get_elem_sqllite3(id)
            obj = Creative(id=obj_tuple[0],
                           contractId=obj_tuple[1],
                           textData=obj_tuple[2],
                           description=obj_tuple[3],
                           isSocial=obj_tuple[4],
                           )
            return obj
        return False
