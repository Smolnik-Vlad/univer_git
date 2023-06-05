from typing import Dict, List

from minimization import McCluskyMethod
from sdnf_sknf_part import build_sdnf

fsm_signal = 'V'
pre_tacts = ['q1', 'q2', 'q3']
post_tacts = ['Q1', 'Q2', 'Q3']
trigger_functions = ['H1', 'H2', 'H3']

input_vars = ['q1', 'q2', 'q3', 'V']


def get_table(n):
    rows = 2 ** n
    table = []

    for i in range(rows):
        row = []
        for j in range(n - 1, -1, -1):
            row.append((i >> j) & 1)
        table.append(row)

    return table


def fill_tables(inputs_table, excitation_table, table):
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


def build_truth_table(count: int) -> Dict[str, List[List[int]]]:
    table = get_table(count)
    table_for_input = []
    table_for_excitation = []
    print(table)

    fill_tables(table_for_input, table_for_excitation, table)

    print("TRANSITION TABLE")
    print(" ".join(pre_tacts), fsm_signal, " ".join(post_tacts),
          " ".join(trigger_functions))
    for i in range(len(table_for_input)):
        print("  ".join(map(str, table_for_input[i])), "", "  ".join(map(str, table_for_excitation[i])))
    only_wars_table = []
    for i in range(len(table_for_input)):
        only_wars_table.append(table_for_input[i][:4])
    return {"table_with_only_vars": only_wars_table, "excitation_table": table_for_excitation}


def lab5_minimization_h1_h2_h3(vars_table, table_for_excitation, vars):
    h1 = list(map(lambda x: x[0], table_for_excitation))
    h2 = list(map(lambda x: x[1], table_for_excitation))
    h3 = list(map(lambda x: x[2], table_for_excitation))
    h1_sdnf = build_sdnf(vars_table, h1, vars)
    h2_sdnf = build_sdnf(vars_table, h2, vars)
    h3_sdnf = build_sdnf(vars_table, h3, vars)

    min_obj = McCluskyMethod()
    print('H1:', min_obj.get_sdnf_answer(h1_sdnf))
    print('H2:', min_obj.get_sdnf_answer(h2_sdnf))
    print('H3:', min_obj.get_sdnf_answer(h3_sdnf))


tables = build_truth_table(3)

lab5_minimization_h1_h2_h3(tables['table_with_only_vars'], tables['excitation_table'], input_vars)
