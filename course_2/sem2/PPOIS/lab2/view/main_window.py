import re
import tkinter as tk
from tkinter import ttk, BOTH, END, NW
from typing import Dict

from model.model import Student
from view.creation_window import CreationWindow


class MainWindow:

    def __create_drop_down_lists(self):
        """Выпадающие списки"""
        mainmenu = tk.Menu(self.main_window)
        self.main_window.config(menu=mainmenu)

        actions_menu = tk.Menu(self.main_window, tearoff=0)
        actions_menu.add_command(label="Фильтры")
        actions_menu.add_command(label="Добавить новую запись", command=CreationWindow)
        actions_menu.add_command(label="Удалить отфильтрованные записи")

        file_menu = tk.Menu(self.main_window)
        file_menu.add_command(label="открыть...")
        file_menu.add_command(label="сохранить")
        file_menu.add_command(label="сохранить как...")
        file_menu.add_separator()
        file_menu.add_command(label="Выход")

        mainmenu.add_cascade(label="Файл", menu=file_menu)
        mainmenu.add_cascade(label="Действия", menu=actions_menu)

    def __create_tables(self):
        """Таблица"""
        columns = (
            'id', 'stud_name', 'group', 'sem_1', 'sem_2', 'sem_3', 'sem_4', 'sem_5', 'sem_6', 'sem_7', 'sem_8', 'sem_9',
            'sem_10',)
        self.main_table = ttk.Treeview(columns=columns, show='headings')
        self.main_table.pack(fill=BOTH, expand=1)

        self.main_table.heading('id', text="Номер")
        self.main_table.column(f'id', width=10)
        self.main_table.heading('stud_name', text="ФИО студента")
        self.main_table.column(f'stud_name', width=60)
        self.main_table.heading('group', text="Группа")
        self.main_table.column(f'group', width=10)

        for i in range(1, 11):
            self.main_table.column(f'sem_{i}', width=30)
            self.main_table.heading(f'sem_{i}', text=f"Семестр {i}")

        # """Встроенная таблица семестров"""
        # community_services_column = [f'{i + 1}_sem' for i in range(10)]
        # self.__community_services = ttk.Treeview(self.main_table, columns=community_services_column,
        #                                          show='headings')
        # self.__community_services.pack(fill=BOTH, expand=1)
        # for i in range(10):
        #     self.__community_services.heading(f'{i + 1}_sem', text=f'{i + 1} Семестр')

    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.title("student community service")
        self.main_window.geometry("1200x500")

        # табличка
        self.__create_tables()

        # выпадающие менюшки
        self.__create_drop_down_lists()
        tk.Button(self.main_window, text="Обновить данные таблицы", command=self.__build_table).pack()

    def __build_table(self):
        studs = [(1, "Vlad", 121701, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
                 (2, "Vlad2", 121701, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1), ]

        all_entries: Dict[str: Student] = Student.get_all_students()
        print(f'Все списки: {all_entries}')
        studs = []
        for i in all_entries.values():
            studs.append((i.id, i.student_name, i.student_group, *i.community_service.values()))

        print(studs)
        self.main_table.delete(*self.main_table.get_children())

        for stud in studs:
            self.main_table.insert("", END, values=stud)

    def run_table(self):
        # self.__build_table()
        self.main_window.mainloop()
