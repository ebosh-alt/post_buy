from collections import namedtuple

from ..SQLite import Sqlite3_Database


class Invoice:
    def __init__(self, id, **kwargs):
        self.id: int = id
        if len(kwargs):
            self.contractId: str = kwargs.get("contractId")
            self.clientRole: str = kwargs.get("clientRole")
            self.contractorRole: str = kwargs.get("contractorRole")
            self.date: str = kwargs.get("date")
            self.startDate: str = kwargs.get("startDate")
            self.endDate: str = kwargs.get("endDate")
            self.isVat: bool = kwargs.get("isVat")
            self.number: str = kwargs.get("number")
        else:
            self.contractId: str = ""
            self.clientRole = "rd"
            self.contractorRole = "rr"
            self.date: str = ""
            self.startDate: str = ""
            self.endDate: str = ""
            self.isVat: bool = False
            self.number: str = ""

    def __iter__(self):
        dict_class = self.__dict__
        Result = namedtuple("Result", ["name", "value"])
        for attr in dict_class:
            if not attr.startswith("__"):
                if attr != "flag":
                    yield Result(attr, dict_class[attr])
                else:
                    yield Result(attr, dict_class[attr].value)


class Invoices(Sqlite3_Database):
    def __init__(self, db_file_name, table_name, *args) -> None:
        Sqlite3_Database.__init__(self, db_file_name, table_name, *args)
        self.len = len(self.get_keys())

    def add(self, obj: Invoice) -> None:
        self.add_row(obj)
        self.len += 1

    def __len__(self):
        return self.len

    def __delitem__(self, key):
        self.del_instance(key)
        self.len -= 1

    def __iter__(self) -> Invoice:
        keys = self.get_keys()
        for id in keys:
            user = self.get(id)
            yield user

    def get(self, id: int) -> Invoice | bool:
        if id in self:
            obj_tuple = self.get_elem_sqllite3(id)
            obj = Invoice(id=obj_tuple[0],
                          contractId=obj_tuple[1],
                          clientRole=obj_tuple[2],
                          contractorRole=obj_tuple[4],
                          date=obj_tuple[4],
                          startDate=obj_tuple[5],
                          endDate=obj_tuple[6],
                          isVat=obj_tuple[7],
                          number=obj_tuple[8]
                          )
            return obj
        return False
