n = int(input())
a = list(map(int, input().split()))

# Случай 1: если сумма всего массива не равна нулю
if sum(a) != 0:
    print("YES")
    print(1)
    print(1, n)
else:
    # Случай 2: сумма массива равна нулю, поиск места для разбиения массива
    current_sum = 0 
    
    for i in range(n):
        current_sum += a[i]  # добавляем текущий элемент
        
        # Проверяем сумму первых i+1 элементов
        if current_sum != 0:
            print("YES")
            print(2)  # разбиваем на 2 подмассива
            
            print(1, i + 1)
            
            print(i + 2, n)
            break
    
    else:
        # Случай 3: сумма любых первых k элементов всегда равна 0. Это означает, что все элементы массива равны 0
        print("NO")
