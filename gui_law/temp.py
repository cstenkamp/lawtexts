str_list = ["banana", "apple", "nom", "Eeeeeeeeeeek"]
sec_list = [0.123423, 9.231, 23, 10.11001]
temp = sorted(zip(str_list, sec_list), key=lambda x: len(x[0]))
str_list, sec_list = map(list, zip(*temp))
print(str_list)
print(sec_list)