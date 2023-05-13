import random

table = [[0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 1, 1], [1, 0, 0], [1, 0, 1], [1, 1, 0], [1, 1, 1]]
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


# ________________________________________________________________
def get_random_int(maxi):
    return random.randint(0, maxi - 1)


def form_keys_object(arr):
    obj = {}
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            if isinstance(arr[i][j], str):
                if arr[i][j][0] == '!':
                    obj[arr[i][j][1:]] = 0
                else:
                    obj[arr[i][j]] = 0
    return obj


def difference_arrays(arr1, arr2):
    difference = list(filter(lambda x: x not in arr2, arr1))
    return difference


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
                    if implicants[j][k][0] == '!':
                        if keys.count(implicants[j][k][1:]) != 0:
                            implicant.append(int(not substitutions[i][implicants[j][k][1:]]))
                        else:
                            implicant.append(implicants[j][k])
                    else:
                        if keys.count(implicants[j][k]) != 0:
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
        obj = form_keys_object(ans[i])
        for j in range(len(ans[i])):
            for el in ans[i][j]:
                if isinstance(el, str):
                    if el[0] == '!':
                        obj[el[1:]] -= 1
                    else:
                        obj[el] += 1
        row_results.append(obj)
    indexes = []
    answer = []
    for i in range(len(row_results)):
        keys = list(row_results[i].keys())
        sch = 0
        for j in range(len(keys)):
            sch += row_results[i][keys[j]]
        if sch == 0:
            answer.append(False)
            indexes.append(i)
        else:
            answer.append(True)
    return answer


def compare_arrays(arr1, arr2):
    count = 0
    for i in range(len(arr2)):
        if arr1[i] == arr2[i]:
            count += 1
    ans = count == len(arr2)
    return ans


def check_array_include_array(chosen_array, checked_array):
    for arr in chosen_array:
        if compare_arrays(arr, checked_array):
            return True
    return False


def sdnf_intersection(sdnf):
    intersection_sdnf = []
    for i in range(len(sdnf) - 1):
        for j in range(i + 1, len(sdnf)):
            intersection = [x for x in sdnf[i] if x in sdnf[j]]
            if len(intersection) >= len(sdnf[0]) - 1:
                intersection_sdnf.append(intersection)
    return intersection_sdnf


def minimization_mcclasky_sec_term(intersection):
    new_terms = []
    for i in range(len(intersection)):
        for j in range(i + 1, len(intersection)):
            if intersection[i][0] == intersection[j][0]:
                if intersection[i][1][0] == '!':
                    if intersection[i][1].find(intersection[j][1]) != -1:
                        new_terms.extend(sdnf_intersection([intersection[i], intersection[j]]))
                else:
                    if intersection[j][1].find(intersection[i][1]) != -1:
                        new_terms.extend(sdnf_intersection([intersection[i], intersection[j]]))
            elif intersection[i][1] == intersection[j][1]:
                if intersection[i][0][0] == '!':
                    if intersection[i][0].find(intersection[j][0]) != -1:
                        new_terms.extend(sdnf_intersection([intersection[i], intersection[j]]))
                else:
                    if intersection[j][0].find(intersection[i][0]) != -1:
                        new_terms.extend(sdnf_intersection([intersection[i], intersection[j]]))
    answer = []
    for i in range(len(new_terms)):
        if not check_array_include_array(answer, new_terms[i]):
            answer.append(new_terms[i])
    return answer


def implicants_sdnf_check(sdnf, copyOfSDNF, sknf=False):
    substitutions = []

    reduced_implicants = minimization_mcclasky_sec_term(sdnf)

    if len(reduced_implicants) != 0:
        sdnf = reduced_implicants

    for implicant in sdnf:
        subctitute = {}
        for i in range(len(implicant)):
            if implicant[i][0] == '!':
                subctitute[implicant[i][1:]] = 0
            else:
                subctitute[implicant[i]] = 1
        substitutions.append(subctitute)

    answer = reduction_implicants(sdnf, substitutions)
    build_implicants, indexes = [], []
    variables = set()
    for i in range(len(sdnf)):
        if answer[i]:
            build_implicants.append(sdnf[i])
            continue
        indexes.append(i)
    for i in range(len(build_implicants)):
        for variable in build_implicants[i]:
            if variable[0] == '!':
                variables.add(variable[1:])
            else:
                variables.add(variable[0:])
    # let reduced_implicants = reduceImplicants(build_implicants)
    if len(variables) != 3:
        if len(indexes) != 0:
            build_implicants.append(copyOfSDNF[indexes[get_random_int(len(indexes))]])
    else:
        if len(reduced_implicants) != 0:
            build_implicants = reduced_implicants
    if len(sdnf) == 1 and len(copyOfSDNF) > len(sdnf):
        build_implicants.append(copyOfSDNF[1])

    show_rasch_method_res(build_implicants, sdnf, sknf)

def rasch_minimization(SDNF, SKNF):
    intersection_of_sdnf = sdnf_intersection(SDNF)
    copy_of_sdnf = intersection_of_sdnf[:]
    if len(intersection_of_sdnf) == 1:
        for i in range(len(SDNF)):
            if len(difference_arrays(SDNF[i], intersection_of_sdnf[0])) == len(SDNF[i]):
                copy_of_sdnf.append(SDNF[i])
    implicants_sdnf_check(intersection_of_sdnf, copy_of_sdnf)

    intersection_of_sknf = sdnf_intersection(SKNF)
    copy_of_sknf = intersection_of_sknf[:]
    if len(intersection_of_sknf) == 1:
        for i in range(len(SKNF)):
            if len(difference_arrays(SKNF[i], intersection_of_sknf[0])) == len(SKNF[i]):
                copy_of_sknf.append(SKNF[i])
    implicants_sdnf_check(intersection_of_sknf, copy_of_sknf, True)


# ________________________________________________________________


def fill_current_object(object1, sdnf_sknf, intersection):
    obj = dict(object1)
    for i in range(len(sdnf_sknf)):
        for j in range(len(intersection)):
            if len(difference_arrays(sdnf_sknf[i], intersection[j])) == 1:
                obj[f'{sdnf_sknf[i]}'].append(intersection[j])
    return dict(obj)


def get_filled_min_object_terms(current_object, sdnf_sknf, intersection):
    obj = dict(current_object)
    for i in range(len(sdnf_sknf)):
        for j in range(len(intersection)):
            if len(difference_arrays(sdnf_sknf[i], intersection[j])) == 2:
                obj[f'{sdnf_sknf[i]}'].append(intersection[j])
        return dict(obj)


def build_object(sdnf_sknf, intersection, min_term=False):
    current_object = form_object(sdnf_sknf)
    if min_term:
        filled_object = get_filled_min_object_terms(current_object, sdnf_sknf, intersection)
    else:
        filled_object = fill_current_object(current_object, sdnf_sknf, intersection)
    return dict(filled_object)


def form_object(sdnf_sknf):
    obj = {}
    for row in sdnf_sknf:
        obj[f'{row}'] = []
    return dict(obj)


def build_two_dimension_table(sdnf_sknf, intersection):
    table = []
    # Fill table
    for i in range(len(sdnf_sknf)):
        row = []
        for j in range(len(intersection)):
            row.append(False)
            table.append(row)
    # Build table
    for i in range(len(sdnf_sknf)):
        for j in range(len(intersection)):
            if len(difference_arrays(sdnf_sknf[i], intersection[j])) == 1:
                table[i][j] = True
    return [list(row) for row in table]

def from_str_to_list(element):
    if '[' not in element[0]:
        return element
    else:
        for i in range(len(element)):
            element[i] = element[i].replace('[', '')
            element[i] = element[i].replace(']', '')
            element[i] = element[i].replace('\'', '')
        a = str(element)
        return eval(a)



def build_tnf_by_mcclasky(obj):
    keys = list(obj.keys())
    chosen_implicants = []

    for i in range(len(keys)):
        if len(obj[keys[i]]) == 1:
            sch = 0
            for j in range(len(chosen_implicants)):
                if chosen_implicants[j] == obj[keys[i]][0]:
                    continue
                else:
                    sch += 1
            if sch == len(chosen_implicants):
                chosen_implicants.append(obj[keys[i]][0])

    for i in range(len(keys)):
        sch = 0
        for j in range(len(chosen_implicants)):
            if check_array_include_array(obj[keys[i]], chosen_implicants[j]):
                break
            else:
                sch += 1
        if sch == len(chosen_implicants) and len(obj[keys[i]]) > 0:
            chosen_implicants.append(obj[keys[i]][0])
        elif sch == len(chosen_implicants) and len(obj[keys[i]]) == 0:
            chosen_implicants.append(keys[i].split(','))
    chosen_implicants = list(map(from_str_to_list, chosen_implicants))
    return chosen_implicants


def mcclasky_minimization(sdnf, sknf):
    intersection_of_sdnf = sdnf_intersection(sdnf)
    min_terms_sdnf = minimization_mcclasky_sec_term(intersection_of_sdnf)

    object_sdnf = build_object(sdnf, intersection_of_sdnf)

    if len(min_terms_sdnf) != 0:
        intersection_of_sdnf = min_terms_sdnf
        object_sdnf = build_object(sdnf, intersection_of_sdnf, True)

    intersection_of_sknf = sdnf_intersection(sknf)
    min_terms_sknf = minimization_mcclasky_sec_term(intersection_of_sknf)

    object_sknf = build_object(sknf, intersection_of_sknf)

    if len(min_terms_sknf) != 0:
        intersection_of_sknf = min_terms_sknf
        object_sknf = build_object(sknf, intersection_of_sknf, True)

    table_sdnf = build_two_dimension_table(sdnf, intersection_of_sdnf)
    table_sknf = build_two_dimension_table(sknf, intersection_of_sknf)


    chosen_implicants_sdnf = build_tnf_by_mcclasky(object_sdnf)
    chosen_implicants_sknf = build_tnf_by_mcclasky(object_sknf)
    show_rasch_method_res(chosen_implicants_sdnf, intersection_of_sdnf)
    show_rasch_method_res(chosen_implicants_sknf, intersection_of_sknf, True)


def main():
    decoded_formula = decode_formula('(!((x1+x2)*x3))')  # (((!x1)+(!x2*x3))->((x1~(!x3))))
    # (!((x1+x2)*x3)) #работает 2й и 3(2)
    stack_variables, stac_signs = get_stacks_of_signs_and_variables(decoded_formula)

    answers = solution(decoded_formula, stac_signs, stack_variables, table)
    show_table(table, answers, stack_variables)
    sdnf = show_sdnf_form(table, answers, stack_variables)
    sknf = show_sknf_form(table, answers, stack_variables)
    sdnf_sknf_num_form(answers)
    build_int(answers)
    print('________________________________________________________________')
    rasch_minimization(sdnf, sknf)
    print('________________________________________________________________')
    mcclasky_minimization(sdnf, sknf)


main()
