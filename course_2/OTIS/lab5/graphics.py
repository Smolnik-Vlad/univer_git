from tkinter import *
from tkinter import messagebox
from node_and_edge import Node

class Methods:
    @staticmethod
    def return_name():
        pass
        #return name_of_node.get()

class Graphics(Methods):
    def __init__(self):
        self.window = Tk()
        self.window.title("Граф предпостений для абстрактных сущностей")
        self.window.geometry('600x600')
        self.nodes={}

    def process(self):
        self.window.bind('<Double-Button-1>', Graphics.__evente_create_node)
        self.window.mainloop()

    @staticmethod
    def __evente_create_node(event):
        coord=[event.x_root, event.y_root]
        print(coord)
        #new_node=Graphics.__create_node(coord)

    @staticmethod
    def __create_node(coord):
        name = Graphics.__insert()
        pass

    @staticmethod
    def __insert():
        ins=Tk()
        name_of_node = Entry(width=50)
        button_for_enter=Button(text="Задать имя", command=Methods.return_name)


