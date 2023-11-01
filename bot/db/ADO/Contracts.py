from collections import namedtuple

from ..SQLite import Sqlite3_Database


class Contract:
    def __init__(self, id, **kwargs):
        self.id: int = id
        if len(kwargs):
            self.clientId: str = kwargs.get("clientId")
            self.contractorId: str = kwargs.get("contractorId")
            self.isRegReport: bool = kwargs.get("isRegReport")
            self.date: str = kwargs.get("date")
            self.amount: float = kwargs.get("amount")
            self.isVat: bool = kwargs.get("amount")

        else:
            self.clientId: str = ""
            self.contractorId: str = ""
            self.isRegReport: bool = True
            self.date: str = ""
            self.amount: float = 0.0
            self.isVat: bool = False

    def __iter__(self):
        dict_class = self.__dict__
        Result = namedtuple("Result", ["name", "value"])
        for attr in dict_class:
            if not attr.startswith("__"):
                if attr != "flag":
                    yield Result(attr, dict_class[attr])
                else:
                    yield Result(attr, dict_class[attr].value)


class Contracts(Sqlite3_Database):
    def __init__(self, db_file_name, table_name, *args) -> None:
        Sqlite3_Database.__init__(self, db_file_name, table_name, *args)
        self.len = len(self.get_keys())

    def add(self, obj: Contract) -> None:
        self.add_row(obj)
        self.len += 1

    def __len__(self):
        return self.len

    def __delitem__(self, key):
        self.del_instance(key)
        self.len -= 1

    def __iter__(self) -> Contract:
        keys = self.get_keys()
        for id in keys:
            user = self.get(id)
            yield user

    def get(self, id: int) -> Contract | bool:
        if id in self:
            obj_tuple = self.get_elem_sqllite3(id)
            obj = Contract(id=obj_tuple[0],
                           clientId=obj_tuple[1],
                           contractorId=obj_tuple[2],
                           isRegReport=obj_tuple[3],
                           date=obj_tuple[4],
                           amount=obj_tuple[5],
                           isVat=obj_tuple[6],
                           )
            return obj
        return False
