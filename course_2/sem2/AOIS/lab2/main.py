table = [[0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 1, 1], [1, 0, 0],  [1, 0, 1], [1, 1, 0], [1, 1, 1]]
operations_priority = {'!': 6, '*': 5, '+': 4, '~': 3, '->': 2, }


def decode_formula(current_formula: str) -> list:
    """
    Позволяет собрать "- >" в один элемент списка и так же делает переменные x123 как один элемент списка
    """
    arr = list(current_formula)
    i = 0
    while i < len(arr):
        if arr[i] == '-' and arr[i + 1] == '>':
            arr[i] = '->'
            arr.pop(i + 1)
        j = i + 1
        tmp = ''
        while j < len(arr) and arr[j].isdigit():
            tmp += arr[j]
            j += 1

        if arr[i] not in ('(', '!', '*', '+'):
            arr[i] += tmp
            arr[i + 1:i + 1 + len(tmp)] = []
        i += 1
    return arr


def binary_operation(variables, sign):
    a = variables.pop()
    b = variables.pop()

    if sign == '*':
        # return conjunction(a, b)
        return int(a) and int(b)
    elif sign == '+':
        # return disjunction(a, b)
        return int(a) or int(b)
    elif sign == '->':
        # return implication(b, a)
        return 0 if (int(b) and not int(a)) else 1
    elif sign == '~':
        # return equivalence(a, b)
        return int(a) == int(b)


def binary_operation_with_inversion(variables, sign):
    """Функция на проверку отрицания"""
    if sign == '!':
        return int(not int(variables.pop()))
    else:
        return int(binary_operation(variables, sign))


def binary_calculating(formula, variables, signs):
    stack_variables = []
    stack_signs = []
    for element in formula:
        if element in variables:
            stack_variables.append(element)
        elif element == '(':
            stack_signs.append(element)
        elif element == ')':
            while stack_signs[-1] != '(':
                stack_variables.append(binary_operation_with_inversion(stack_variables, stack_signs.pop()))
            stack_signs.pop()
        elif element in signs:
            # while len(stack_signs) > 0 and get_priority(stack_signs[-1]) >= get_priority(element):
            while len(stack_signs) > 0 and operations_priority.get(stack_signs[-1], 1) >= operations_priority.get(
                    element, 1):
                stack_variables.append(binary_operation_with_inversion(stack_variables, stack_signs.pop()))
            stack_signs.append(element)
    while len(stack_signs) != 0:
        stack_variables.append(binary_operation_with_inversion(stack_variables, stack_signs.pop()))
    return stack_variables.pop()


def get_stacks_of_signs_and_variables(decoded_formula):
    """
    Получение стеков из знаков и значений
    """
    stack_sign = list(filter(lambda x: x in ['!', '*', '+', '->', '(', ')', '~'], decoded_formula))
    stack_variables = list(filter(lambda x: x not in ['!', '*', '+', '->', '(', ')', '~'], decoded_formula))

    # Создаем множество, чтобы каждый элемент встречался ровно 1 раз
    stack_variables = list(set(stack_variables))
    stack_variables.sort(key=lambda x: int(x[1:]))

    return stack_variables, stack_sign


def replace_variables(formula, column, variables):
    bit = formula.copy()
    for i in range(len(bit)):
        if bit[i] in variables:
            bit[i] = str(column[variables.index(bit[i])])
    return bit



def solution(formula, stack_signs, stack_variables, table):
    answers = []
    for column in table:
        formula_with_numbers = replace_variables(formula, column, stack_variables)
        bit = binary_calculating(formula_with_numbers, list(map(str, column)), stack_signs)
        answers.append(bit)
    return answers


def show_table(table: list, result, variables):
    print('index  ', ' '.join(variables), '   result')
    for i in range(len(table)):
        column = (len(variables[i % 3]) * ' ').join(list(map(str, table[i])))
        print(f'{i + 1}       {column}     {str(result[i])}')


# def show_sknf_form(table, answers, variables):
#     answer = ""
#     for i in range(len(answers)):
#         if answers[i] == 0:
#             answer += " ("
#             for j in range(len(table[i])):
#                 if table[i][j] == 1:
#                     answer += f"!{variables[j]}"
#                     if j != len(table[i]) - 1:
#                         answer += " + "
#                 elif table[i][j] == 0:
#                     answer += variables[j]
#                     if j != len(table[i]) - 1:
#                         answer += " + "
#             answer += ") *"
#     answer = answer[:-2]
#     print(f'SKNF form: {answer}')
#     return answer
#

# def show_sdnf_form(table, answers, variables):
#     answer = ""
#     sdnf = []
#     for i in range(len(answers)):
#         if answers[i] == 1:
#             answer += " ("
#             for j in range(len(table[i])):
#                 if table[i][j] == 0:
#                     answer += f"!{variables[j]}"
#                     if j != len(table[i]) - 1:
#                         answer += " * "
#                 elif table[i][j] == 1:
#                     answer += variables[j]
#                     if j != len(table[i]) - 1:
#                         answer += " * "
#             answer += ") +"
#     answer = answer[:-2]
#     print(f'SDNF Form: {answer}')
#     return answer

def show_sdnf_form(table, answers, variables):
    answer = ""
    sdnf = []
    for i in range(len(answers)):
        if answers[i] == 1:
            row = []
            answer += " ("
            for j in range(len(table[i])):
                if table[i][j] == 0:
                    row.append(f"!{variables[j]}")
                    answer += f"!{variables[j]}"
                    if j != len(table[i]) - 1:
                        answer += " * "
                elif table[i][j] == 1:
                    row.append(variables[j])
                    answer += variables[j]
                    if j != len(table[i]) - 1:
                        answer += " * "
            answer += ") +"
            sdnf.append(row)
    answer = answer[:-2]
    print(f'SDNF Form: {answer}')
    return sdnf

def show_sknf_form(table, answers, variables):
    answer = ""
    sknf = []
    for i in range(len(answers)):
        if answers[i] == 0:
            row = []
            answer += " ("
            for j in range(len(table[i])):
                if table[i][j] == 1:
                    row.append("!" + variables[j])
                    answer += "!" + variables[j]
                    if j != len(table[i]) - 1:
                        answer += " + "
                elif table[i][j] == 0:
                    row.append(variables[j])
                    answer += variables[j]
                    if j != len(table[i]) - 1:
                        answer += " + "
            answer += ") * "
            sknf.append(row)
    answer = answer[:-2]
    print(f'SKNF Form: {answer}')
    return sknf

def sdnf_sknf_num_form(answers):
    ans1 = []
    ans2 = []
    for i in range(len(answers)):
        if not answers[i]:
            ans1.append(i)
        else:
            ans2.append(i)
    print('SKNF_indexes: ', ', '.join(map(str, ans1)))
    print('SDNF_indexes: ', ', '.join(map(str, ans2)))

def from_binary_to_decimal(bin_str: str) -> int:
    # перевод из двоичного представления в двоичное представление
    n = len(bin_str)
    s = 0
    for i in range(n):
        if bin_str[i] == '1':
            s += 2 ** (n - i - 1)
    if bin_str[0] == '1':
        s -= 2 ** n
    return s



def build_int(answers):
    answers_copy = answers.copy()
    bit_form = ''.join(map(str, answers_copy))
    decimal_form = from_binary_to_decimal(bit_form)
    print(f'Index form: {decimal_form}')
    return decimal_form

def intersection_sdnf_sknf(sdnf):
    intersection_result = []
    for i in range(len(sdnf) - 1):
        for j in range(i + 1, len(sdnf)):
            intersection = list(filter(lambda x: x in sdnf[j], sdnf[i]))
            if len(intersection) >= len(sdnf[0]) - 1:
                intersection_result.append(intersection)
    return intersection_result

def reduction_implicants(implicants, substitutions):
    ans = []
    for i in range(len(implicants)):
        row = []
        for j in range(len(implicants)):
            if i == j:
                continue
            implicant = []
            for k in range(len(implicants[j])):
                keys = list(substitutions[i].keys())
                for l in range(len(keys)):
                    if k != l:
                        continue
                    if implicants[j][k][0] == "!":
                        if implicants[j][k][1:] in keys:
                            implicant.append(int(not substitutions[i][implicants[j][k][1:]]))
                        else:
                            implicant.append(implicants[j][k])
                    else:
                        if implicants[j][k] in keys:
                            implicant.append(substitutions[i][implicants[j][k]])
                        else:
                            implicant.append(implicants[j][k])
            row.append(implicant)
        ans.append(row)
    for row in ans:
        i = 0
        while i < len(row):
            if 0 in row[i]:
                row.pop(i)
                i = -1
            i += 1
    row_results = []
    for i in range(len(ans)):
        obj = {}
        for j in range(len(ans[i])):
            for el in ans[i][j]:
                if type(el) == str:
                    if el[0] == "!":
                        if el[1:] in obj:
                            obj[el[1:]] -= 1
                        else:
                            obj[el[1:]] = -1
                    else:
                        if el in obj:
                            obj[el] += 1
                        else:
                            obj[el] = 1
        row_results.append(obj)
    answer = []
    for i in range(len(row_results)):
        keys = list(row_results[i].keys())
        sch = 0
        for j in range(len(keys)):
            sch += row_results[i][keys[j]]
        if sch != 0:
            answer.append(True)
        else:
            answer.append(False)
    return answer

def show_rasch_method_res(build_implicants, implicants, sknf=False):
    str = ""
    if not sknf:
        if build_implicants:
            for i in range(len(build_implicants)):
                for j in range(len(build_implicants[i])):
                    str += build_implicants[i][j]
                    if j != len(build_implicants[i]) - 1:
                        str += "*"
                if i != len(build_implicants) - 1:
                    str += " + "
        else:
            for i in range(len(implicants)):
                for j in range(len(implicants[i])):
                    str += implicants[i][j]
                    if j != len(implicants[i]) - 1:
                        str += "*"
                if i != len(implicants) - 1:
                    str += " + "
    else:
        if build_implicants:
            for i in range(len(build_implicants)):
                str += '('
                for j in range(len(build_implicants[i])):
                    str += build_implicants[i][j]
                    if j != len(build_implicants[i]) - 1:
                        str += "+"
                str += ')'
                if i != len(build_implicants) - 1:
                    str += " * "
        else:
            for i in range(len(implicants)):
                str += '('
                for j in range(len(implicants[i])):
                    str += implicants[i][j]
                    if j != len(implicants[i]) - 1:
                        str += "+"
                str += ')'
                if i != len(implicants) - 1:
                    str += " * "
    print(str)
    return str
def check_implicants_sdnf_sknf(sdnf, sknf=False):
    substitutions = []

    for implicant in sdnf:
        subctitute = {}
        for i in range(len(implicant)):
            if implicant[i][0] == '!':
                subctitute[f"{implicant[i][1:]}"] = 0
            else:
                subctitute[f"{implicant[i]}"] = 1
        substitutions.append(subctitute)
    print(substitutions, 'substitutions')
    answer = reduction_implicants(sdnf, substitutions)
    buildImplicants = []
    for i in range(len(sdnf)):
        if answer[i]:
            buildImplicants.append(sdnf[i])
    show_rasch_method_res(buildImplicants, sdnf, sknf)
def minimizaztion_by_raschet_method(sdnf, sknf):
    sdnf_intersection_value = intersection_sdnf_sknf(sdnf)
    check_implicants_sdnf_sknf(sdnf_intersection_value)
    sknf_intersection_value = intersection_sdnf_sknf(sknf)
    check_implicants_sdnf_sknf(sknf_intersection_value, True)

def main():
    decoded_formula = decode_formula('(!((x1+x2)*x3))')  #(((!x1)+(!x2*x3))->((x1~(!x3))))
    #(!((a+b)*c))
    stack_variables, stac_signs = get_stacks_of_signs_and_variables(decoded_formula)

    answers = solution(decoded_formula, stac_signs, stack_variables, table)
    show_table(table, answers, stack_variables)
    sdnf = show_sdnf_form(table, answers, stack_variables)
    sknf = show_sknf_form(table, answers, stack_variables)
    sdnf_sknf_num_form(answers)
    build_int(answers)
    # minimizaztion_by_raschet_method(sdnf, sknf)





main()
