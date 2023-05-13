table = [[0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 1, 1], [1, 0, 0], [1, 0, 1], [1, 1, 0], [1, 1, 1]]
borrows = [0, 1, 1, 1, 0, 0, 0, 1]
differences = [0, 1, 1, 0, 1, 0, 0, 1]
x_table = [[0, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0], [0, 0, 1, 1], [0, 1, 0, 0], [0, 1, 0, 1], [0, 1, 1, 0],
           [0, 1, 1, 1], [1, 0, 0, 0], [1, 0, 0, 1], [1, 0, 1, 0], [1, 0, 1, 1], [1, 1, 0, 0], [1, 1, 0, 1],
           [1, 1, 1, 0], [1, 1, 1, 1]]

y_table_for_showing = [[0, 0, 0, 1], [0, 0, 1, 0], [0, 0, 1, 1], [0, 1, 0, 0], [0, 1, 0, 1], [0, 1, 1, 0], [0, 1, 1, 1],
                       [1, 0, 0, 0], [1, 0, 0, 1], [1, 0, 1, 0]]

y_table = [[0, 0, 0, 0, 0, 0, 0, 1, 1, 1], [0, 0, 0, 1, 1, 1, 1, 0, 0, 0], [0, 1, 1, 0, 0, 1, 1, 0, 0, 1],
           [1, 0, 1, 0, 1, 0, 1, 0, 1, 0]]


class McCluskyMethod:

    def get_small_terms(self, sdnf_sknf):
        sdnf_sknf = list(map(lambda x: x[:], sdnf_sknf))
        single_parts = []
        while self.get_vars_count(sdnf_sknf[0]) > 1:
            # Здесь проходим все время по sdnf_sknf до того момента, пока не сократим до самого конца
            reduced_elements = []
            for i in range(len(sdnf_sknf)):
                self.check(i, reduced_elements, sdnf_sknf, single_parts)
            sdnf_sknf = reduced_elements
            if len(reduced_elements) == 0:
                break

        small_terms = []
        for i in range(len(sdnf_sknf)):
            if not self.similarity_check(small_terms, sdnf_sknf[i]):
                small_terms.append(sdnf_sknf[i])
        for i in range(len(single_parts)):
            small_terms.append(single_parts[i])
        return small_terms

    @staticmethod
    def get_vars_count(term):
        """Подсчет количества переменных"""
        sch = 0
        for variable in term:
            if variable != "-":
                sch += 1
        return sch

    @staticmethod
    def similarity_check(res, sdnf_func_part):
        if not res:
            return False
        for i in range(len(res)):
            flag = True
            for j in range(len(res[i])):
                if res[i][j] != sdnf_func_part[j]:
                    flag = False
            if flag:
                return True
        return False

    @staticmethod
    def include_check(small_term, full_terms):
        for i in range(len(full_terms)):
            if small_term[i] != full_terms[i] and small_term[i] != '-':
                return False
        return True

    def check(self, index, result, reduce_parts, single_parts):
        """Формируется маленький терм"""
        same = False
        for i in range(len(reduce_parts)):
            if self.compare_two_terms(reduce_parts[index], reduce_parts[i]) and index != i:
                small_term = []
                for variable in reduce_parts[index]:
                    if variable in reduce_parts[i]:
                        small_term.append(variable)
                    else:
                        small_term.append('-')
                if self.get_vars_count(small_term) == self.get_vars_count(reduce_parts[index]) - 1:
                    if not self.similarity_check(result, small_term):
                        result.append(small_term)
                    same = True
        if not same and not self.similarity_check(single_parts, reduce_parts[index]):
            single_parts.append(reduce_parts[index])

    @staticmethod
    def compare_two_terms(term_1, term_2):
        count = 0
        for i in range(len(term_1)):
            if term_1[i] == term_2[i]:
                pass
            elif not (term_1[i] in term_2[i] or term_2[i] in term_1[i]):
                return False
            else:
                count += 1
                if count > 1:
                    return False
        return True

    def build_mcklasky_table(self, sdnf_or_sknf):
        """Создание таблицы мак-класки"""

        mcklasky_table = []
        small_terms = self.get_small_terms(sdnf_or_sknf)
        full_terms = list(map(lambda x: x[:], sdnf_or_sknf))
        for i in small_terms:
            small_term_in_full_term = []
            for j in full_terms:
                small_term_in_full_term.append(self.include_check(i, j))
            mcklasky_table.append(small_term_in_full_term)
        return mcklasky_table

    @staticmethod
    def ged_minimized_terms(terms):
        minimized_terms = []
        for term in terms:
            if term not in minimized_terms:
                minimized_terms.append(term)
        return minimized_terms

    def solution(self, sdnf_or_sknf):
        final_terms = []
        table = self.build_mcklasky_table(sdnf_or_sknf)
        list_of_small_terms = self.get_small_terms(sdnf_or_sknf)
        for i in range(len(table[0])):
            truth_count = 0
            index_of_truth = 0
            for j in range(len(table)):
                if table[j][i]:
                    truth_count += 1
                    index_of_truth = j
            if truth_count == 1 and not self.similarity_check(final_terms, list_of_small_terms[index_of_truth]):
                final_terms.append([list_of_small_terms[index_of_truth]])
        return self.ged_minimized_terms(final_terms)

    def get_sdnf_answer(self, sdnf, pr=True):
        terms = self.solution(sdnf)
        answer = ""
        for i in range(len(terms)):
            part = ""
            for j in range(len(terms[i])):
                part = ' * '.join(filter(lambda el: el != '-', terms[i][j]))
            answer += part
            if i != len(terms) - 1:
                answer += " + "
        if pr:
            print(f'Borrow minimized dnf: {answer}')

        terms = list(map(lambda term: term[0], terms))
        return terms

    def get_sknf_answer(self, sknf):
        terms = self.solution(sknf)
        answer = ""
        for i in range(len(terms)):
            result = "("
            part = ""
            for j in range(len(terms[i])):
                part = '+'.join(filter(lambda el: el != '-', terms[i][j]))
            result += part
            result += ")"
            answer += result
            if i != len(terms) - 1:
                answer += " * "
        return answer


class AnotherOperations:

    @staticmethod
    def show_sdnf_form(table, answers, variables, show=True):
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
        if show:
            print(f'Borrow PDNF: {answer}')
        return sdnf

    @staticmethod
    def show_table(table: list, borrows, differences, variables):
        print("Truth table")
        print(' '.join(variables))
        for i in range(len(table)):
            column = (len(variables[i % 3]) * ' ').join(list(map(str, table[i])))
            print(f'{column}   {str(borrows[i])} {str(differences[i])}')

    @staticmethod
    def print_table(x_table, y_table):
        print('x1  x2  x3  x4  y1  y2  y3  y4')
        for i in range(10):
            x_str = '   '.join(list(map(str, x_table[i])))
            y_str = '   '.join(list(map(str, y_table[i])))
            print(x_str + '   ' + y_str)

        for i in range(10, 16):
            x_str = '   '.join(list(map(str, x_table[i])))
            print(x_str, '  -   -   -   -')

    @staticmethod
    def get_additional_y_part():
        bits = [0, 1]
        table = [[a, b, c, d, e, f] for a in bits for b in bits for c in bits for d in bits for e in bits for f in bits]
        return table

    @staticmethod
    def lab4(table, borrows, differences, x_table, y_table, y_table_for_showing):
        AnotherOperations.show_table(table, borrows, differences, ['x1', 'x2', 'Bi', ' B', 'D'])
        sdnf = AnotherOperations.show_sdnf_form(table, borrows, ['x1', 'x2', 'Bi'])
        McCluskyMethod().get_sdnf_answer(sdnf)

        sdnf = AnotherOperations.show_sdnf_form(table, differences, ['x1', 'x2', 'Bi'])
        McCluskyMethod().get_sdnf_answer(sdnf)

        print('----------------------------------------------------------------')

        AnotherOperations.print_table(x_table, y_table_for_showing)

        full_y_table = []
        for i in y_table:
            full_y = list(map(lambda x: [*i, *x], AnotherOperations.get_additional_y_part()))
            full_y_table.append(full_y)

        # print(full_y_table)

        # full_sdnf_list = [
        #     list(
        #     map(lambda y: AnotherOperations.show_sdnf_form(x_table, y, ['x1', 'x2', 'x3', 'x4', 'y1'], False),
        #         y_table)) for y_table in full_y_table
        # ]

        full_sdnf_list = []

        for y_table in full_y_table:
            sndf_list = list(
                map(lambda y: AnotherOperations.show_sdnf_form(x_table, y, ['x1', 'x2', 'x3', 'x4', 'y1'], False),
                    y_table))
            full_sdnf_list.append(sndf_list)


        sdnf_list = [AnotherOperations.show_sdnf_form(x_table, i, ['x1', 'x2', 'x3', 'x4', 'y1'], False) for i in
                     y_table]

        print(sdnf_list)
        McCluskyMethod().get_sdnf_answer(sdnf_list[0])
        McCluskyMethod().get_sdnf_answer(sdnf_list[1])
        McCluskyMethod().get_sdnf_answer(sdnf_list[2])
        McCluskyMethod().get_sdnf_answer(sdnf_list[3])

        # full_list_of_minimized_functions = [
        #     list(map(lambda x: McCluskyMethod().get_sdnf_answer(x, pr=False), list_of_sdnf)) for
        #     list_of_sdnf in full_sdnf_list]
        #
        # full_list_of_minimized_functions = list(
        #     map(lambda list_of_minimized_functions: sorted(list_of_minimized_functions, key=len),
        #         full_list_of_minimized_functions))
        #
        # minimal_sizes = list(map(lambda sizes: len(sizes[0]), full_list_of_minimized_functions))
        # for i in range(len(full_list_of_minimized_functions)):
        #     full_list_of_minimized_functions[i] = list(
        #         filter(lambda x: len(x) == minimal_sizes[i], full_list_of_minimized_functions[i]))
        #
        # # full_list_of_minimized_functions = list(map(lambda x: list(filter())))
        #
        # full_list_of_minimized_functions


AnotherOperations.lab4(table, borrows, differences, x_table, y_table, y_table_for_showing)
