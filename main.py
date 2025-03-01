from app.sqlite_worker import SQLiteWorker
from app.gui import get_gui


def main():
    worker = SQLiteWorker("db.sqlite3")
    worker.insert_data_from_json("data.json")


if __name__ == "__main__":
    main()
