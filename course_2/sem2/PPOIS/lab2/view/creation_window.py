import tkinter as tk
import tkinter.messagebox as mb

from model.model import Student


class CreationWindow:

    def __create_entries_fields(self):
        # накинуть валидации
        self.entries = []
        tk.Label(self.creation_window, text=f'ФИО студента').grid(row=0, column=0)
        a = tk.Entry(self.creation_window, )
        a.grid(row=0, column=1)
        self.entries.append(a)
        tk.Label(self.creation_window, text=f'Номер группы').grid(row=1, column=0)
        a = tk.Entry(self.creation_window)
        a.grid(row=1, column=1)
        self.entries.append(a)
        for i in range(10):
            tk.Label(self.creation_window, text=f'Работа за {i + 1} семестр').grid(row=2 + i, column=0)
            a = tk.Entry(self.creation_window)
            a.grid(row=2 + i, column=1)
            self.entries.append(a)

    def save_entry(self):
        dict_of_services = {i + 1: self.entries[i + 2].get() for i in range(10)}
        new_entry = {'student_name': self.entries[0].get(), 'student_group': self.entries[1].get(),
                     'community_service': dict_of_services}
        try:
            Student.create_new_student(new_entry)
        except ValueError as er:
            mb.showwarning("Предупреждение", er)

    def __init__(self):
        self.creation_window = tk.Tk()
        self.creation_window.title = 'creation window'
        self.creation_window.geometry('370x310')

        self.__create_entries_fields()

        tk.Button(self.creation_window, text='Создать новую запись', command=self.save_entry).grid(row=13, column=1)
        self.creation_window.mainloop()
