def build_sdnf(table, answers, variables):
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


def show_table(table: list, result, variables):
    print('index  ', ' '.join(variables), '   result')
    for i in range(len(table)):
        column = (len(variables[i % 3]) * ' ').join(list(map(str, table[i])))
        print(f'{i + 1}       {column}     {str(result[i])}')

