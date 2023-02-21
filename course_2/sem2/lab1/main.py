from sets_and_operations import Sets_and_operations


class Read_a_line:

    def read_line(self):
        while True:
            raw_line = input("Enter a line of sets and operations: ")


a = Sets_and_operations()
b = Sets_and_operations()
#b.check(s='a, b') #сюда передается множество без внешних скобок
a.check(s="{a, b} + {c} + (({a} + {b})+{d, {e, f}}) + ({a} + {b, c}) + ({a, b}-({a, {b, c}} + {d}))")


