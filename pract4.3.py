import math

t = int(input())
for _ in range(t):
    n, d = map(int, input().split()) 
    s = input()
    
    # Поиск позиции для вставки
    # Чтобы получить max число, нужно найти первую цифру в числе, которая < d, и вставить d перед этой цифрой. Иначе, если все цифры >= d, то d вставляется в конец
    pos = n  # по умолчанию в конец
    for i in range(n):
        if int(s[i]) < d:
            pos = i
            break
    
    # Вставка цифры в найденную позицию
    print(s[:pos] + str(d) + s[pos:])

#print ("\n ПРОВЕРОЧНЫЙ ТЕСТ ")

#test_cases = [
#    (5, 4, "76543", "765443"),
#    (1, 0, "1", "10"),
#    (2, 5, "44", "544"),
#    (3, 6, "666", "6666"),
#    (5, 6, "13579", "613579"),
#    (5, 8, "97531", "987531"),
#]

#for n, d, s, expected in test_cases:
#    pos = n
#    for i in range(n):
#        if int(s[i]) < d:
#            pos = i
#            break
#    result = s[:pos] + str(d) + s[pos:]
    
#    if result == expected:
#        print(f"{s} + {d} -> {result} +")
#    else:
#        print(f"{s} + {d} -> {result} -, expected {expected}")

