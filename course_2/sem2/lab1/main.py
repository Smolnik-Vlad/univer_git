from another_operations import Another_operations
from constants import Constants
from sets_and_operations import Sets_and_operations
import argparse


class Read_a_line:

    @staticmethod
    def validate_line(raw_line):
        if raw_line.count('(') != raw_line.count(')') or raw_line.count('{') != raw_line.count('}'):
            raise ValueError('Invalid expression: The number of brackets is not the same')

    @staticmethod
    def read_raw_line(raw_line: str):
        raw_line = raw_line.replace(' ', '')
        try:
            Read_a_line.validate_line(raw_line)

            if raw_line.find('size') != -1 or raw_line.find('psp') != -1 or raw_line.find('[') != -1:
                print(Another_operations().read_the_line_with_another_operatios(raw_line))

            elif not raw_line.islower() and (raw_line[0].isalpha() or raw_line[0]=='{' or raw_line[0]=='('):
                Constants().read_line(raw_line)

            elif raw_line[0] == '(' or raw_line[0] == '{':
                Sets_and_operations.check(raw_line)

            else:
                raise ValueError('Invalid expression')
        except Exception as e:
            if str(e) == 'list index out of range':
                print('Unknown error! The expression is incorrect!')
            else:
                print(e)


# a = Sets_and_operations()
# b = Sets_and_operations()
# #b.check(s='a, b') #сюда передается множество без внешних скобок
# a.check(s="({a, {c, d}, b} + {a, {c, d}}) - ({b, d, {d, c}} * {{c, d}})")

# a = Constants()
# try:
#     print(a.read_line("psp(F)"))
# except ValueError as a:
#     print(a)

# a = Another_operations()
# res = a.read_the_line('D[4]', value='[')
# print(res.output_a_set(first_enter=True))

parser = argparse.ArgumentParser()
parser.add_argument('--set', type=str, help='combinations of sets')
args = parser.parse_args()
Read_a_line.read_raw_line(args.set)

# Read_a_line.read_raw_line('A = {a, b}')
