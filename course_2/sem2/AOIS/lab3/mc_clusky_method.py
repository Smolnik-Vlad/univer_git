class McCluskyMethod:

    def __get_small_terms(self, sdnf_sknf):
        sdnf_sknf = list(map(lambda x: x[:], sdnf_sknf))
        single_parts = []
        while self.__get_vars_count(sdnf_sknf[0]) > 1:
            reduced_elements = []
            for i in range(len(sdnf_sknf)):
                self.__check(i, reduced_elements, sdnf_sknf, single_parts)
            sdnf_sknf = reduced_elements
            if len(reduced_elements) == 0:
                break

        small_terms = []
        for i in range(len(sdnf_sknf)):
            if not self.__similarity_check(small_terms, sdnf_sknf[i]):
                small_terms.append(sdnf_sknf[i])
        for i in range(len(single_parts)):
            small_terms.append(single_parts[i])
        return small_terms

    @staticmethod
    def __get_vars_count(term):
        """Подсчет количества переменных"""
        sch = 0
        for variable in term:
            if variable != "-":
                sch += 1
        return sch

    @staticmethod
    def __similarity_check(res, sdnf_func_part):
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
    def __include_check(small_term, full_terms):
        for i in range(len(full_terms)):
            if small_term[i] != full_terms[i] and small_term[i] != '-':
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
                    if not self.__similarity_check(result, small_term):
                        result.append(small_term)
                    same = True
        if not same and not self.__similarity_check(single_parts, reduce_parts[index]):
            single_parts.append(reduce_parts[index])


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

    def __build_mcklasky_table(self, sdnf_or_sknf):
        """Создание таблицы мак-класки"""

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
    def __ged_minimized_terms(terms):
        minimized_terms = []
        for term in terms:
            if term not in minimized_terms:
                minimized_terms.append(term)
        return minimized_terms

    def solution(self, sdnf_or_sknf):
        final_terms = []
        table = self.__build_mcklasky_table(sdnf_or_sknf)
        list_of_small_terms = self.__get_small_terms(sdnf_or_sknf)
        for i in range(len(table[0])):
            truth_count = 0
            index_of_truth = 0
            for j in range(len(table)):
                if table[j][i]:
                    truth_count += 1
                    index_of_truth = j
            if truth_count == 1 and not self.__similarity_check(final_terms, list_of_small_terms[index_of_truth]):
                final_terms.append([list_of_small_terms[index_of_truth]])
        return self.__ged_minimized_terms(final_terms)



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
