import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from .sqlite_worker import SQLiteWorker


class FileSelectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File and Folder Selector")
        
        # Переменные для хранения путей
        self.folder_path = tk.StringVar()
        self.db_name = tk.StringVar()
        self.file_path = tk.StringVar()
        
        # Создание элементов интерфейса
        self.create_widgets()
    
    def create_widgets(self):
        # Фрейм для выбора папки
        folder_frame = ttk.Frame(self.root, padding="10")
        folder_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        ttk.Label(folder_frame, text="Выберите папку:").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(folder_frame, textvariable=self.folder_path, width=50).grid(row=0, column=1, padx=5)
        ttk.Button(folder_frame, text="Обзор...", command=self.select_folder).grid(row=0, column=2)
        
        db_name_frame = ttk.Frame(self.root, padding="10")
        db_name_frame.grid(row=1, column=0, sticky=(tk.W, tk.E))

        ttk.Label(db_name_frame, text="Введите имя базы данных:").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(db_name_frame, textvariable=self.db_name, width=50).grid(row=0, column=1, padx=5)
        # Фрейм для выбора файла
        file_frame = ttk.Frame(self.root, padding="10")
        file_frame.grid(row=2, column=0, sticky=(tk.W, tk.E))
        
        ttk.Label(file_frame, text="Выберите файл:").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(file_frame, textvariable=self.file_path, width=50).grid(row=0, column=1, padx=5)
        ttk.Button(file_frame, text="Обзор...", command=self.select_file).grid(row=0, column=2)
        
        # Кнопка выполнения
        ttk.Button(self.root, text="Выполнить", command=self.process).grid(row=3, column=0, pady=10)
        
        # Настройка отступов
        for child in self.root.winfo_children():
            child.grid_configure(padx=10, pady=5)
    
    def select_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.folder_path.set(folder_selected)
    
    def select_file(self):
        file_selected = filedialog.askopenfilename()
        if file_selected:
            self.file_path.set(file_selected)
    
    def process(self):
        folder = self.folder_path.get()
        file = self.file_path.get()
        
        if not folder and not file:
            messagebox.showwarning("Предупреждение", "Выберите папку, имя базы данных и файл!")
            return
        worker = SQLiteWorker(folder + "/" + self.db_name.get().strip(".sqlite3")+".sqlite3")
        worker.insert_data_from_json(file)
        # Здесь можно добавить свою логику обработки
        messagebox.showinfo("Информация", 
                          f"Выбрана папка: {folder}\nВыбран файл: {file}\n\nОбработка выполнена!")

def get_gui():
    root = tk.Tk()
    app = FileSelectorApp(root)
    root.mainloop()