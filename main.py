from app.sqlite_worker import SQLiteWorker
from app.gui import get_gui


def main():
    worker = SQLiteWorker(input("Enter db path (*.sqlite3):"))
    worker.insert_data_from_json(input("Enter .json file path:"))


if __name__ == "__main__":
    main()
