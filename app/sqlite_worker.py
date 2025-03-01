import sqlite3
import json


class SQLiteWorker:
    def connect(self, db_name: str):
        try:
            self.connection = sqlite3.connect(db_name)
        except sqlite3.OperationalError as e:
            print(f"Failed to connect to database {db_name}", e)

    def __init__(self, db_name: str):
        self.connect(db_name)

    def close(self):
        if self.connection:
            self.connection.close()

    def insert_data_from_sql(self, file_name, encoding="UTF-8", format="dbeaver"):
        with open(file_name, encoding=encoding) as f:
            raw_sql = f.read()
            if format == "dbeaver":
                try:
                    self.connection.execute(raw_sql)
                    self.connection.commit()
                except sqlite3.OperationalError as e:
                    print(f"Failed to execute sql query from file {file_name}", e)

    def insert_data_from_json(self, file_name, encoding="UTF-8", format="dbeaver"):
        def get_raw_sql_from_json_object(json_model_name, json_model):
            """
            JSON object must suit the following format:
            [
                {
                    "object_property_1": "object_property_1_value",
                    "object_property_2": "object_property_2_value",
                },
            ]
            """
            if not len(json_model):
                return
            keys = json_model[0].keys()
            raw_sql = f"INSERT INTO {json_model_name} ({",".join([key for key in keys])}) VALUES ({",".join(["?" for key in keys])});"
            return raw_sql

        type_map = {
            int: "INTEGER",
            float: "REAL",
            str: "TEXT",
            bool: "INTEGER",  # SQLite uses 0/1 for booleans
            dict: "TEXT"       # Store nested JSON as a string
        }

        with open(file_name, encoding=encoding) as f:
            json_object = json.loads(f.read())
            if format == "dbeaver":
                for model, value in json_object.items():
                    self.connection.execute(f"CREATE TABLE IF NOT EXISTS {model} ({",".join([key + " " + type_map[type(value[0][key])] for key in value[0].keys()])});")
                    self.connection.executemany(get_raw_sql_from_json_object(model, value), [list(v.values()) for v in value])
                self.connection.commit()

