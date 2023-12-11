from sqlite3 import connect

class Database:

    base_path = __file__.replace("main.py", "db.db")

    def __init__(self, table: str, _db_path=None):
        self._table = table
        self.db_path = _db_path if _db_path else self.base_path

    def insert(self, insert_pairs: dict):
        columns = ("".join(i + "," for i in insert_pairs))[:-1]
        qw = ("".join("?," for _ in insert_pairs))[:-1]
        values = [insert_pairs[i] for i in insert_pairs]
        connection = connect(self.db_path, check_same_thread=False)
        cursor = connection.cursor()
        cursor.execute(f"INSERT INTO {self._table}({columns}) values({qw})", values)
        connection.commit()
        connection.close()

    def get(self, get_means: list, search_pair: list, *args):
        if len(args) == 0:
            get_means = ("".join(i + "," for i in get_means))[:-1]
            connection = connect(self.db_path, check_same_thread=False)
            cursor = connection.cursor()
            _result = cursor.execute(f"""SELECT {get_means} FROM {self._table} WHERE {search_pair[0]}=?""", (search_pair[1],)).fetchall()
            connection.commit()
            connection.close()
        else:
            get_means = ("".join(i + "," for i in get_means))[:-1]
            search_pairs = [search_pair]
            search_pairs.extend([i for i in args])
            search_params = "".join(i[0]+"=? AND " for i in search_pairs)[:-4]
            search_means = [i[1] for i in search_pairs]
            connection = connect(self.db_path, check_same_thread=False)
            cursor = connection.cursor()
            _result = cursor.execute(f"""SELECT {get_means} FROM {self._table} WHERE {search_params}""",
                                     search_means).fetchall()
            connection.commit()
            connection.close()
        return _result

    def get_all(self):
        connection = connect(self.db_path, check_same_thread=False)
        cursor = connection.cursor()
        _result = cursor.execute(f"""SELECT * FROM {self._table}""").fetchall()
        connection.commit()
        connection.close()
        return _result

    def set(self, set_pair:list, search_pair: list, *args):
        if len(args) == 0:
            connection = connect(self.db_path, check_same_thread=False)
            cursor = connection.cursor()
            cursor.execute(f"""UPDATE {self._table} SET {set_pair[0]}=? WHERE {search_pair[0]}=?""",
                          (set_pair[1], search_pair[1]))
            connection.commit()
            connection.close()
        else:
            search_pairs = [search_pair]
            search_pairs.extend([i for i in args])
            search_params = "".join(i[0]+"=? AND " for i in search_pairs)[:-4]
            search_means = [i[1] for i in search_pairs]
            connection = connect(self.db_path, check_same_thread=False)
            cursor = connection.cursor()
            params = [set_pair[1]]
            params.extend(search_means)
            _result = cursor.execute(f"""UPDATE {self._table} SET {set_pair[0]}=? WHERE {search_params}""", params)
            connection.commit()
            connection.close()


    def create_table(self, creation_pairs: dict):
        columns = ("".join(f"{i} {creation_pairs[i]}," for i in creation_pairs))[:-1]
        connection = connect(self.db_path, check_same_thread=False)
        cursor = connection.cursor()
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {self._table}({columns})")
        connection.commit()
        connection.close()
        return self

    def delete(self, search_pair: list):
        connection = connect(self.db_path, check_same_thread=False)
        cursor = connection.cursor()
        cursor.execute(f"""DELETE FROM {self._table} WHERE {search_pair[0]}=?""", (search_pair[1],))
        connection.commit()
        connection.close()