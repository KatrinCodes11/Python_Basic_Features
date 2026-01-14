"""
Спецификация программы

1. Множества и типы:
   R+ - множество положительных вещественных чисел
   D = {d₁, d₂, h, Vₛ, n, θ₁} - множество входных параметров, где:
     d₁, h ∈ R+, единица измерения: ярды (yd)
     d₂ ∈ R+, единица измерения: футы (ft)
     Vₛ ∈ R+, единица: мили/час (mph)
     n ∈ R+, n ≥ 1 (безразмерный)
     θ₁ ∈ [0, 90], единица: градусы (°)

2. Функции преобразования единиц измерения
   f₁: yd => ft, f₁(x) = 3x
   f₂: mph => ft/s, f₂(v) = v × 5280/3600
   f₃: ° => rad, f₃(α) = α × pi/180

3. Математическая модель:
   3.1 Промежуточные величины:
        d₁' = f₁(d₁)  [ft]
        h' = f₁(h)    [ft]
        Vₛ' = f₂(Vₛ)  [ft/s]
   
   3.2 Длины путей для угла θ:
        x = d₁' × tan(θ')
        L₁(θ) = |AB| = √(x² + d₁'²)
        L₂(θ) = |BC| = √((h' - x)² + d₂²)
   
   3.3 Время для угла θ:
        t(θ) = (L₁(θ) + n × L₂(θ)) / Vₛ'  [s]

4. Функциональная структура:
   ∀(d₁, d₂, h, Vₛ, n, θ₁) ∈ D:
     get_user_input: input stream => D
     (запрос 6 значений через стандартный ввод)
     validate_input: D => {True, False}
     convert_units: (d₁, h, Vₛ) => (d₁', h', Vₛ')
     find_optimal_angle: (d₁', d₂, h', Vₛ', n) => (θ_opt, t_min)
     display_results: (θ_opt, t_min) => output(θ_opt, t_min)

5. Предусловия:
   C1: d₁ > 0 ∧ d₂ > 0 ∧ h > 0
   C2: Vₛ > 0
   C3: n ≥ 1
   C4: 0 ≤ θ₁ ≤ 90
   C5: Программа завершится корректно при выполнении C1 ∧ C2 ∧ C3 ∧ C4

6. Постусловие:
   После выполнения программы будет выведено минимальное время t_min ∈ R+
   с точностью до 0.1 секунды и соответствующий угол θ_opt ∈ [0, 90],
   при котором достигается минимальное время.
"""

import math

def get_user_input():
    # Функция для взаимодействия с пользователем и получения исходных данных
    d1 = float(input("Введите кратчайшее расстояние между спасателем и кромкой воды, d1 (ярды) => "))
    d2 = float(input("Введите кратчайшее расстояние от утопающего до берега, d2 (футы) => "))
    h = float(input("Введите боковое смещение между спасателем и утопающим, h (ярды) => "))
    V_sand = float(input("Введите скорость движения спасателя по песку, V_sand (мили/час) => "))
    n = float(input("Введите коэффициент замедления спасателя при движении в воде, n => "))
    theta1 = float(input("Введите направление движения спасателя по песку, theta1 (град) => "))
    return d1, d2, h, V_sand, n, theta1

def validate_input(d1, d2, h, V_sand, n, theta1):
    # Функция для валидации входных данных. Возвращает кортеж (is_valid, error_message)
    
    # Проверка положительных расстояний
    if d1 <= 0:
        return False, "Ошибка: расстояние d1 должно быть положительным!"
    if d2 <= 0:
        return False, "Ошибка: расстояние d2 должно быть положительным!"
    if h <= 0:
        return False, "Ошибка: боковое смещение h должно быть положительным!"
    
    # Проверка положительной скорости
    if V_sand <= 0:
        return False, "Ошибка: скорость V_sand должна быть положительной!"
    
    # Проверка коэффициента замедления
    if n < 1:
        return False, "Ошибка: коэффициент замедления n должен быть ≥ 1!"
    
    # Проверка угла (диапазон [0, 90])
    if theta1 < 0 or theta1 > 90:
        return False, "Ошибка: угол theta1 должен быть в диапазоне от 0 до 90 градусов включительно!"
    
    return True, "Валидация пройдена успешно"

def convert_units(d1, h, V_sand):
    # Функция для преобразования единиц измерения
    d1_f = d1 * 3  # ярды => футы
    h_f = h * 3  # ярды => футы
    V_sand_fs = V_sand * 5280 / 3600  # мили/час => футы/сек
    return d1_f, h_f, V_sand_fs

def calculate_time_for_angle(d1_f, d2, h_f, V_sand_fs, n, theta_deg):
    # Функция для вычисления времени для конкретного угла
    theta_rad = math.radians(theta_deg)
    x = d1_f * math.tan(theta_rad)
    L1 = math.sqrt(x**2 + d1_f**2)
    L2 = math.sqrt((h_f - x)**2 + d2**2)
    t = (L1 + n * L2) / V_sand_fs
    return t

def find_optimal_angle(d1_f, d2, h_f, V_sand_fs, n):
    # Функция для поиска оптимального угла в диапазоне от 0 до 90 градусов с шагом 1 градус
    min_time = float('inf')
    optimal_angle = 0
    
    # Цикл по всем углам от 0 до 90 градусов включительно с шагом 1 градус
    for angle in range(0, 91):
        current_time = calculate_time_for_angle(d1_f, d2, h_f, V_sand_fs, n, angle)
        
        if current_time < min_time:
            min_time = current_time
            optimal_angle = angle
    
    return optimal_angle, min_time

def display_results(theta_opt, t_min):
    # Функция для вывода результатов
    print(f"\nОптимальный угол для начала движения: {theta_opt} градусов")
    print(f"Минимальное время достижения утопающего: {t_min:.1f} секунд")

# МОДУЛЬНЫЕ ТЕСТЫ

#import math

#def test_convert_units():
    # Тестирование преобразования единиц измерения
    #print("\nТестирование convert_units")
    
    # Тест 1: Преобразование ярдов в футы
    #inputs_1 = (10, 20, 1)  # d1, h, V_sand
    #result = convert_units(*inputs_1)
    #expected_1 = (30, 60, 1 * 5280 / 3600)  # d1_f, h_f, V_sand_fs
    
    #assert abs(result[0] - expected_1[0]) < 0.001, f"Ошибка: d1_f={result[0]}, ожидалось {expected_1[0]}"
    #assert abs(result[1] - expected_1[1]) < 0.001, f"Ошибка: h_f={result[1]}, ожидалось {expected_1[1]}"
    #print(f"Тест 1: Ярды => футы: inputs={inputs_1[:2]}, expected={expected_1[:2]}, result={result[:2]}")
    
    # Тест 2: Преобразование скорости
    #assert abs(result[2] - expected_1[2]) < 0.01, f"Ошибка: V_sand_fs={result[2]}, ожидалось {expected_1[2]}"
    #print(f"Тест 2: Мили/ч => футы/с: expected={expected_1[2]:.5f}, result={result[2]:.5f}")
    
    #print("Все тесты convert_units пройдены успешно!")
    

#def test_calculate_time():
    # Тестирование вычисления времени
    #print("\n Тестирование calculate_time")
    
    # Тест 1: Базовый случай (θ₁ = 45°)
    #inputs_1 = {
        #'d1_f': 30,        # 10 ярдов = 30 футов
        #'d2': 50,          # 50 футов
        #'h_f': 60,         # 20 ярдов = 60 футов
        #'V_sand_fs': 1.46667,  # 1 миля/час
        #'n': 1.5,          # коэффициент замедления
        #'theta1_rad': math.radians(45)
    #}
    #result_1 = calculate_time_for_angle(inputs_1['d1_f'], inputs_1['d2'], inputs_1['h_f'], 
                                       #inputs_1['V_sand_fs'], inputs_1['n'], 45)
    #assert result_1 > 0, f"Ошибка: t={result_1}"
    #print(f"Тест 1: Базовый случай: inputs={inputs_1}, result={result_1:.2f} сек")
    
    # Тест 2: Граничный случай (θ₁ = 0°)
    #inputs_2 = inputs_1.copy()
    #inputs_2['theta1_rad'] = math.radians(0)
    #result_2 = calculate_time_for_angle(inputs_2['d1_f'], inputs_2['d2'], inputs_2['h_f'], 
                                       #inputs_2['V_sand_fs'], inputs_2['n'], 0)
    
    # Ожидаемый расчёт для θ₁ = 0°
    #expected_L1 = 30  
    #expected_L2 = math.sqrt(60**2 + 50**2)  
    #expected_t = (expected_L1 + 1.5 * expected_L2) / 1.46667
    
    #assert abs(result_2 - expected_t) < 0.001, f"Ошибка: t={result_2}, ожидалось {expected_t}"
    #print(f"Тест 2: θ₁=0°: expected={expected_t:.2f}, result={result_2:.2f}")
    
    # Тест 3: Граничный случай (θ₁ близко к 90°)
    #inputs_3 = inputs_1.copy()
    #inputs_3['theta1_rad'] = math.radians(89.999)
    #result_3 = calculate_time_for_angle(inputs_3['d1_f'], inputs_3['d2'], inputs_3['h_f'], 
                                       #inputs_3['V_sand_fs'], inputs_3['n'], 89.999)
    
    #assert result_3 > 0, f"Ошибка: t={result_3}"
    #assert result_3 > result_2, f"Ошибка: при θ₁ близкому к 90° время должно быть больше чем при θ₁=0°"
    #print(f"Тест 3: θ₁ близкий к 90°: result={result_3:.2f} сек (должно быть > {result_2:.2f})")

    # Тест 4: Влияние коэффициента n
    #inputs_4_low_n = inputs_1.copy()
    #inputs_4_high_n = inputs_1.copy()
    
    #inputs_4_low_n['n'] = 1.0
    #inputs_4_high_n['n'] = 10.0
    
    #result_low = calculate_time_for_angle(inputs_4_low_n['d1_f'], inputs_4_low_n['d2'], inputs_4_low_n['h_f'], 
                                         #inputs_4_low_n['V_sand_fs'], inputs_4_low_n['n'], 45)
    #result_high = calculate_time_for_angle(inputs_4_high_n['d1_f'], inputs_4_high_n['d2'], inputs_4_high_n['h_f'], 
                                          #inputs_4_high_n['V_sand_fs'], inputs_4_high_n['n'], 45)
    
    #assert result_high > result_low, f"Ошибка: при n=10 время должно быть больше чем при n=1"
    #print(f"Тест 4: Влияние n: t(n=10)={result_high:.2f} > t(n=1)={result_low:.2f}")

    #print("Все тесты calculate_time пройдены успешно!") 


#def test_validate_input():
    # Тестирование валидации входных данных
    #print("\nТестирование validate_input")
    
    # Тест 1: Поиск ошибки в расстояниях
    #print("Тест 1: Ошибка в d1, d2, h")
    #assert validate_input(-5, 50, 20, 5, 1.5, 45)[0] == False
    #assert validate_input(10, -5, 20, 5, 1.5, 45)[0] == False
    #assert validate_input(10, 50, -5, 5, 1.5, 45)[0] == False
    #print("Тест 1 пройден")
    
    # Тест 2: Поиск ошибки в скорости
    #print("Тест 2: Ошибка в V_sand")
    #assert validate_input(10, 50, 20, 0, 1.5, 45)[0] == False
    #print("Тест 2 пройден")
    
    # Тест 3: Поиск ошибки в коэффициенте n
    #print("Тест 3: Ошибка в n")
    #assert validate_input(10, 50, 20, 5, 0.5, 45)[0] == False
    #print("Тест 3 пройден")
    
    # Тест 4: Поиск ошибки в угле
    #print("Тест 4: Ошибка в teta")
    #assert validate_input(10, 50, 20, 5, 1.5, -10)[0] == False
    #assert validate_input(10, 50, 20, 5, 1.5, 100)[0] == False
    #print("Тест 4 пройден")
    

#def test_find_optimal_angle():
    # Тестирование поиска оптимального угла
    #print("\nТестирование find_optimal_angle")
    
    # Тест 1: Базовый случай
    #print("Тест 1: Базовый случай")
    #d1_f, d2, h_f, V_sand_fs, n = 30, 50, 60, 7.3333, 1.5
    #theta_opt, t_min = find_optimal_angle(d1_f, d2, h_f, V_sand_fs, n)
    
    #assert 0 <= theta_opt <= 90, f"Оптимальный угол вне диапазона: {theta_opt}"
    #assert t_min > 0, "Минимальное время должно быть положительным"
    
    # Проверяем, что найденное время действительно минимальное
    #for angle in [0, 45, 90]:  # Проверяем ключевые точки
        #t_test = calculate_time_for_angle(d1_f, d2, h_f, V_sand_fs, n, angle)
        #assert t_min <= t_test, f"t_min={t_min} должно быть ≤ t({angle}°)={t_test}"
    
    #print(f"Найден оптимальный угол: {theta_opt}°, время: {t_min:.2f} сек")
    
#def run_all_tests():
    #print("\nЗАПУСК МОДУЛЬНЫХ ТЕСТОВ")
    
    #try:
        #test_convert_units()
        #test_calculate_time()
        #test_validate_input()
        #test_find_optimal_angle()
        
        #print("\nВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
        
    #except AssertionError as e:
        #print(f"\nТЕСТ ПРОВАЛЕН: {e}")
       # print("\nНЕКОТОРЫЕ ТЕСТЫ НЕ ПРОЙДЕНЫ")
 

# Получение входных данных
d1, d2, h, V_sand, n, theta1 = get_user_input()

# Валидация входных данных
is_valid, message = validate_input(d1, d2, h, V_sand, n, theta1)

if not is_valid:
   print(f"\n{message}")
else:
    # Преобразование единиц измерения
    d1_f, h_f, V_sand_fs = convert_units(d1, h, V_sand)
    
    # Поиск оптимального угла
    theta_opt, t_min = find_optimal_angle(d1_f, d2, h_f, V_sand_fs, n)
    
    # Вывод результатов
    display_results(theta_opt, t_min)
    

#run_all_tests()
