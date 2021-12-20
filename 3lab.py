import pickle
import json
from tqdm import tqdm
from valid import Validator
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('path', help='The path to the file folder')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-u', '-union', help='Performs all functions')
group.add_argument('-valid', '--validate', help='Get valid data and write it to a file')
group.add_argument('-pickle', '--pickled', help='Get sorted data and write it to file (pickle)')
group.add_argument('-check', '--checker', help='Output of random sequence elements to the screen.')
args = parser.parse_args()

path_in_ = args.path + "\\Данил\\PycharmProjects\\lab3\\95.txt"
path_out_ = args.path + "\\Данил\\PycharmProjects\\lab3\\valid.txt"
path_fin_ = args.path + "\\Данил\\PycharmProjects\\lab3\\out.txt"

"""
Сортировка вставками
"""


def insertion_sort(data, param):
    for i in range(1, len(data)):
        temp = data[i]
        while i - 1 >= 0 and temp[param] < data[i - 1][param]:
            data[i] = data[i - 1]
            i -= 1
            data[i] = temp


"""
Поиск максимального значения в словаре
"""


def max_value_in_data(data: object, param: str):
    numbers = []
    for el in data:
        numbers.append(int(el[param]))
    return max(numbers)


"""
Сортировка по сегменту
"""


def bucket(data, param):
    new_data = []
    tmp = max_value_in_data(data, param)
    for _ in range(len(data)):
        new_data.append([])
    for i in range(len(data)):
        number = int(data[i][param] / (tmp/len(data)))
        new_data[number].append(data[i]) if number != len(data) else new_data[len(data) - 1].append(data[i])
    for z in range(len(new_data)):
        insertion_sort(new_data[z], param)
        result = []
    for x in range(len(new_data)):
        result += new_data[x]
        return result

"""
Валидация файла
"""

def val(path_in, path_out) -> None:
    data = json.load(open(path_in_, encoding='windows-1251'))

    true_data = list()
    email = 0
    height = 0
    passport = 0
    address = 0
    age = 0
    inn = 0
    occupation = 0
    worldview = 0
    political_view = 0
    with tqdm(total=len(data)) as progressbar:
        for person in data:
            temp = True
            if not Validator.check_email(person['email']):
                email += 1
                temp = False
            if not Validator.check_height(person['height']):
                height += 1
                temp = False
            if not Validator.check_inn(person['inn']):
                inn += 1
                temp = False
            if not Validator.check_passport(person['passport_number']):
                passport += 1
                temp = False
            if not Validator.check_address(person["address"]):
                address += 1
                temp = False
            if not Validator.check_type_int(person['age']):
                age += 1
                temp = False
            if not Validator.check_type_string(person['occupation']):
                occupation += 1
                temp = False
            if not Validator.check_type_string(person['political_views']):
                political_view += 1
                temp = False
            if not Validator.check_type_string(person['worldview']):
                worldview += 1
                temp = False
            if temp:
                true_data.append(person)
            progressbar.update(1)

    out_put = open(path_out_, 'w', encoding='utf-8')
    valid_data = json.dumps(true_data, ensure_ascii=False, indent=4)
    out_put.write(valid_data)
    out_put.close()

    print(f'Число валидных записей: {len(true_data)}')
    print(f'Число невалидных записей: {len(data) - len(true_data)}')
    print(f'  - Число невалидных email:  {email}')
    print(f'  - Число невалидного роста: {height}')
    print(f'  - Число невалидных ИНН: {inn}')
    print(f'  - Число невалидных номеров паспорта: {passport}')
    print(f'  - Число невалидных профессий: {occupation}')
    print(f'  - Число невалидных возрастов: {age}')
    print(f'  - Число невалидных политических взглядов: {political_view}')
    print(f'  - Число невалидных мировоззрений: {worldview}')
    print(f'  - Число невалидных адресов: {address}')
    pass


def bucket_sort(path_out_, path_fin_):
    sort_data = json.load(open(path_out_, encoding='UTF-8'))
    print("By which parameter will the sorting take place:\n1.\'height\'\n2.\'inn\'\n3.\'passport_number\'\n4.\'age\'\n")
    choice1 = int(input())
    if choice1 == 1:
        bucket(sort_data, 'height')
    elif choice1 == 2:
        bucket(sort_data, 'inn')
    elif choice1 == 3:
        bucket(sort_data, 'passport_number')
    elif choice1 == 4:
        bucket(sort_data, 'age')
    fin = open(path_fin_, 'wb')
    fin_data = pickle.dumps(sort_data)
    fin.write(fin_data)
    fin.close()
    print("Sorting was successful\n")



def check_data(path_fin) -> None:
    t_put = open(path_fin, 'rb')
    test = pickle.load(t_put)
    print("Sorted data\n")
    print("\n", test[1], "\n", test[2000], "\n", test[4000], "\n", test[6000], "\n", test[8000], "\n")


if args.validate is not None:
    val(path_in_, path_out_)
else:
    if args.pickled is not None:
        bucket_sort(path_out_, path_fin_)
    else:
        if args.checker is not None:
            check_data(path_fin_)
        else:
            if args.u is not None:
                val(path_in_, path_out_)
                bucket_sort(path_out_, path_fin_)
                check_data(path_fin_)





