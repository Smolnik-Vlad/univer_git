'''def check_tuple_in_set(sets):
    a = 0
    check = 0
    str_get = ''
    for i in range(len(sets)):
        if(type(sets[i])!=set):   
            if '<' in sets[i]:
                check+=1
                str_get+=sets[i]+', '''''


def check_tuple2(sets):
    tuple_get = sets[0] + ', '
    check = 1
    i = 1  # >' not in sets[i]
    while (check > 0):
        if '<' in sets[i]:
            check += 1
        if '>>' in sets[i]:
            check -= 2
        elif '>' in sets[i]:
            check -= 1
        tuple_get += sets[i] + ', '
        i += 1
    tuple_get = tuple_get[:len(tuple_get) - 2]
    return tuple_get, i


def check_tuple1(sets):
    for i in sets:
        temporary = list()
        j = 0
        while j < len(i):
            if (type(i[j]) != list):
                if ('<' in i[j]):
                    tuple_get, a = check_tuple2(i[j:])
                    for t in range(a):
                        i.pop(j)
                    temporary.append(tuple_get)
                    j -= 1
            '''elif(type(i[j]==list)):
                temporary.append(check_tuple1(i[j]))
                sets.pop(j)
                j-=1'''

            j += 1
        for l in temporary:
            i.append(l)
    return sets


def check_sets(union, set_b):
    if (len(union) != len(set_b)):
        return False

    for i in set_b:
        if type(i) != list:
            if (i not in union):
                return False
        else:
            for j in union:
                if type(j) == list:
                    if (check_sets(j, i)):
                        return True
    return True


def union(sets):
    union = list()

    for i in sets:
        for j in i:
            if (type(j) != list):
                if (j not in union):
                    union.append(j)
            else:
                a = 0
                for i in union:
                    if type(i) == list:
                        a += 1
                check = 0
                for k in union:
                    if (type(k) == list):
                        if (check_sets(k, j)):
                            break
                        check += 1
                if (a == check):
                    union.append(j)
    return union


def get_set(temporary_set):
    rec_set = list()
    while (temporary_set):
        if ('[' in temporary_set[0]):
            temporary_set[0] = temporary_set[0].replace('[', '', 1)
            # temporary_set.sort()
            set_in = get_set(temporary_set)
            # set_in.sort()
            rec_set.append(set_in)
            while (']' not in temporary_set[0]):
                temporary_set.reverse()
                temporary_set.pop()
                temporary_set.reverse()
        elif (']' in temporary_set[0]):
            if (']]' in temporary_set[0]):
                a = temporary_set[0].count(']')
                temporary_set[0] = temporary_set[0].replace(']', '', a)
                if temporary_set[0] != '':
                    rec_set.append(temporary_set[0])
                temporary_set[0] = temporary_set[0] + a * ']'
            elif (temporary_set[0] == ']'):
                return rec_set
            else:
                temporary_set[0] = temporary_set[0].replace(']', '', 1)
                rec_set.append(temporary_set[0])
                temporary_set[0] = temporary_set[0] + ']'
            return rec_set
        else:
            rec_set.append(temporary_set[0])
        if (']]' in temporary_set[0]):  ##рассмотреть случай для больше ]
            check = temporary_set[0].count(']')
        else:
            check = 0
        temporary_set.reverse()
        temporary_set.pop()
        if (check != 0):
            temporary_set.append((check - 1) * ']')
        temporary_set.reverse()

    # rec_set.remove('')
    return rec_set


file = open("file4")
get_str = []

for line in file:
    get_str.append(line.split())
sets = list()

for i in get_str:
    set_i = get_set(i)
    sets.append(set_i)

print(sets)

sets = check_tuple1(sets)

print(sets)
un = union(sets)
print(un)
