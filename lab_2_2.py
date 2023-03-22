# Задача 2.1

# п.1
# Считываем строку с клавиатуры:
s = input("Введите строку: ")

# п.2
# Задаем переменную для подсчета слов, начинающихся с "m":
count = 0

# Задаем флаг, который будет определять, находимся ли мы внутри слова:
inside_word = False

# Перебираем все символы в строке:
for i in range(len(s)):
    # Если текущий символ является буквой "m" и мы не находимся внутри слова, то увеличиваем счетчик
    if s[i] == "m" and not inside_word:
        count += 1
    # Если текущий символ не является буквой "m" и не является буквой алфавита, то мы находимся вне слова
    if not s[i].isalpha():
        inside_word = False
    # Если текущий символ является буквой алфавита, то мы находимся внутри слова
    elif not inside_word:
        inside_word = True

# Выводим количество слов, начинающихся с "m"
print("Количество слов, начинающихся с буквы 'm':", count)