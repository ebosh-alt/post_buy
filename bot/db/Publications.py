from collections import namedtuple

from .SQLite import Sqlite3_Database


class Publication:
    def __init__(self, id: int, **kwargs):
        self.id: int = id
        if len(kwargs):
            self.name_channel: str | None = kwargs.get('name_channel')
            self.id_user: int | None = kwargs.get('id_user')
            self.text: str | None = kwargs.get('text')
            self.price_publication: int | None = kwargs.get('price_publication')
            self.photo: str | None = kwargs.get('photo')
            self.video: str | None = kwargs.get('video')
            self.publication_time: str | None = kwargs.get('publication_time')
            self.fixing: bool | str = kwargs.get('fixing')
            self.message_id: int | None = kwargs.get('message_id')
        else:
            self.name_channel: str | None = None
            self.id_user: int | None = None
            self.text: str | None = None
            self.price_publication: int | None = None
            self.photo: str | None = None
            self.video: str | None = None
            self.publication_time: str | None = None
            self.fixing: bool | str = False
            self.message_id: int = 0

    def __iter__(self):
        dict_class = self.__dict__
        Result = namedtuple("Result", ["name", "value"])
        for attr in dict_class:
            if not attr.startswith("__"):
                if attr != "flag":
                    yield Result(attr, dict_class[attr])
                else:
                    yield Result(attr, dict_class[attr].value)


class Publications(Sqlite3_Database):
    def __init__(self, db_file_name, table_name, *args) -> None:
        Sqlite3_Database.__init__(self, db_file_name, table_name, *args)
        self.len = len(self.get_keys())

    def add(self, obj: Publication) -> None:
        self.add_row(obj)
        self.len += 1

    def __len__(self):
        return len(self.get_keys())

    def __delitem__(self, key):
        self.del_instance(key)
        self.len -= 1

    def __iter__(self) -> Publication:
        keys = self.get_keys()
        for id in keys:
            obj = self.get(id)
            yield obj

    def get_time_by_name(self, name, time):
        conn = self.sqlite_connect()
        curs = conn.cursor()
        curs.execute(
            f'''SELECT name_channel from {self.table_name} where name_channel = '{name}' and publication_time='{time}' ''')
        answer = curs.fetchone()
        conn.close()
        return answer

    def get_by_name(self, name) -> Publication:
        conn = self.sqlite_connect()
        curs = conn.cursor()
        curs.execute(
            f'''SELECT id from {self.table_name} where name_channel = '{name}' ''')
        answer = curs.fetchone()
        conn.close()

        return self.get(answer[0])

    def get(self, id: int) -> Publication | bool:
        if id in self:
            obj_tuple = self.get_elem_sqllite3(id)
            obj = Publication(id=obj_tuple[0],
                              name_channel=obj_tuple[1],
                              id_user=obj_tuple[2],
                              text=obj_tuple[3],
                              price_publication=obj_tuple[4],
                              photo=obj_tuple[5],
                              video=obj_tuple[6],
                              publication_time=obj_tuple[7],
                              fixing=obj_tuple[8],
                              message_id=obj_tuple[9],
                              )
            return obj
        return False
