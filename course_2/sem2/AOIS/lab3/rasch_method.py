import random
from typing import List

from mc_clusky_method import McCluskyMethod


def sdnf_intersect(sdnf):
    intersection_sdnf = []
    for i in range(len(sdnf) - 1):
        for j in range(i + 1, len(sdnf)):
            intersection = list(filter(lambda x: x in sdnf[j], sdnf[i]))
            if len(intersection) >= len(sdnf[0]) - 1:
                intersection_sdnf.append(intersection)
    return intersection_sdnf


def find_difference_in_lists(list_1, list_2):
    difference = list(filter(lambda x: x not in list_2, list_1))
    return difference.copy()


def compare_lists(arr1, arr2):
    count = 0
    for i in range(len(arr2)):
        if arr1[i] == arr2[i]:
            count += 1
    ans = count == len(arr2)
    return ans


def check_if_list_include_list(chosen_list, checked_list):
    for arr in chosen_list:
        if compare_lists(arr, checked_list):
            return True
    return False


def minimization_mc_clasky_sec_term_get_solution(intersect):
    term = []
    for i in range(len(intersect)):
        for j in range(i + 1, len(intersect)):
            if intersect[i][0] == intersect[j][0]:
                if intersect[i][1][0] == '!':
                    if intersect[i][1].find(intersect[j][1]) != -1:
                        term.extend(sdnf_intersect([intersect[i], intersect[j]]))
                else:
                    if intersect[j][1].find(intersect[i][1]) != -1:
                        term.extend(sdnf_intersect([intersect[i], intersect[j]]))
            elif intersect[i][1] == intersect[j][1]:
                if intersect[i][0][0] == '!':
                    if intersect[i][0].find(intersect[j][0]) != -1:
                        term.extend(sdnf_intersect([intersect[i], intersect[j]]))
                else:
                    if intersect[j][0].find(intersect[i][0]) != -1:
                        term.extend(sdnf_intersect([intersect[i], intersect[j]]))
    res = []
    for i in range(len(term)):
        if not check_if_list_include_list(res, term[i]):
            res.append(term[i])
    return res


def implicants_in_sdnf_check(sdnf, sknf, copied_sdnf, sknf_flag=False):
    sdnf_1 = sdnf.copy()
    sknf_1 = sknf.copy()
    substits = []
    reduced_implicts = minimization_mc_clasky_sec_term_get_solution(sdnf)

    if len(reduced_implicts) != 0:
        sdnf = reduced_implicts

    for imps in sdnf:
        substitute = {}
        for i in range(len(imps)):
            if imps[i][0] == '!':
                substitute[imps[i][1:]] = 0
            else:
                substitute[imps[i]] = 1
        substits.append(substitute)

    answer = implicants_reduction_get(sdnf, substits)
    build_implicants = []
    indexes = []
    variables = set()

    for i in range(len(sdnf)):
        if answer[i]:
            build_implicants.append(sdnf[i])
            continue
        indexes.append(i)

    for imps in build_implicants:
        for variable in imps:
            if variable[0] == '!':
                variables.add(variable[1:])
            else:
                variables.add(variable)
    if len(variables) != 3:
        if len(indexes) != 0:
            build_implicants.append(copied_sdnf[indexes[random.randint(0, len(indexes))]])
    else:
        if len(reduced_implicts) != 0:
            build_implicants = reduced_implicts

    if len(sdnf) == 1 and len(copied_sdnf) > len(sdnf):
        build_implicants.append(copied_sdnf[1])

    # show_res_by_rasch_method(build_implicants, sdnf, sknf)
    get_res(sdnf_1, sknf_1)


def solve():
    a = McCluskyMethod()
    return a


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


    # print(str_res)


def get_keys_obj(list_of):
    res_obj = {}
    for i in range(len(list_of)):
        for j in range(len(list_of[i])):
            if isinstance(list_of[i][j], str):
                if list_of[i][j][0] == '!':
                    res_obj[list_of[i][j][1:]] = 0
                else:
                    res_obj[list_of[i][j]] = 0
    return res_obj

def get_res(sdnf, sknf):
    a = solve()
    sdnf = a.get_sdnf_answer(sdnf)
    sknf = a.get_sknf_answer(sknf)
    print(f'sDNF: {sdnf}')
    print(f'sKNF: {sknf}')


def imp_red_get_1(res, implics, substs):
    for i in range(len(implics)):
        row = []
        for j in range(len(implics)):
            if i == j:
                continue
            implicant = []
            for k in range(len(implics[j])):
                keys = list(substs[i].keys())
                for l in range(len(keys)):
                    if k != l:
                        continue
                    if implics[j][k][0] == '!':
                        if implics[j][k][1:] in keys:
                            implicant.append(int(not substs[i][implics[j][k][1:]]))
                        else:
                            implicant.append(implics[j][k])
                    else:
                        if implics[j][k] in keys:
                            implicant.append(substs[i][implics[j][k]])
                        else:
                            implicant.append(implics[j][k])
            row.append(implicant)
        res.append(row)


def imp_red_get_2(res):
    row_res = []
    for i in range(len(res)):
        obj = get_keys_obj(res[i])
        for j in range(len(res[i])):
            for el in res[i][j]:
                if isinstance(el, str):
                    if el[0] == '!':
                        obj[el[1:]] -= 1
                    else:
                        obj[el] += 1
        row_res.append(obj)

    inds = []
    res = []
    for i in range(len(row_res)):
        keys = list(row_res[i].keys())
        count = 0
        for j in range(len(keys)):
            count += row_res[i][keys[j]]
        if count == 0:
            res.append(False)
            inds.append(i)
        else:
            res.append(True)

def implicants_reduction_get(implics, substs):
    res: List[list] = []
    imp_red_get_1(res, implics, substs)

    for row in res:
        for i in range(len(row)):
            if 0 in row[i]:
                row.pop(i)
                break
    imp_red_get_2(res)
    return res


def minimizetion_by_rasch_method(sdnf, sknf):
    sdnf_inters = sdnf_intersect(sdnf)
    sdnf_copy = sdnf_inters[:]
    if len(sdnf_inters) == 1:
        for i in range(len(sdnf)):
            if len(find_difference_in_lists(sdnf[i], sdnf_inters[0])) == len(sdnf[i]):
                sdnf_copy.append(sdnf[i])
    implicants_in_sdnf_check(sdnf_inters, sknf, sdnf_copy)

    sknf_inters = sdnf_intersect(sknf)
    sknf_copy = sknf_inters[:]
    if len(sknf_inters) == 1:
        for i in range(len(sknf)):
            if len(find_difference_in_lists(sknf[i], sknf_inters[0])) == len(sknf[i]):
                sknf_copy.append(sknf[i])


    implicants_in_sdnf_check(sdnf, sknf, True)
