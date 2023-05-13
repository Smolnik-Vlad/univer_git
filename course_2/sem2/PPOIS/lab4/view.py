import tkinter as tk
from tkinter import messagebox as mb

from main import Read_a_Line


class MainWindow:
    def __solution(self):
        try:
            result = Read_a_Line.read_raw_line(self.entry_place.get(), my_module=True)

            if result:
                self.text.insert('end', f"{result}\n")
            else:
                self.text.insert('end', f"Добавлена новая переменная!\n")
        except Exception as e:
            mb.showerror("Exception", e)

    def __init__(self, ):
        self.__main_window = tk.Tk()
        self.__main_window.title("Калькулятор множеств")
        self.__main_window.geometry("400x270")
        self.entry_place = tk.Entry(self.__main_window)
        self.entry_place.pack()
        self.button = tk.Button(self.__main_window, text='Подсчитать', command=self.__solution)
        self.button.pack()
        self.text = tk.Text(self.__main_window)
        self.text.pack()
        self.__main_window.mainloop()


MainWindow()
