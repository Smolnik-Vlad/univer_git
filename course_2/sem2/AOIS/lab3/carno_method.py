from sdnf_sknf import decode_formula, get_stacks_of_signs_and_variables, solution

table = [[0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 1, 1], [1, 0, 0], [1, 0, 1], [1, 1, 0], [1, 1, 1]]


def get_from_k_map_res(ans, k_map):
    for i in range(len(k_map)):
        for j in range(len(k_map[i])):
            k_map[i][j] = ans[k_map[i][j]]
    return k_map


def check_of_two_power(a):
    if a == 1:
        return False
    return (a & (a - 1)) == 0


def get_suitable_groups_from_kmap(k_map, compare=1):
    current_groups = []
    for i in range(len(k_map)):
        for j in range(len(k_map[i])):
            if k_map[i][j] == compare:
                k = j + 1
                while k < len(k_map[i]) and k_map[i][k] == compare:
                    if check_of_two_power(k - j - 1):
                        current_groups.append({"row": [i], "group": [j, k], "side": False})
                    k += 1
                k = i + 1
                if k > 1:
                    continue
                while k < len(k_map) and k_map[k][j] == compare:
                    if check_of_two_power(k + 1):
                        current_groups.append({"row": [i, k], "group": [j], "side": False})
                    k += 1
                    if k > 1:
                        break
    # find squares
    for j in range(len(k_map[0])):
        if k_map[0][j] == compare and k_map[1][j] == compare:
            k = j + 1
            while k < len(k_map[0]) and k_map[0][k] == compare and k_map[1][k] == compare:
                if check_of_two_power(k - j - 1):
                    current_groups.append({"row": [0, 1], "group": [j, k], "side": False})
                k += 1
    # find side squares
    if k_map[0][0] == compare and k_map[0][len(k_map[0]) - 1] == compare:
        current_groups.append({"row": [0], "group": [0, len(k_map[0]) - 1], "side": True})
    if k_map[1][0] == compare and k_map[1][len(k_map[0]) - 1] == compare:
        current_groups.append({"row": [1], "group": [0, len(k_map[1]) - 1], "side": True})
    if k_map[0][0] == compare and k_map[1][0] == compare and k_map[0][len(k_map[0]) - 1] == compare and k_map[1][
        len(k_map[0]) - 1] == compare:
        current_groups.append({"row": [0, 1], "group": [0, len(k_map[1]) - 1], "side": True})
    return current_groups


def compare_arrays(array1, array2):
    indexes = []
    for i in range(len(array1)):
        if array1[i] == array2[i]:
            indexes.append(i)
    return indexes


def sorting_arr_length_arrs(ansvers):
    for i in range(len(ansvers)):
        for j in range(len(ansvers)):
            if len(ansvers[i]) < len(ansvers[j]):
                ansvers[i], ansvers[j] = ansvers[j], ansvers[i]


def comparing_variables_and_groups(groups, variables_vertical_groups, variables_horisontal_groups, variables,
                                   sknf=False):
    vertical = [variables[0]]  # x1
    horizontal = [variables[1], variables[2]]  # x2 x3
    variable_ans = []

    for group in groups:
        if len(group['row']) == 1:
            variable = '!x1' if not variables_vertical_groups[group['row'][0]] else 'x1'
            indexOfDiff = compare_arrays(variables_horisontal_groups[group['group'][0]],
                                         variables_horisontal_groups[group['group'][1]])
            if len(indexOfDiff) == 0:
                variable_ans.append([variable])
                continue
            else:
                vars = []
                for i in indexOfDiff:
                    vars.append(f"!{horizontal[i]}" if not int(variables_horisontal_groups[group['group'][0]][i]) else
                                horizontal[i])
                variable_ans.append([variable, *vars])
        elif len(group['group']) == 1:
            firsVar = f"!{horizontal[0]}" if not int(variables_horisontal_groups[group['group'][0]][0]) else horizontal[
                0]
            secondVar = f"!{horizontal[1]}" if not int(variables_horisontal_groups[group['group'][0]][1]) else \
                horizontal[1]
            variable_ans.append([firsVar, secondVar])
        elif len(group['group']) > 1 and len(group['row']) > 1:
            indexOfDiff = compare_arrays(variables_horisontal_groups[group['group'][0]],
                                         variables_horisontal_groups[group['group'][1]])
            if len(indexOfDiff) != 0:
                vars = []
                for i in indexOfDiff:
                    vars.append(f"!{horizontal[i]}" if not int(variables_horisontal_groups[group['group'][0]][i]) else
                                horizontal[i])
                variable_ans.append(vars)

    ans_variables_and_so = set()
    sorting_arr_length_arrs(variable_ans)
    unused_answer = variable_ans.copy()
    if sknf:
        for i in range(len(unused_answer)):
            for j in range(len(unused_answer[i])):
                if unused_answer[i][j][0] == '!':
                    unused_answer[i][j] = unused_answer[i][j][1:]
                else:
                    unused_answer[i][j] = f"!{unused_answer[i][j]}"

    k = 0
    minimal_answer = []
    while len(ans_variables_and_so) != 3 and k < len(variable_ans):
        size_start = len(ans_variables_and_so)
        for j in range(len(variable_ans[k])):
            if variable_ans[k][j][0] == '!':
                ans_variables_and_so.add(variable_ans[k][j][1:])
            else:
                ans_variables_and_so.add(variable_ans[k][j])
        if len(ans_variables_and_so) != size_start:
            minimal_answer.append(variable_ans[k])
        k += 1

    return {'unused_answer': unused_answer, 'minimal_answer': minimal_answer}


def ger_result_from_rasch_method(builded_implicants, implicants, sknf=False):
    result = ""
    if not sknf:
        if len(builded_implicants) > 0:
            for i in range(len(builded_implicants)):
                for j in range(len(builded_implicants[i])):
                    result += builded_implicants[i][j]
                    if j != len(builded_implicants[i]) - 1:
                        result += "*"
                if i != len(builded_implicants) - 1:
                    result += " + "
        else:
            for i in range(len(implicants)):
                for j in range(len(implicants[i])):
                    result += implicants[i][j]
                    if j != len(implicants[i]) - 1:
                        result += "*"
                if i != len(implicants) - 1:
                    result += " + "
    else:
        if len(builded_implicants) > 0:
            for i in range(len(builded_implicants)):
                result += '('
                for j in range(len(builded_implicants[i])):
                    result += builded_implicants[i][j]
                    if j != len(builded_implicants[i]) - 1:
                        result += "+"
                result += ')'
                if i != len(builded_implicants) - 1:
                    result += " * "
        else:
            for i in range(len(implicants)):
                result += '('
                for j in range(len(implicants[i])):
                    result += implicants[i][j]
                    if j != len(implicants[i]) - 1:
                        result += "+"
                result += ')'
                if i != len(implicants) - 1:
                    result += " * "

    print(result)


def karnaugh_map(answers, variables):
    carno_map = [[], []]
    carno_map[1].extend([0, 1, 3, 2])
    carno_map[0].extend([4, 5, 7, 6])
    my_map = get_from_k_map_res(answers, carno_map)
    list_of_sdnf = get_suitable_groups_from_kmap(my_map)
    list_of_sknf = get_suitable_groups_from_kmap(my_map, 0)

    variables_vertical_list = [1, 0]
    variables_horisontal_list = [[0, 0], [0, 1], [1, 1], [1, 0]]
    sdnf_obj = comparing_variables_and_groups(list_of_sdnf, variables_vertical_list, variables_horisontal_list,
                                              variables)
    sknf_obj = comparing_variables_and_groups(list_of_sknf, variables_vertical_list, variables_horisontal_list,
                                              variables, True)

    impl_sdnf = sdnf_obj["unused_answer"]
    minimal_answer_sdnf = sdnf_obj["minimal_answer"]
    imp_sknf = sknf_obj["unused_answer"]
    minimal_answer_sdnf = sknf_obj["minimal_answer"]

    ger_result_from_rasch_method(minimal_answer_sdnf, impl_sdnf)
    ger_result_from_rasch_method(minimal_answer_sdnf, imp_sknf, True)


# karnaugh_map(answers, variables)

def carnaugh_method(formula):
    decoded_formula = decode_formula(formula)  # (((!x1)+(!x2*x3))->((x1~(!x3))))   '(!((x1+x2)*x3))'
    # (!((a+b)*c))
    stack_variables, stac_signs = get_stacks_of_signs_and_variables(decoded_formula)

    answers = solution(decoded_formula, stac_signs, stack_variables, table)
    print(answers)

    karnaugh_map(answers, stack_variables)
