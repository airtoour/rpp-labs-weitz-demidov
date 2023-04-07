# Задача 3.1

# п.1
import sys

# Считываем массив из параметров командной строки:
print("Введите число: ")
x = int(input())
y = int(input())
z = int(input())
a = int(input())
b = int(input())

arr_list = []
arr_list = list()

arr_list.append(x)
arr_list.append(y)
arr_list.append(z)
arr_list.append(a)
arr_list.append(b)

# п.2
# Находим максимальный элемент в массиве:
max_elem = max(range(1, 6)) #max_elem - переменная с макимальным числом из массива

# п.3
# Выводим массив в обратном порядке:
print("Массив в обратном порядке:")
for i in range(len(arr_list)-1, -1, -1):
    print(arr_list[i], end=" ")

# п.4
# Вычисляем среднее арифметическое всех элементов:
sum = 0
count = 0
for elem in arr_list:
    if elem != 0:
        sum = sum + elem
        count = count + 1
    if count > 0:
        avg_elem = sum / count
    else:
        avg_elem = 0

# Заменяем все нулевые элементы на среднее арифметическое
print("Массив после замены нулевых элементов на среднее арифметическое:")
for i in range(len(arr_list)):
    if arr_list[i] == 0:
        arr_list[i] = round(avg_elem)

# Выводим массив после замены нулевых элементов
for elem in arr_list:
    print(elem, end=" ")