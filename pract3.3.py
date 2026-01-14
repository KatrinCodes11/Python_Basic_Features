"""
Спецификация программы

1. Множества и типы:
   R+ - множество положительных вещественных чисел
   D = {d₁, d₂, h, Vₛ, n} - множество входных параметров, где:
     d₁, h ∈ R+, единица измерения: ярды (yd)
     d₂ ∈ R+, единица измерения: футы (ft)
     Vₛ ∈ R+, единица: мили/час (mph)
     n ∈ R+, n ≥ 1 (безразмерный)

2. Функции преобразования единиц измерения
   f₁: yd => ft, f₁(x) = 3x
   f₂: mph => ft/s, f₂(v) = v × 5280/3600

3. Математическая модель:
   3.1 Промежуточные величины:
        d₁' = f₁(d₁)  [ft]
        h' = f₁(h)    [ft]
        Vₛ' = f₂(Vₛ)  [ft/s]
   
   3.2 Длины путей для угла θ (в радианах):
        x = d₁' × tan(θ)
        L₁(θ) = |AB| = √(x² + d₁'²)
        L₂(θ) = |BC| = √((h' - x)² + d₂²)
   
   3.3 Время для угла θ:
        t(θ) = (L₁(θ) + n × L₂(θ)) / Vₛ'  [s]

4. Функциональная структура:
   ∀(d₁, d₂, h, Vₛ, n) ∈ D:
     get_user_input: input stream => D
     (запрос 5 значений через стандартный ввод)
     validate_input: D => {True, False}
     convert_units: (d₁, h, Vₛ) => (d₁', h', Vₛ')
     find_optimal_angle: (d₁', d₂, h', Vₛ', n) => (θ_opt, t_min)
     display_results: (θ_opt, t_min) => output(θ_opt, t_min)

5. Предусловия:
   C1: d₁ > 0 ∧ d₂ > 0 ∧ h > 0
   C2: Vₛ > 0
   C3: n ≥ 1
   C4: Программа завершится корректно при выполнении C1 ∧ C2 ∧ C3

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
    return d1, d2, h, V_sand, n

def validate_input(d1, d2, h, V_sand, n):
    # Функция для валидации входных данных
    if d1 <= 0:
        return False, "Ошибка: расстояние d1 должно быть положительным!"
    if d2 <= 0:
        return False, "Ошибка: расстояние d2 должно быть положительным!"
    if h <= 0:
        return False, "Ошибка: боковое смещение h должно быть положительным!"
    
    if V_sand <= 0:
        return False, "Ошибка: скорость V_sand должна быть положительной!"
    
    if n < 1:
        return False, "Ошибка: коэффициент замедления n должен быть ≥ 1!"
    
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
    # Функция для поиска оптимального угла в диапазоне от 0 до 90 градусов
    min_time = float('inf')
    optimal_angle = 0
    
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

def test_convert_units():
    print("\nТестирование convert_units")
    
    inputs_1 = (10, 20, 1)
    result = convert_units(*inputs_1)
    expected_1 = (30, 60, 1 * 5280 / 3600)
    
    assert abs(result[0] - expected_1[0]) < 0.001, f"Ошибка: d1_f={result[0]}, ожидалось {expected_1[0]}"
    assert abs(result[1] - expected_1[1]) < 0.001, f"Ошибка: h_f={result[1]}, ожидалось {expected_1[1]}"
    print(f"Тест 1: Ярды => футы: inputs={inputs_1[:2]}, expected={expected_1[:2]}, result={result[:2]}")
    
    assert abs(result[2] - expected_1[2]) < 0.01, f"Ошибка: V_sand_fs={result[2]}, ожидалось {expected_1[2]}"
    print(f"Тест 2: Мили/ч => футы/с: expected={expected_1[2]:.5f}, result={result[2]:.5f}")
    
    print("Все тесты convert_units пройдены успешно!")

def test_calculate_time():
    print("\nТестирование calculate_time")
    
    d1_f, d2, h_f, V_sand_fs, n = 30, 50, 60, 1.46667, 1.5
    
    result_1 = calculate_time_for_angle(d1_f, d2, h_f, V_sand_fs, n, 45)
    assert result_1 > 0, f"Ошибка: t={result_1}"
    print(f"Тест 1: Базовый случай: θ=45°, result={result_1:.2f} сек")
    
    result_2 = calculate_time_for_angle(d1_f, d2, h_f, V_sand_fs, n, 0)
    expected_L1 = 30  
    expected_L2 = math.sqrt(60**2 + 50**2)  
    expected_t = (expected_L1 + 1.5 * expected_L2) / 1.46667
    assert abs(result_2 - expected_t) < 0.001, f"Ошибка: t={result_2}, ожидалось {expected_t}"
    print(f"Тест 2: θ=0°: expected={expected_t:.2f}, result={result_2:.2f}")
    
    result_3 = calculate_time_for_angle(d1_f, d2, h_f, V_sand_fs, n, 89.999)
    assert result_3 > 0, f"Ошибка: t={result_3}"
    assert result_3 > result_2, f"Ошибка: при θ≈90° время должно быть больше чем при θ=0°"
    print(f"Тест 3: θ≈90°: result={result_3:.2f} сек (должно быть > {result_2:.2f})")

    result_low = calculate_time_for_angle(d1_f, d2, h_f, V_sand_fs, 1.0, 45)
    result_high = calculate_time_for_angle(d1_f, d2, h_f, V_sand_fs, 10.0, 45)
    assert result_high > result_low, f"Ошибка: при n=10 время должно быть больше чем при n=1"
    print(f"Тест 4: Влияние n: t(n=10)={result_high:.2f} > t(n=1)={result_low:.2f}")

    print("Все тесты calculate_time пройдены успешно!")

def test_validate_input():
    print("\nТестирование validate_input")
    
    print("Тест 1: Ошибка в расстояниях")
    assert validate_input(-5, 50, 20, 5, 1.5)[0] == False
    assert validate_input(10, -5, 20, 5, 1.5)[0] == False
    assert validate_input(10, 50, -5, 5, 1.5)[0] == False
    print("Тест 1 пройден")
    
    print("Тест 2: Ошибка в скорости")
    assert validate_input(10, 50, 20, 0, 1.5)[0] == False
    print("Тест 2 пройден")
    
    print("Тест 3: Ошибка в коэффициенте n")
    assert validate_input(10, 50, 20, 5, 0.5)[0] == False
    print("Тест 3 пройден")
    
    print("Тест 4: Корректные данные")
    assert validate_input(10, 50, 20, 5, 1.5)[0] == True
    print("Тест 4 пройден")

def test_find_optimal_angle():
    print("\nТестирование find_optimal_angle")
    
    print("Тест 1: Базовый случай")
    d1_f, d2, h_f, V_sand_fs, n = 30, 50, 60, 7.3333, 1.5
    theta_opt, t_min = find_optimal_angle(d1_f, d2, h_f, V_sand_fs, n)
    
    assert 0 <= theta_opt <= 90, f"Оптимальный угол вне диапазона: {theta_opt}"
    assert t_min > 0, "Минимальное время должно быть положительным"
    
    for angle in [0, 45, 90]:
        t_test = calculate_time_for_angle(d1_f, d2, h_f, V_sand_fs, n, angle)
        assert t_min <= t_test, f"t_min={t_min} должно быть ≤ t({angle}°)={t_test}"
    
    print(f"Найден оптимальный угол: {theta_opt}°, время: {t_min:.2f} сек")


print("\n ПРОГРАММА ДЛЯ ОПРЕДЕЛЕНИЯ ОПТИМАЛЬНОГО УГЛА ДВИЖЕНИЯ СПАСАТЕЛЯ")

d1, d2, h, V_sand, n = get_user_input()

is_valid, message = validate_input(d1, d2, h, V_sand, n)

if not is_valid:
   print(f"\n{message}")
else:
    d1_f, h_f, V_sand_fs = convert_units(d1, h, V_sand)
    
    theta_opt, t_min = find_optimal_angle(d1_f, d2, h_f, V_sand_fs, n)
    
    display_results(theta_opt, t_min)

# Запуск тестов
test_convert_units()
test_calculate_time()
test_validate_input()
test_find_optimal_angle()
