table = [[0, 0, 0], [0, 0, 1], [0, 1, 0], [1, 0, 0], [0, 1, 1], [1, 1, 0], [1, 0, 1], [1, 1, 1]]
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
    ans = formula.copy()
    for i in range(len(ans)):
        if ans[i] in variables:
            ans[i] = str(column[variables.index(ans[i])])
    return ans


def solution(formula, stack_signs, stack_variables, table):
    answers = []
    for column in table:
        formula_with_numbers = replace_variables(formula, column, stack_variables)
        ans = binary_calculating(formula_with_numbers, list(map(str, column)), stack_signs)
        answers.append(ans)
    return answers


def show_table(table: list, result, variables):
    print('index  ', ' '.join(variables), '   result')
    for i in range(len(table)):
        column = (len(variables[i % 3]) * ' ').join(list(map(str, table[i])))
        print(f'{i + 1}       {column}     {str(result[i])}')


def show_sknf_form(table, answers, variables):
    answer = "SKNF Form: "
    for i in range(len(answers)):
        if answers[i] == 0:
            answer += " ("
            for j in range(len(table[i])):
                if table[i][j] == 1:
                    answer += f"!{variables[j]}"
                    if j != len(table[i]) - 1:
                        answer += " + "
                elif table[i][j] == 0:
                    answer += variables[j]
                    if j != len(table[i]) - 1:
                        answer += " + "
            answer += ") *"
    answer = answer[:-2]
    print(answer)


def show_sdnf_form(table, answers, variables):
    answer = "SDNF Form: "
    for i in range(len(answers)):
        if answers[i] == 1:
            answer += " ("
            for j in range(len(table[i])):
                if table[i][j] == 0:
                    answer += f"!{variables[j]}"
                    if j != len(table[i]) - 1:
                        answer += " * "
                elif table[i][j] == 1:
                    answer += variables[j]
                    if j != len(table[i]) - 1:
                        answer += " * "
            answer += ") +"
    answer = answer[:-2]
    print(answer)


def sdnf_sknf_num_form(answers):
    ans1 = []
    ans2 = []
    for i in range(len(answers)):
        if not answers[i]:
            ans1.append(i + 1)
        else:
            ans2.append(i + 1)
    print('SKNF_indexes: ', ', '.join(map(str, ans1)))
    print('SDNF_indexes: ', ', '.join(map(str, ans2)))


def build_int(answers):
    answers_copy = answers.copy()
    answers_copy.append('.')
    ans = ''.join(map(str, answers_copy))
    print(f'Index form: {ans}')
    return ans


def main():
    decoded_formula = decode_formula('((x1+(x2*(!x3)))->((x1~(!x2))))')  #
    stack_variables, stac_signs = get_stacks_of_signs_and_variables(decoded_formula)

    answers = solution(decoded_formula, stac_signs, stack_variables, table)
    show_table(table, answers, stack_variables)
    show_sdnf_form(table, answers, stack_variables)
    show_sknf_form(table, answers, stack_variables)
    sdnf_sknf_num_form(answers)
    build_int(answers)


main()
