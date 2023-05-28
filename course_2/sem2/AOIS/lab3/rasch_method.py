class RaschMethod:

    @staticmethod
    def __find_rasch_results(res, sdnf_func_part):
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
    def __compare_two_terms(term_1, term_2):
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

    def __check(self, index, result, reduce_parts, single_parts):
        """Формируется маленький терм"""
        same = False
        for i in range(len(reduce_parts)):
            if self.__compare_two_terms(reduce_parts[index], reduce_parts[i]) and index != i:
                small_term = []
                for variable in reduce_parts[index]:
                    if variable in reduce_parts[i]:
                        small_term.append(variable)
                    else:
                        small_term.append('-')
                if self.__get_vars_count(small_term) == self.__get_vars_count(reduce_parts[index]) - 1:
                    if not self.__find_rasch_results(result, small_term):
                        result.append(small_term)
                    same = True
        if not same and not self.__find_rasch_results(single_parts, reduce_parts[index]):
            single_parts.append(reduce_parts[index])

    @staticmethod
    def __include_check(small_term, full_terms):
        for i in range(len(full_terms)):
            if small_term[i] != full_terms[i] and small_term[i] != '-':
                return False
        return True

    @staticmethod
    def __get_vars_count(term):
        """Подсчет количества переменных"""
        sch = 0
        for variable in term:
            if variable != "-":
                sch += 1
        return sch

    def __get_small_terms(self, sdnf_sknf):
        sdnf_sknf = list(map(lambda x: x[:], sdnf_sknf))
        single_parts = []
        while self.__get_vars_count(sdnf_sknf[0]) > 1:
            # Здесь проходим все время по sdnf_sknf до того момента, пока не сократим до самого конца
            reduced_elements = []
            for i in range(len(sdnf_sknf)):
                self.__check(i, reduced_elements, sdnf_sknf, single_parts)
            sdnf_sknf = reduced_elements
            if len(reduced_elements) == 0:
                break

        small_terms = []
        for i in range(len(sdnf_sknf)):
            if not self.__find_rasch_results(small_terms, sdnf_sknf[i]):
                small_terms.append(sdnf_sknf[i])
        for i in range(len(single_parts)):
            small_terms.append(single_parts[i])
        return small_terms

    def __get_resolve_table(self, sdnf_or_sknf):

        mcklasky_table = []
        small_terms = self.__get_small_terms(sdnf_or_sknf)
        full_terms = list(map(lambda x: x[:], sdnf_or_sknf))
        for i in small_terms:
            small_term_in_full_term = []
            for j in full_terms:
                small_term_in_full_term.append(self.__include_check(i, j))
            mcklasky_table.append(small_term_in_full_term)
        return mcklasky_table

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
    def get_vars_count(term):
        """Подсчет количества переменных"""
        sch = 0
        for variable in term:
            if variable != "-":
                sch += 1
        return sch

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

    def generate_covered_terms(self, terms):
        covered_terms = set()
        num_vars = len(terms[0])
        for term in terms:
            for i in range(num_vars):
                if term[i] != '-':
                    new_term = term.copy()
                    new_term[i] = '-'
                    covered_terms.add(tuple(new_term))
        return covered_terms

    def find_dead_ends(self, terms):
        dead_ends = set()
        covered_terms = self.generate_covered_terms(terms)

        for term in terms:
            if tuple(term) not in covered_terms:
                dead_ends.add(tuple(term))

        return dead_ends


    @staticmethod
    def __ged_minimized_terms(terms):
        minimized_terms = []
        for term in terms:
            if term not in minimized_terms:
                minimized_terms.append(term)
        return minimized_terms

    def compare_and_build_minimized_terms(self, terms):
        self.min_terms_names_for = []
        try:
            for term in terms:
                for j in term:
                    if j == '-':
                        self.min_terms_names_for.append(term)
                    else:
                        continue

        except:
            return

    def get_sdnf_answer(self, sdnf):
        terms = self.solution(sdnf)
        answer = ""
        for i in range(len(terms)):
            part = ""
            for j in range(len(terms[i])):
                part = '*'.join(filter(lambda el: el != '-', terms[i][j]))
            answer += part
            if i != len(terms) - 1:
                answer += " + "
        return answer

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

    def get_result_by_rashch_method(self, table, final_terms, list_of_small_terms):
        for i in range(len(table[0])):
            truth_count = 0
            index_of_truth = 0
            for j in range(len(table)):
                if table[j][i]:
                    truth_count += 1
                    index_of_truth = j
            if truth_count == 1 and not self.__find_rasch_results(final_terms, list_of_small_terms[index_of_truth]):
                final_terms.append([list_of_small_terms[index_of_truth]])
        return self.__ged_minimized_terms(final_terms)

    def prepearing(self, sdnf_sknf):
        final_terms = []
        small_terms = self.get_small_terms(sdnf_sknf)
        table = self.__get_resolve_table(sdnf_sknf)
        list_of_small_terms = self.__get_small_terms(sdnf_sknf)
        return small_terms, table, final_terms, list_of_small_terms

    def solution(self, sdnf_sknf):

        small_terms, table, final_terms, list_of_small_terms = self.prepearing(sdnf_sknf)
        self.find_dead_ends(small_terms)
        self.generate_covered_terms(small_terms)
        return self.get_result_by_rashch_method(table, final_terms, list_of_small_terms)


# a = RaschMethod()
# sdnf = a.solution([['!x1', '!x2', 'x3'], ['!x1', 'x2', '!x3'], ['!x1', 'x2', 'x3'], ['x1', 'x2', '!x3']])
# print(sdnf)
# c = a.get_sdnf_answer([['!x1', '!x2', 'x3'], ['!x1', 'x2', '!x3'], ['!x1', 'x2', 'x3'], ['x1', 'x2', '!x3']])
# print('sDNF:', c)
# d = a.get_sknf_answer([['x1', 'x2', 'x3'], ['!x1', 'x2', 'x3'], ['!x1', 'x2', '!x3'], ['!x1', '!x2', '!x3']])
# print('sKNF: ', d)
