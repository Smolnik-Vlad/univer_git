import sys


class BinaryMethods:
    num_31 = 31
    num_32 = 32
    num_127 = 127
    num_23 = 23
    num_24 = 24
    binary_127_long = '00000000000000000000000001111111'

    @classmethod
    def get_positive_binary(cls, decimal_num: int) -> str:
        binary_num = ""
        # генерируем двоичное представление числа в обычном коде
        while decimal_num > 0:
            remainder = decimal_num % 2
            binary_num = str(remainder) + binary_num
            decimal_num = decimal_num // 2
        binary_num = binary_num.rjust(cls.num_32, "0")  # дополнение строки до 32 битов
        return binary_num

    @staticmethod
    def get_negative_binary(decimal_num: str) -> str:
        inverted_bits = ''.join(['1' if bit == '0' else '0' for bit in decimal_num])

        # Add 1 to the inverted bits to get the two's complement
        carry = True
        two_complement_bits = ''
        for bit in reversed(inverted_bits):
            if bit == '1' and carry:
                two_complement_bits += '0'
            elif bit == '0' and carry:
                two_complement_bits += '1'
                carry = False
            else:
                two_complement_bits += bit
        return two_complement_bits[::-1]

    @staticmethod
    def from_decimal_to_binary(decimal_num: int) -> str:
        if decimal_num >= 0:
            # If the decimal number is positive, return its positive binary representation
            return BinaryMethods.get_positive_binary(decimal_num)
        else:
            # Convert the absolute value of the decimal number to binary and pad with leading zeros
            abs_num_bits: str = BinaryMethods.get_positive_binary(abs(decimal_num))

            # Invert all bits

            return BinaryMethods.get_negative_binary(abs_num_bits)

    @staticmethod
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

    @classmethod
    def add_binary(cls, a_bits: list, b_bits: list) -> str:
        # Приведение чисел к 32-битному двоичному формату дополнительного кода

        a_bits: list = ['0' for _ in range(cls.num_32 - len(a_bits))] + a_bits
        b_bits: list = ['0' for _ in range(cls.num_32 - len(b_bits))] + b_bits

        add_binary_result = ""
        carry = 0

        # складывание двух чисел
        for i in range(cls.num_31, -1, -1):
            bit_sum = int(a_bits[i]) + int(b_bits[i]) + carry

            # обработка переноса
            if bit_sum >= 2:
                carry = 1
            else:
                carry = 0

            # добавление бита суммы в результат
            add_binary_result = str(bit_sum % 2) + add_binary_result

        return add_binary_result

    @staticmethod
    def add_decimal(a: int, b: int) -> int:
        """
        enter 2 decimal numbers and add them together
        """
        a_bits = list(BinaryMethods.from_decimal_to_binary(a))
        b_bits = list(BinaryMethods.from_decimal_to_binary(b))
        add_decimal_result: str = BinaryMethods.add_binary(a_bits, b_bits)
        return BinaryMethods.from_binary_to_decimal(add_decimal_result)

    @staticmethod
    def calculate_expression(expression: str):
        first_number, operator, second_number = expression.split()
        first_number = int(first_number)
        second_number = int(second_number)
        if operator == '-':
            second_number = -second_number
        return BinaryMethods.add_decimal(first_number, second_number)

    @classmethod
    def positive_multiplication_of_numbers(cls, a: int, b: int) -> int:
        positive_multiplication_result = '0' * cls.num_32
        a_binary: str = BinaryMethods.from_decimal_to_binary(a)
        b_binary: str = BinaryMethods.from_decimal_to_binary(b)
        for i in range(cls.num_31, -1, -1):
            positive_multiplication_result = list(positive_multiplication_result)
            # Если текущий бит второго числа равен 1, прибавляем к результату первое число, сдвинутое на i позиций
            if b_binary[i] == '1':
                # Сдвигаем первое число на i позиций влево, добавляя i нулей в конец
                shifted_a = list(a_binary[(cls.num_31 - i):] + '0' * (cls.num_31 - i))
                # Добавляем сдвинутое число к результату
                positive_multiplication_result = BinaryMethods.add_binary(positive_multiplication_result, shifted_a)
            # Возвращаем результат, обрезанный до 32 бит
        res_str = ''.join(positive_multiplication_result)
        return int(res_str[-cls.num_32:], 2)

    @staticmethod
    def multiplication_of_numbers(a: int, b: int) -> int:
        multiplication_result = BinaryMethods.positive_multiplication_of_numbers(abs(a), abs(b))

        return multiplication_result if ((a > 0 and b > 0) or (a < 0 and b < 0)) else -multiplication_result

    @classmethod
    def divide_bin(cls, a: str, b: str):
        # Проверка на нулевое значение b
        if len(set(b)) == 1 and b[0] == '0':
            raise ZeroDivisionError("division by zero")

        # Проверка на равенство a и b
        if a == b:
            return cls.num_31 * '0' + '1'

        remainder = ''
        divide_bin_result = ''

        for i in range(len(a)):
            current = remainder + a[i]

            # Если текущее значение меньше b, добавляем следующий бит и переходим к следующей цифре
            if int(current) < int(b):
                remainder = current
                divide_bin_result += '0'
                continue

            # Иначе, вычитаем b из текущего значения и добавляем единицу к результату
            # remainder = bin(int(current) - int(b, 2))[2:].zfill(32)
            remainder = str(int(BinaryMethods.add_binary(list(current.zfill(32)),
                                                         list(BinaryMethods.get_negative_binary(b.zfill(32))))))
            divide_bin_result += '1'

        return divide_bin_result.zfill(32)

    @staticmethod
    def divide_dec(a: int, b: int):
        divide_dec_result = BinaryMethods.divide_bin(BinaryMethods.from_decimal_to_binary(abs(a)),
                                                     BinaryMethods.from_decimal_to_binary(abs(b)))

        divide_dec_result = BinaryMethods.from_binary_to_decimal(divide_dec_result)
        return divide_dec_result if (a > 0 and b > 0) or (a < 0 and b < 0) else -divide_dec_result

    @classmethod
    def from_fraction_to_bin(cls, decimal_part: str):
        decimal_part = float(f'0.{decimal_part}')
        from_fraction_to_bin_result = ""
        while decimal_part != 0 and len(from_fraction_to_bin_result) < cls.num_127:
            decimal_part *= 2
            if decimal_part >= 1:
                from_fraction_to_bin_result += "1"
                decimal_part -= 1
            else:
                from_fraction_to_bin_result += "0"
        return from_fraction_to_bin_result if from_fraction_to_bin_result != "" else "0"

    @classmethod
    def find_shift_order(cls, binary_int: str, binary_fractional: str) -> str:  # сдвиг считаем
        if binary_int != '0':
            exponent = len(str(int(binary_int))) - 1
        else:
            fractional = binary_fractional
            exponent = ...
            for i in range(len(fractional)):
                if fractional[i] != '0':
                    exponent = i
                    break

            exponent = -exponent - 1

        shift_order = BinaryMethods.from_decimal_to_binary(BinaryMethods.add_decimal(cls.num_127, exponent))
        return shift_order

    @classmethod
    def from_decimal_to_float(cls, decimal_num: float) -> str:
        """
        Перевод полноценного числа в бинарное число с мантиссой
        """
        # from_decimal_to_float_result = ''
        from_decimal_to_float_result = '0' if decimal_num >= 0 else '1'

        int_number = BinaryMethods.from_decimal_to_binary(abs(int(decimal_num)))
        int_number = int_number[int_number.find('1'):]

        fractional_number = BinaryMethods.from_fraction_to_bin(
            str(decimal_num)[str(decimal_num).find('.') + 1:])

        if int_number == '0' and fractional_number == '0':
            return '0' * cls.num_32

        shift_order = BinaryMethods.find_shift_order(int_number, fractional_number)[cls.num_24:]
        from_decimal_to_float_result = from_decimal_to_float_result + ' ' + shift_order

        mantissa = str(int(int_number + fractional_number))[1:cls.num_24]
        mantissa = mantissa.ljust(cls.num_23, '0')
        from_decimal_to_float_result = from_decimal_to_float_result + ' ' + mantissa
        return from_decimal_to_float_result

    @staticmethod
    def from_binary_remainder_to_decimal(binary_remainder):
        """
        Перевод дробной части бинарного числа в дробную часть 10го числа
        """
        decimal_remainder = 0
        for i in range(len(binary_remainder)):
            if binary_remainder[i] == '1':
                decimal_remainder += 2 ** (-i - 1)
        return decimal_remainder

    @classmethod
    def from_float_to_decimal(cls, float_num: str) -> float:
        float_num = float_num.replace(' ', '')

        if float_num == cls.num_23 * '0':
            return 0.0

        shift = float_num[1:9]
        shift = -BinaryMethods.from_binary_to_decimal(BinaryMethods.add_binary(list(cls.binary_127_long),
                                                                               list(BinaryMethods.get_negative_binary(
                                                                                   shift.rjust(cls.num_32, '0')))))

        if shift > 0:
            whole_part = '1' + float_num[9:][:shift]
            fractional_part = float_num[9:][abs(shift):]
        elif shift < 0:
            whole_part = '0'
            fractional_part = '0' * (abs(shift) - 1) + '1' + float_num[9:]
        else:
            whole_part = '1'
            fractional_part = float_num[9:]

        from_float_to_decimal_result = float(
            str(BinaryMethods.from_binary_to_decimal(whole_part.rjust(cls.num_32, '0'))) + str(
                BinaryMethods.from_binary_remainder_to_decimal(fractional_part))[1:])

        return from_float_to_decimal_result if float_num[0] == '0' else -from_float_to_decimal_result

    @classmethod
    def search_of_initial_arguments(cls, numb_1: str, numb_2: str):

        sign1 = numb_1[0]
        sign2 = numb_2[0]

        # Здесь работа со сдвигом
        exp1 = -BinaryMethods.from_binary_to_decimal(BinaryMethods.add_binary(list(cls.binary_127_long),
                                                                              list(BinaryMethods.get_negative_binary(
                                                                                  numb_1[1:9].rjust(cls.num_32, '0')))))
        exp2 = -BinaryMethods.from_binary_to_decimal(BinaryMethods.add_binary(list(cls.binary_127_long),
                                                                              list(BinaryMethods.get_negative_binary(
                                                                                  numb_2[1:9].rjust(cls.num_32, '0')))))

        return sign1, sign2, exp1, exp2

    @staticmethod
    def diff_between_shifts_and_mantissa_additions(numb_1: str, numb_2: str, exp1: int, exp2: int):
        mantissa1 = '1' + numb_1[9:]
        mantissa2 = '1' + numb_2[9:]
        # exp_result = 0
        if int(exp1) > int(exp2):
            diff = BinaryMethods.add_binary(list(str(BinaryMethods.from_decimal_to_binary(exp1))),
                                            list(BinaryMethods.get_negative_binary(
                                                str(BinaryMethods.from_decimal_to_binary(exp2)))))  # exp1 - exp2

            diff_dec = BinaryMethods.from_binary_to_decimal(diff)
            mantissa2 = '0' * diff_dec + mantissa2[:-diff_dec]
            exp_result = exp1
        elif int(exp1) < int(exp2):
            diff = BinaryMethods.add_binary(list(str(BinaryMethods.from_decimal_to_binary(exp2))),
                                            list(BinaryMethods.get_negative_binary(
                                                str(BinaryMethods.from_decimal_to_binary(exp1)))))  # exp2 - exp1
            diff_dec = BinaryMethods.from_binary_to_decimal(diff)
            mantissa1 = '0' * diff_dec + mantissa1[:-diff_dec]
            exp_result = exp2

        else:
            exp_result = exp1

        return mantissa1, mantissa2, exp_result

    @classmethod
    def mantissa_addition(cls, sign1: str, sign2: str, mantissa1: str, mantissa2: str, exp_result: int):
        # mantissa_sum = ''
        if sign1 == sign2:
            mantissa_sum = BinaryMethods.add_binary(list(mantissa1.rjust(cls.num_32, '0')),
                                                    list(mantissa2.rjust(cls.num_32, '0')))

        elif int(mantissa1) > int(mantissa2):
            mantissa_sum = BinaryMethods.add_binary(list(mantissa1.rjust(cls.num_32, '0')),
                                                    list(BinaryMethods.get_negative_binary(
                                                        mantissa2.rjust(cls.num_32, '0'))))
        elif int(mantissa1) < int(mantissa2):
            mantissa_sum = BinaryMethods.add_binary(list(mantissa2.rjust(cls.num_32, '0')),
                                                    list(BinaryMethods.get_negative_binary(
                                                        mantissa1.rjust(cls.num_32, '0'))))

        else:
            # mantissa_sum = '0' * 23
            return '0' * cls.num_32, ...

        mantissa_sum = mantissa_sum[mantissa_sum.find(
            '1'):]  # [:24] #здесь может быть проблема в том, что по какой-то причине размер мантиссы 24
        addition_shift = len(mantissa_sum) - cls.num_24  # проверить, может ли быть отрицательным
        if addition_shift < 0:
            mantissa_sum += '0' * abs(addition_shift)

        mantissa_sum = mantissa_sum[:cls.num_24]
        exp_result = exp_result + addition_shift

        return mantissa_sum, exp_result
        # print(len(mantissa_sum))

    @staticmethod
    def define_sign(sign1: str, sign2: str, exp1: int, exp2: int, mantissa1: str, mantissa2: str):
        if sign1 == sign2:
            result_sign = sign1
        else:
            if exp1 > exp2:
                result_sign = sign1
            elif exp1 < exp2:
                result_sign = sign2
            else:
                result_sign = sign2 if int(mantissa1) < int(mantissa2) else sign1
        return result_sign

    @classmethod
    def binary_float_addition(cls, numb_1: str, numb_2: str) -> str:
        numb_1 = numb_1.replace(' ', '')
        numb_2 = numb_2.replace(' ', '')

        if int(numb_1) == 0 and int(numb_2) == 0:
            return '0' * cls.num_32

        sign1, sign2, exp1, exp2 = BinaryMethods.search_of_initial_arguments(numb_1, numb_2)

        mantissa1, mantissa2, exp_result = BinaryMethods.diff_between_shifts_and_mantissa_additions(numb_1, numb_2,
                                                                                                    exp1, exp2)
        mantissa_sum, exp_result = BinaryMethods.mantissa_addition(sign1, sign2, mantissa1, mantissa2, exp_result)

        if int(mantissa_sum) == 0:
            return '0' * cls.num_32

        # определение знака
        result_sign = BinaryMethods.define_sign(sign1, sign2, exp1, exp2, mantissa1, mantissa2)

        shift_result = BinaryMethods.add_binary(list(BinaryMethods.from_decimal_to_binary(exp_result)),
                                                list('01111111'))  # итоговое значение сдвига

        result_mantissa = mantissa_sum[1:]  # и вот тут по какой-то причине урезается первый элемент

        result = result_sign + shift_result[-8:] + result_mantissa
        return result

    @staticmethod
    def binary_float_addition2(float1: float, float2: float) -> float:
        number1 = BinaryMethods.from_decimal_to_float(float1)
        number2 = BinaryMethods.from_decimal_to_float(float2)
        result = BinaryMethods.binary_float_addition(number1, number2)
        return BinaryMethods.from_float_to_decimal(result)


class Checker:

    @staticmethod
    def check_hardcoded_expression():
        print(f'Сумма двух чисел: {BinaryMethods.add_decimal(-10, 5)}')

        expression = '0 - 0'
        print(f'Решение выражения: {BinaryMethods.calculate_expression(expression)}')

        print(f'Произведение двух чисел: {BinaryMethods.multiplication_of_numbers(10, 5)}')

        print(f'Деление двух чисел: {BinaryMethods.divide_dec(10, -1)}')

        print(f'Сумма двух чисел с плавающей точкой: {BinaryMethods.binary_float_addition2(-16.387, 4.0)}')

    @staticmethod
    def execute_request():
        function: str = sys.argv[1]
        value = sys.argv[2:]

        list_of_functions = {'--expression': BinaryMethods.calculate_expression,
                             '--mult': BinaryMethods.multiplication_of_numbers,
                             '--div': BinaryMethods.divide_dec,
                             '--float_sum': BinaryMethods.binary_float_addition2,
                             '--get_float': BinaryMethods.from_decimal_to_float,
                             '--get_decimal_from_float': BinaryMethods.from_float_to_decimal,
                             '--get_binary_from_decimal': BinaryMethods.from_decimal_to_binary,
                             '--get_decimal_from_binary': BinaryMethods.from_binary_to_decimal,
                             }

        try:
            get_function = list_of_functions[function]

            if function in ['--expression', '--get_decimal_from_float', '--get_decimal_from_binary']:
                data = value

            elif function in ['--float_sum', '--get_float']:
                data = list(map(float, value))

            else:
                data = list(map(int, value))

            print(get_function(*data))

        except KeyError:
            return f'Неизвестная функция {function}'


Checker.check_hardcoded_expression()

# Checker.check_hardcoded_expression()
