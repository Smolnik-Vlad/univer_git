class BinaryMethods:

    @staticmethod
    def get_positive_binary(DecimalNum: int) -> str:
        BinaryNum = ""
        # генерируем двоичное представление числа в обычном коде
        while DecimalNum > 0:
            remainder = DecimalNum % 2
            BinaryNum = str(remainder) + BinaryNum
            DecimalNum = DecimalNum // 2
        binary_num = BinaryNum.rjust(32, "0")  # дополнение строки до 32 битов
        return binary_num

    @staticmethod
    def get_negative_binary(DecimalNum: str) -> str:
        inverted_bits = ''.join(['1' if bit == '0' else '0' for bit in DecimalNum])

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

    @staticmethod
    def compare_abs_elements(a, b):
        if a[0] != b[0]:
            if a[0] == '1':
                negative_binary = list(BinaryMethods.get_negative_binary(a))
                return True if negative_binary == a else False

            else:
                negative_binary = list(BinaryMethods.get_negative_binary(a))
                return True if negative_binary == b else False

        return False

    @staticmethod
    def add_binary(a_bits: list, b_bits: list) -> str:
        # Приведение чисел к 32-битному двоичному формату дополнительного кода

        a_bits: list = ['0' for _ in range(32 - len(a_bits))] + a_bits
        b_bits: list = ['0' for _ in range(32 - len(b_bits))] + b_bits

        result = ""
        carry = 0

        # складывание двух чисел
        for i in range(31, -1, -1):
            bit_sum = int(a_bits[i]) + int(b_bits[i]) + carry

            # обработка переноса
            if bit_sum >= 2:
                carry = 1
            else:
                carry = 0

            # добавление бита суммы в результат
            result = str(bit_sum % 2) + result

        return result

    @staticmethod
    def add_decimal(a: int, b: int) -> int:
        """
        enter 2 decimal numbers and add them together
        """
        a_bits = list(BinaryMethods.from_decimal_to_binary(a))
        b_bits = list(BinaryMethods.from_decimal_to_binary(b))
        result: str = BinaryMethods.add_binary(a_bits, b_bits)
        return BinaryMethods.from_binary_to_decimal(result)

    @staticmethod
    def positive_multiplication_of_numbers(a: int, b: int) -> int:
        result = '0' * 32
        a_binary: str = BinaryMethods.from_decimal_to_binary(a)
        b_binary: str = BinaryMethods.from_decimal_to_binary(b)
        for i in range(31, -1, -1):
            result = list(result)
            # Если текущий бит второго числа равен 1, прибавляем к результату первое число, сдвинутое на i позиций
            if b_binary[i] == '1':
                # Сдвигаем первое число на i позиций влево, добавляя i нулей в конец
                shifted_a = list(a_binary[(31 - i):] + '0' * (31 - i))
                a = len(shifted_a)
                # Добавляем сдвинутое число к результату
                result = BinaryMethods.add_binary(result, shifted_a)
            # Возвращаем результат, обрезанный до 32 бит
        res_str = ''.join(result)
        return int(res_str[-32:], 2)

    @staticmethod
    def multiplication_of_numbers(a: int, b: int) -> int:
        result = BinaryMethods.positive_multiplication_of_numbers(abs(a), abs(b))

        return result if ((a > 0 and b > 0) or (a < 0 and b < 0)) else -result

    @staticmethod
    def divide_bin(a: str, b: str):
        # Проверка на нулевое значение b
        if len(set(b)) == 1 and b[0] == '0':
            raise ZeroDivisionError("division by zero")

        # Проверка на равенство a и b
        if a == b:
            return 31 * '0' + '1'

        # # Проверка на a < b
        # if int(a, 2) < int(b, 2):
        #     return '0' + '0' * 5

        # Инициализация остатка и результата
        remainder = ''
        result = ''

        # Пока есть нерасмотренные цифры
        for i in range(len(a)):
            current = remainder + a[i]

            # Если текущее значение меньше b, добавляем следующий бит и переходим к следующей цифре
            if int(current) < int(b):
                remainder = current
                result += '0'
                continue

            # Иначе, вычитаем b из текущего значения и добавляем единицу к результату
            # remainder = bin(int(current) - int(b, 2))[2:].zfill(32)
            remainder = str(int(BinaryMethods.add_binary(list(current.zfill(32)),
                                                         list(BinaryMethods.get_negative_binary(b.zfill(32))))))
            result += '1'

        # Если остаток содержит только нули, возвращаем только результат
        # if int(remainder, 2) == 0:
        #     return result.zfill(32)
        #
        # # Иначе, добиваем результат нулями до нужной точности
        # while len(result) < 32 + 5:
        #     current = remainder + '0'
        #     current_int = int(current, 2)
        #
        #     if current_int < int(b, 2):
        #         remainder = current
        #         result += '0'
        #         continue
        #
        #     remainder = bin(current_int - int(b, 2))[2:].zfill(32)
        #     result += '1'
        #
        # # Возвращаем результат с округлением до 5 знаков после запятой
        # return '{:.5f}'.format(int(result, 2) / (2 ** 5))

        return result.zfill(32)

    @staticmethod
    def divide_dec(a: int, b: int):
        result = BinaryMethods.divide_bin(BinaryMethods.from_decimal_to_binary(abs(a)),
                                          BinaryMethods.from_decimal_to_binary(abs(b)))

        result = BinaryMethods.from_binary_to_decimal(result)
        return result if (a > 0 and b > 0) or (a < 0 and b < 0) else -result

    @staticmethod
    def from_fraction_to_bin(decimal_part: str):
        decimal_part = float(f'0.{decimal_part}')
        result = ""
        while decimal_part != 0 and len(result) < 127:
            decimal_part *= 2
            if decimal_part >= 1:
                result += "1"
                decimal_part -= 1
            else:
                result += "0"
        return result if result != "" else "0"

    @staticmethod
    def find_shift_order(binary_int: str, binary_fractional: str) -> str:  # сдвиг считаем
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

        shift_order = BinaryMethods.from_decimal_to_binary(BinaryMethods.add_decimal(127, exponent))
        return shift_order

    @staticmethod
    def from_decimal_to_float(decimal_num: float) -> str:
        """
        Перевод полноценного числа в бинарное число с мантиссей
        """
        result = ''
        result = '0' if decimal_num >= 0 else '1'

        int_number = BinaryMethods.from_decimal_to_binary(abs(int(decimal_num)))
        int_number = int_number[int_number.find('1'):]

        fractional_number = BinaryMethods.from_fraction_to_bin(
            str(decimal_num)[str(decimal_num).find('.') + 1:])

        if int_number == '0' and fractional_number == '0':
            return '0' * 32

        shift_order = BinaryMethods.find_shift_order(int_number, fractional_number)[24:]
        result = result + ' ' + shift_order

        mantissa = str(int(int_number + fractional_number))[1:24]
        mantissa = mantissa.ljust(23, '0')
        result = result + ' ' + mantissa
        return result

    @staticmethod
    def from_binary_remainder_to_decimal(binary_remainder):
        """
        перевод дробной части бинарного числа в дробную часть 10го числа
        """
        decimal_remainder = 0
        for i in range(len(binary_remainder)):
            if binary_remainder[i] == '1':
                decimal_remainder += 2 ** (-i - 1)
        return decimal_remainder

    @staticmethod
    def from_float_to_decimal(float_num: str) -> float:
        float_num = float_num.replace(' ', '')

        if float_num == 32 * '0':
            return 0.0

        shift = float_num[1:9]
        shift = -BinaryMethods.from_binary_to_decimal(BinaryMethods.add_binary(list('00000000000000000000000001111111'),
                                                                               list(BinaryMethods.get_negative_binary(
                                                                                   shift.rjust(32, '0')))))

        if shift > 0:
            whole_part = '1' + float_num[9:][:shift]
            fractional_part = float_num[9:][abs(shift):]
        elif shift < 0:
            whole_part = '0'
            fractional_part = '0' * (abs(shift) - 1) + '1' + float_num[9:]
        else:
            whole_part = '1'
            fractional_part = float_num[9:]

        result = float(
            str(BinaryMethods.from_binary_to_decimal(whole_part.rjust(32, '0'))) + str(
                BinaryMethods.from_binary_remainder_to_decimal(fractional_part))[1:])

        return result if float_num[0] == '0' else -result

    @staticmethod
    def search_of_initial_arguments(numb_1: str, numb_2: str):

        sign1 = numb_1[0]
        sign2 = numb_2[0]

        # Здесь работа со сдвигом
        exp1 = -BinaryMethods.from_binary_to_decimal(BinaryMethods.add_binary(list('00000000000000000000000001111111'),
                                                                              list(BinaryMethods.get_negative_binary(
                                                                                  numb_1[1:9].rjust(32, '0')))))
        exp2 = -BinaryMethods.from_binary_to_decimal(BinaryMethods.add_binary(list('00000000000000000000000001111111'),
                                                                              list(BinaryMethods.get_negative_binary(
                                                                                  numb_2[1:9].rjust(32, '0')))))

        return sign1, sign2, exp1, exp2

    @staticmethod
    def diff_between_shifts_and_mantissa_additions(numb_1: str, numb_2: str, exp1: int, exp2: int):
        mantissa1 = '1' + numb_1[9:]
        mantissa2 = '1' + numb_2[9:]
        exp_result = 0
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


    @staticmethod
    def mantissa_addition(sign1: str, sign2: str, mantissa1: str, mantissa2: str, exp_result: int):
        mantissa_sum = ''
        if sign1 == sign2:
            mantissa_sum = BinaryMethods.add_binary(list(mantissa1.rjust(32, '0')), list(mantissa2.rjust(32, '0')))

        elif int(mantissa1) > int(mantissa2):
            mantissa_sum = BinaryMethods.add_binary(list(mantissa1.rjust(32, '0')),
                                                    list(BinaryMethods.get_negative_binary(mantissa2.rjust(32, '0'))))
        elif int(mantissa1) < int(mantissa2):
            mantissa_sum = BinaryMethods.add_binary(list(mantissa2.rjust(32, '0')),
                                                    list(BinaryMethods.get_negative_binary(mantissa1.rjust(32, '0'))))

        else:
            mantissa_sum = '0' * 23
            # может быть опасное место
            return '0' * 32, ...
        # добавить вариант, когда в результате получается 0

        mantissa_sum = mantissa_sum[mantissa_sum.find(
            '1'):]  # [:24] #здесь может быть проблема в том, что по какой-то причине размер мантиссы 24
        addition_shift = len(mantissa_sum) - 24  # проверить, может ли быть отрицательным
        # решить вопрос с моментом, когда мантиса стала на 1 меньше, и тогда нужно и сдвиг уменьшать, и мантису увеличивать
        if addition_shift < 0:
            mantissa_sum += '0' * abs(addition_shift)

        mantissa_sum = mantissa_sum[:24]
        exp_result = exp_result + addition_shift

        return mantissa_sum, exp_result
        # print(len(mantissa_sum))

    @staticmethod
    def binary_float_addition(numb_1: str, numb_2: str) -> str:
        numb_1 = numb_1.replace(' ', '')
        numb_2 = numb_2.replace(' ', '')

        if int(numb_1) == 0 and int(numb_2) == 0:
            return '0' * 32

        sign1, sign2, exp1, exp2 = BinaryMethods.search_of_initial_arguments(numb_1, numb_2)

        mantissa1, mantissa2, exp_result = BinaryMethods.diff_between_shifts_and_mantissa_additions(numb_1, numb_2,
                                                                                                    exp1, exp2)
        mantissa_sum, exp_result = BinaryMethods.mantissa_addition(sign1, sign2, mantissa1, mantissa2, exp_result)

        if int(mantissa_sum) == 0:
            return '0' * 32

        # определение знака
        if sign1 == sign2:
            result_sign = sign1
        else:
            if exp1 > exp2:
                result_sign = sign1
            elif exp1 < exp2:
                result_sign = sign2
            else:
                result_sign = sign2 if int(mantissa1) < int(mantissa2) else sign1

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


#
# print(BinaryMethods.from_decimal_to_binary(127))
# print(BinaryMethods.from_decimal_to_binary(7))
# print(BinaryMethods.add_decimal(-7, 6))
# print(BinaryMethods.divide_bin('00000000000000000000000000011100', "00000000000000000000000000000111"))
# print('decimal: ' + str(BinaryMethods.from_binary_to_decimal('00000000000000000000000001111001')))
# print(BinaryMethods.divide_dec(-35, 7))
#
# print(BinaryMethods.find_shift_order('0', '0101'))
# print('дробная десятичного -> дробная бинарного: ' + BinaryMethods.from_fraction_to_bin('0234657'))

b = BinaryMethods.from_decimal_to_float(0.0)
c = BinaryMethods.from_decimal_to_float(442.5)
print(f'полноценного десятичное -> бинарное мантисса: {b}.........{c}', end='\n\n')

print("float->decimal: " + str(BinaryMethods.from_float_to_decimal('0 00000000 00000000000000000000000')))

num1 = '0 10000000 00101001111110111110011'  # 2.328
num2 = '0 00000000 00000000000000000000000'  #
# num2 = '0 10000111 10111010100000000000000'  # 442.5
result = BinaryMethods.binary_float_addition(num1,
                                             num2)  # проблема со сдвигом (если он одинаков) и с отрицательным числом
print(result)
print(BinaryMethods.from_float_to_decimal(result))  # 12

print(f'add_2: {BinaryMethods.binary_float_addition2(123.45, 45.278)}')

# "Бланки, заполнить фамилии и распечатать в нужном количестве"
# Условие с 0
# 0 10000011 11000011111101111100111
