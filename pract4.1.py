import math

t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))

    # Если в массиве есть 0, увеличиваем его до 1, т.к. это даст max прирост произведения
    if 0 in a:
        a[a.index(0)] = 1
        print(math.prod(a))
    else:
        min_number = min(a)
        a[a.index(min_number)] += 1
        print(math.prod(a))

#print ("\n ПРОВЕРОЧНЫЙ ТЕСТ ")

#check = [
#    ([2,2,1,2], 16),
#    ([0,1,2], 2),
#    ([4,3,2,3,4], 432),
#    ([9]*9, 430467210)
#    ]
#for numbers, expected in check:
#    a = numbers.copy()
#    if 0 in a:
#        a[a.index(0)] = 1
#    else:
#        a[a.index(min(a))] += 1
#    result = math.prod(a)
#    print(f"{numbers} => {result} (ожидалось {expected}) {'+' if result == expected else '-'}")
        
            
