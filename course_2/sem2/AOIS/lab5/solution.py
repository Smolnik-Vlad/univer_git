from typing import Dict, List

from minimization import McCluskyMethod
from sdnf_sknf_part import build_sdnf

fsm_signal = 'V'
pre_tacts = ['q1', 'q2', 'q3']
post_tacts = ['Q1', 'Q2', 'Q3']
trigger_functions = ['H1', 'H2', 'H3']

input_vars = ['q1', 'q2', 'q3', 'V']


def get_truth_table(n):
    rows = 2 ** n
    table = []

    for i in range(rows):
        row = []
        for j in range(n - 1, -1, -1):
            row.append((i >> j) & 1)
        table.append(row)

    return table


def build_table(count: int) -> Dict[str, List[List[int]]]:
    table = get_truth_table(count)
    inputs_table = []
    excitation_table = []
    print(table)
    for i in range(len(table)):
        for j in range(2):
            if j == 0:
                inputs_table.append(table[i] + [j] + table[i])
            elif j == 1:
                if i != len(table) - 1:
                    inputs_table.append(table[i] + [j] + table[i + 1])
                else:
                    inputs_table.append(table[i] + [j] + table[0])
    for i in range(len(inputs_table)):
        row = []
        for j in range(3):
            if inputs_table[i][j] != inputs_table[i][j + 4]:
                row.append(1)
            else:
                row.append(0)
        excitation_table.append(row)
    print("TRANSITION TABLE")
    print(" ".join(pre_tacts), fsm_signal, " ".join(post_tacts),
          " ".join(trigger_functions))
    for i in range(len(inputs_table)):
        print("  ".join(map(str, inputs_table[i])), "", "  ".join(map(str, excitation_table[i])))
    table_with_only_vars = []
    for i in range(len(inputs_table)):
        table_with_only_vars.append(inputs_table[i][:4])
    return {"table_with_only_vars": table_with_only_vars, "excitation_table": excitation_table}




def get_h1_h2_h3(excitation_table):
    h1 = list(map(lambda x: x[0], excitation_table))
    h2 = list(map(lambda x: x[1], excitation_table))
    h3 = list(map(lambda x: x[2], excitation_table))
    return h1,  h2,  h3


def minimize_h1_h2_h3(table_with_only_vars, excitation_table, input_vars):
    h1, h2, h3 = get_h1_h2_h3(excitation_table)
    h1_sdnf = build_sdnf(table_with_only_vars, h1, input_vars)
    h2_sdnf = build_sdnf(table_with_only_vars, h2, input_vars)
    h3_sdnf = build_sdnf(table_with_only_vars, h3, input_vars)

    min_obj = McCluskyMethod()
    print('H1:', min_obj.get_sdnf_answer(h1_sdnf))
    print('H2:', min_obj.get_sdnf_answer(h2_sdnf))
    print('H3:', min_obj.get_sdnf_answer(h3_sdnf))


tables = build_table(3)

minimize_h1_h2_h3(tables['table_with_only_vars'], tables['excitation_table'], input_vars)
