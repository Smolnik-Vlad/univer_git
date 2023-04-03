import tkinter as tk
from tkinter import ttk, E
import tkinter.messagebox as mb


from models.models import Student


class FilteringWindow:

    def __create_filter_fields(self):
        # накинуть валидации
        self.__filter_entries = []
        tk.Label(self.filtering_window, text=f'Фильтрация по ФИО').grid(row=0, column=0, sticky=E)
        a = tk.Entry(self.filtering_window, )
        a.grid(row=0, column=1)
        self.__filter_entries.append(a)

        tk.Label(self.filtering_window, text=f'Фильтрация по номеру группы').grid(row=1, column=0, sticky=E)
        groups = Student.list_of_groups
        combo = ttk.Combobox(self.filtering_window, values=groups)
        combo.set("none")
        combo.config(width=19)
        combo.grid(row=1, column=1)
        self.__filter_entries.append(combo)

        tk.Label(self.filtering_window, text=f'Общественная работа (нижний предел)').grid(row=2, column=0, sticky=E)
        upper_limit = tk.Entry(self.filtering_window, )
        upper_limit.grid(row=2, column=1)
        self.__filter_entries.append(upper_limit)

        tk.Label(self.filtering_window, text=f'Общественная работа (верхний предел)').grid(row=3, column=0, sticky=E)

        lower_limit = tk.Entry(self.filtering_window, )
        lower_limit.grid(row=3, column=1)
        self.__filter_entries.append(lower_limit)

    def __save_filters(self):
        fields_results = list(map(lambda x: x.get(), self.__filter_entries))  # список из данных полей
        names = ['student_name', 'student_group', 'low_limit', 'high_limit']
        named_parametrs = dict(zip(names, fields_results))
        try:
            Student.set_up_filters(named_parametrs)
        except ValueError as e:
            mb.showwarning("Предупреждение", e)





    def __init__(self):
        self.filtering_window = tk.Tk()
        self.filtering_window.title = 'filtering window'
        self.filtering_window.geometry('470x120')

        self.__create_filter_fields()
        tk.Button(self.filtering_window, text='Задать фильтры', command=self.__save_filters).grid(row=4, column=1)
        self.filtering_window.mainloop()


