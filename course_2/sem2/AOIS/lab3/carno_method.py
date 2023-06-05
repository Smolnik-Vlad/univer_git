from mc_clusky_method import McCluskyMethod
from sdnf_sknf import decode_formula, get_stacks_of_signs_and_variables, solution, show_sdnf_form, show_sknf_form

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


def gsgfk1(k_map, compare, current_groups):
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


def get_suitable_groups_from_kmap(k_map, compare=1):
    current_groups = []

    gsgfk1(k_map, compare, current_groups)
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


def cvag(groups, variables_vertical_groups, variables_horisontal_groups, variable_ans, horizontal):
    for group in groups:
        if len(group['row']) == 1:
            variable = '!x1' if not variables_vertical_groups[group['row'][0]] else 'x1'
            index_of_diff = compare_arrays(variables_horisontal_groups[group['group'][0]],
                                         variables_horisontal_groups[group['group'][1]])
            if len(index_of_diff) == 0:
                variable_ans.append([variable])
                continue
            else:
                vars = []
                for i in index_of_diff:
                    vars.append(f"!{horizontal[i]}" if not int(variables_horisontal_groups[group['group'][0]][i]) else
                                horizontal[i])
                variable_ans.append([variable, *vars])
        elif len(group['group']) == 1:
            firs_var = f"!{horizontal[0]}" if not int(variables_horisontal_groups[group['group'][0]][0]) else horizontal[
                0]
            second_var = f"!{horizontal[1]}" if not int(variables_horisontal_groups[group['group'][0]][1]) else \
                horizontal[1]
            variable_ans.append([firs_var, second_var])
        elif len(group['group']) > 1 and len(group['row']) > 1:
            index_of_diff = compare_arrays(variables_horisontal_groups[group['group'][0]],
                                         variables_horisontal_groups[group['group'][1]])
            if len(index_of_diff) != 0:
                vars = []
                for i in index_of_diff:
                    vars.append(f"!{horizontal[i]}" if not int(variables_horisontal_groups[group['group'][0]][i]) else
                                horizontal[i])
                variable_ans.append(vars)


def cvag_2(sknf, unused_answer, ans_variables_and_so, variable_ans, minimal_answer):
    if sknf:
        for i in range(len(unused_answer)):
            for j in range(len(unused_answer[i])):
                if unused_answer[i][j][0] == '!':
                    unused_answer[i][j] = unused_answer[i][j][1:]
                else:
                    unused_answer[i][j] = f"!{unused_answer[i][j]}"

    k = 0

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


def comparing_variables_and_groups(groups, variables_vertical_groups, variables_horisontal_groups, variables,
                                   sknf=False):
    vertical = [variables[0]]
    horizontal = [variables[1], variables[2]]
    variable_ans = []

    cvag(groups, variables_vertical_groups, variables_horisontal_groups, variable_ans, horizontal)

    sorting_arr_length_arrs(variable_ans)
    unused_answer = variable_ans.copy()
    minimal_answer = []

    return {'unused_answer': unused_answer, 'minimal_answer': minimal_answer}


def show_rasch_sdnf(builded_imps, str_res, imps):
    if builded_imps:
        for i in range(len(builded_imps)):
            for j in range(len(builded_imps[i])):
                str_res += builded_imps[i][j]
                if j != len(builded_imps[i]) - 1:
                    str_res += "*"
            if i != len(builded_imps) - 1:
                str_res += " + "
    else:
        for i in range(len(imps)):
            for j in range(len(imps[i])):
                str_res += imps[i][j]
                if j != len(imps[i]) - 1:
                    str_res += "*"
            if i != len(imps) - 1:
                str_res += " + "


def show_rasch_sknf(builded_imps, str_res, imps):
    if builded_imps:
        for i in range(len(builded_imps)):
            str_res += '('
            for j in range(len(builded_imps[i])):
                str_res += builded_imps[i][j]
                if j != len(builded_imps[i]) - 1:
                    str_res += "+"
            str_res += ')'
            if i != len(builded_imps) - 1:
                str_res += " * "
    else:
        for i in range(len(imps)):
            str_res += '('
            for j in range(len(imps[i])):
                str_res += imps[i][j]
                if j != len(imps[i]) - 1:
                    str_res += "+"
            str_res += ')'
            if i != len(imps) - 1:
                str_res += " * "


def show_res_by_rasch_method(builded_imps, imps, sknf=False):
    str_res = ""
    if not sknf:
        show_rasch_sdnf(builded_imps, str_res, imps)

    else:
        show_rasch_sknf(builded_imps, str_res, imps)

    # print(result)


def get_result(table, answers, stack_variables):
    sdnf = show_sdnf_form(table, answers, stack_variables)
    sknf = show_sknf_form(table, answers, stack_variables)
    a = McCluskyMethod()

    c = a.get_sdnf_answer(sdnf)
    print('sDNF:', c)
    c = a.get_sknf_answer(sknf)

    print('sKNF: ', c)


def karnaugh_map(answers, variables, table, answer, stack_variable):
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
    imp_sknf = sknf_obj["unused_answer"]
    minimal_answer_sdnf = sknf_obj["minimal_answer"]

    show_res_by_rasch_method(minimal_answer_sdnf, impl_sdnf)
    show_res_by_rasch_method(minimal_answer_sdnf, imp_sknf, True)

    get_result(table, answers, stack_variable)




def carnaugh_method(formula):
    decoded_formula = decode_formula(formula)
    # (!((a+b)*c))
    stack_variables, stac_signs = get_stacks_of_signs_and_variables(decoded_formula)

    answers = solution(decoded_formula, stac_signs, stack_variables, table)

    karnaugh_map(answers, stack_variables, table, answers, stack_variables)
