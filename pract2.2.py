
"""
Спецификация программы

1. Множества и типы:
   R+ - множество положительных вещественных чисел
   D = {d₁, d₂, h, Vₛ, n, θ₁} - множество входных параметров, где:
     d₁, h ∈ R+, единица измерения: ярды (yd)
     d₂ ∈ R+, единица измерения: футы (ft)
     Vₛ ∈ R+, единица: мили/час (mph)
     n ∈ R+, n ≥ 1 (безразмерный)
     θ₁ ∈ (0, pi/2), единица: градусы (°)

2. Функции преобразования единиц измерения
   f₁: yd => ft, f₁(x) = 3x
   f₂: mph => ft/s, f₂(v) = v × 5280/3600
   f₃: ° => rad, f₃(α) = α × pi/180

3. Математическая модель:
   3.1 Промежуточные величины:
        d₁' = f₁(d₁)  [ft]
        h' = f₁(h)    [ft]
        Vₛ' = f₂(Vₛ)  [ft/s]
        θ₁' = f₃(θ₁)  [rad]
   
   3.2 Длины путей:
        L₁ = |AB| = √(x² + d₁'²)
        L₂ = |BC| = √((h' - x)² + d₂²)
   
   3.3 Время:
        t = (L₁ + n × L₂) / Vₛ'  [s]

4. Функциональная структура:
   ∀(d₁, d₂, h, Vₛ, n, θ₁) ∈ D:
     get_user_input: input stream => D
     (запрос 6 значений через стандартный ввод)
     convert_units:(d₁, h, Vₛ, θ₁) =>(d₁', h', Vₛ', θ₁')
     calculate_time: (d₁', d₂, h', Vₛ', n, θ₁') => t
     display_results: (θ₁, t) => output(θ₁, t)

5. Предусловия:
   C1: d₁ > 0 ∧ d₂ > 0 ∧ h > 0
   C2: Vₛ > 0
   C3: n ≥ 1
   C4: 0 < θ₁ < 90
   C5: Программа завершится корректно при выполнении C1 ∧ C2 ∧ C3 ∧ C4

6. ПОСТУСЛОВИЕ:
   После выполнения программы будет выведено значение t ∈ R+
   с точностью до 0.1 секунды и соответствующий угол θ₁.
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

def convert_units(d1, h, V_sand, theta1):
    # Функция для преобразования единиц измерения
    d1_f = d1 * 3  # ярды => футы
    h_f = h * 3  # ярды => футы
    V_sand_fs = V_sand * 5280 / 3600  # мили/час => футы/сек
    theta1_rad = math.radians(theta1)  # град => рад
    return d1_f, h_f, V_sand_fs, theta1_rad

def calculate_time(d1_f, d2, h_f, V_sand_fs, n, theta1_rad):
    # Функция для выполнения вычислений времени
    x = d1_f * math.tan(theta1_rad)
    L1 = math.sqrt(x**2 + d1_f**2)
    L2 = math.sqrt((h_f - x)**2 + d2**2)
    t = (L1 + n * L2) / V_sand_fs
    return t

def display_results(theta1, t):
    # Функция для вывода результатов
    print(f"Если спасатель начнёт движение под углом theta1, равным {int(theta1)} градусам, он")
    print(f"достигнет утопающего через {t:.1f} секунды")

   # МОДУЛЬНЫЕ ТЕСТЫ
"""
Структура модульных тестов:
Тесты convert_units (3 теста) - проверка преобразования каждой единицы измерения
Тесты calculate_time (4 теста) - проверка вычислений в различных сценариях
Всего: 7 тестов

Обоснование количества тестов:
- convert_units: проверяем 3 типа преобразований (длина, скорость, угол)
- calculate_time: проверяем:
   Базовый случай (нормальные данные)
   Граничный случай (θ₁ = 0°)
   Граничный случай (θ₁ = 90°)
   Случай с максимальным n (сильное замедление в воде)

display_results не тестируется, так как это функция вывода.
get_user_input не тестируется, так как зависит от пользовательского ввода.
"""
#def test_convert_units():
    #"""Тестирование преобразования единиц измерения"""
    #print("\n Тестирование convert_units")
    
    # Тест 1: Преобразование ярдов в футы
    #inputs_1 = (10, 20, 1, 45)  # d1, h, V_sand, theta1
    #result = convert_units(*inputs_1)
    #expected_1 = (30, 60, 1.46667, math.radians(45))  # d1_f, h_f, V_sand_fs, theta1_rad
    
    #assert abs(result[0] - expected_1[0]) < 0.001, f"Ошибка: d1_f={result[0]}, ожидалось {expected_1[0]}"
    #assert abs(result[1] - expected_1[1]) < 0.001, f"Ошибка: h_f={result[1]}, ожидалось {expected_1[1]}"
    #print(f"Тест 1: Ярды => футы: inputs={inputs_1}, expected={expected_1[:2]}, result={result[:2]}")
    
    # Тест 2: Преобразование скорости
    #assert abs(result[2] - expected_1[2]) < 0.01, f"Ошибка: V_sand_fs={result[2]}, ожидалось {expected_1[2]}"
    #print(f"Тест 2: Мили/ч => футы/с: expected={expected_1[2]:.5f}, result={result[2]:.5f}")
    
    # Тест 3: Преобразование угла
    #assert abs(result[3] - expected_1[3]) < 0.001, f"Ошибка: theta1_rad={result[3]}, ожидалось {expected_1[3]}"
    #print(f"Тест 3: Градусы => радианы: expected={expected_1[3]:.5f}, result={result[3]:.5f}")
    
    #print("Все тесты convert_units пройдены успешно!")

#def test_calculate_time():
    #"""Тестирование вычисления времени"""
    #print("\n Тестирование calculate_time")
    
    # Тест 1: Базовый случай (θ₁ = 45°)
    #inputs_1 = {
    #    'd1_f': 30,        # 10 ярдов = 30 футов
    #    'd2': 50,          # 50 футов
    #    'h_f': 60,         # 20 ярдов = 60 футов
    #   'V_sand_fs': 1.46667,  # 1 миля/час
    #    'n': 1.5,          # коэффициент замедления
    #    'theta1_rad': math.radians(45)
    #}
    #result_1 = calculate_time(**inputs_1)
    #assert result_1 > 0, f"Ошибка: время должно быть положительным, t={result_1}"
    #print(f"Тест 1: Базовый случай: inputs={inputs_1}, result={result_1:.2f} сек")
    
    # Тест 2: Граничный случай (θ₁ = 0°)
    #inputs_2 = inputs_1.copy()
    #inputs_2['theta1_rad'] = math.radians(0)
    #result_2 = calculate_time(**inputs_2)
    
    # Ожидаемый расчёт для θ₁ = 0°
    #expected_L1 = 30  
    #expected_L2 = math.sqrt(60**2 + 50**2)  
    #expected_t = (expected_L1 + 1.5 * expected_L2) / 1.46667
    
    #assert abs(result_2 - expected_t) < 0.001, f"Ошибка: t={result_2}, ожидалось {expected_t}"
    #print(f"Тест 2: θ₁=0°: expected={expected_t:.2f}, result={result_2:.2f}")
    
    # Тест 3: Граничный случай (θ₁ близко к 90°)
    #inputs_3 = inputs_1.copy()
    #inputs_3['theta1_rad'] = math.radians(89.999)
    #result_3 = calculate_time(**inputs_3)
    
    #assert result_3 > 0, f"Ошибка: время должно быть положительным при θ₁ близкому к 90°"
    #assert result_3 > result_2, f"Ошибка: при θ₁ близкому к 90° время должно быть больше чем при θ₁=0°"
    #print(f"Тест 3: θ₁ близкий к 90°: result={result_3:.2f} сек (должно быть > {result_2:.2f})")
    
    # Тест 4: Влияние коэффициента n
    #inputs_4_low_n = inputs_1.copy()
    #inputs_4_high_n = inputs_1.copy()
    
    #inputs_4_low_n['n'] = 1.0
    #inputs_4_high_n['n'] = 10.0
    
    #result_low = calculate_time(**inputs_4_low_n)
    #result_high = calculate_time(**inputs_4_high_n)
    
    #assert result_high > result_low, f"Ошибка: при n=10 время должно быть больше чем при n=1"
    #print(f"Тест 4: Влияние n: t(n=10)={result_high:.2f} > t(n=1)={result_low:.2f}")
    
    #print("Все тесты calculate_time пройдены успешно!")

# Взаимодействие с пользователем
d1, d2, h, V_sand, n, theta1 = get_user_input()

# Преобразование единиц измерения
d1_f, h_f, V_sand_fs, theta1_rad = convert_units(d1, h, V_sand, theta1)

# Выполнение вычислений
t = calculate_time(d1_f, d2, h_f, V_sand_fs, n, theta1_rad)

# Вывод результатов
display_results(theta1, t)

# Выполнение тестов
#test_convert_units()
#test_calculate_time()
