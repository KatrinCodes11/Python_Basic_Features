"""
Игра "Жизнь" (Conway's Game of Life) в консольном режиме

Программа предназначена для моделирования развития колонии клеток на прямоугольном поле.

Программа считывает начальную конфигурацию поля из текстового файла, выполняет заданное количество шагов моделирования и сохраняет результаты каждого шага в виде текстового файла с конфигурацией поля
и изображения в формате PNG. Для формирования изображений используется библиотека Pillow.

Краткое описание игры "Жизнь": поле - прямоугольная таблица клеток. Каждая клетка может находиться в одном из двух состояний: живом или мёртвом. На каждом шаге моделирования для каждой клетки подсчитывается
количество живых соседей в 8 направлениях. Переход к следующему состоянию осуществляется следующим образом:

1. живая клетка остаётся живой, если у неё 2 или 3 живых соседа;
2. живая клетка умирает, если число живых соседей меньше 2 или больше 3;
3. мёртвая клетка становится живой, если у неё ровно 3 живых соседа.
В программе учитывается возраст каждой живой клетки.

Формат входного файла: входной файл задаёт начальную конфигурацию поля. Файл - текстовый документ, где каждая строка соответствует 1 строке поля, символ # обозначает живую клетку, любой другой символ обозначает
мёртвую клетку. Все строки входного файла должны имет одинаковую длину.

Пример входного файла:

.......
..#....
...#...
.###...
.......

Поле - это двумерный массив клеток, описывающий состояние колонии на текущем шаге моделирования. В программе поле хранится в виде двумерного списка, где 1 - живая клетка, 0 - мёртвая клетка. Отдельно для каждой
клетки хранится её возраст - количество шагов, в течение которых клетка остаётся живой подряд. При построении изображения используется оттенок выбранного цвета: чем больше возраст клетки, тем более насыщенный
у неё цвет. Мёртвые клетки отображаются белым цветом.

Запуск программы: программа запускается из командной строки. Общий вид команды: python life.py <входной_файл> <количество шагов> <папка для результатов> [цвет]
Входной файл - имя (или путь) к текстовому файлу с начальным состоянием поля; количество шагов - целочисленное количество шагом моделирования; папка для результатов - имя папки, в которую будут сохраняться
результаты. Все 3 параметра обязательные. Необязательный параметр - цвет. Это базовый цвет живых клеток. Допустимые значения: red, blue, green. Если цвет не указан, используется green.

Пример запуска: python life.py input.txt 20 result green

Результат работы программы: в указанной папке создаются файлы для каждого шага моделирования: текстовое представление поля и изображение состояния поля (файл step_0 соответствует начальному состоянию).

Перед запуском программы необходимо установить библиотеку pillow, подготовить входной текстовый файл с начальными данными, разместить файл программы и входной файл в одной папке (или указать полный путь к файлу
при запуске).

"""

import sys
import os
from PIL import Image

# Словарь базовых цветов
base_colors = {
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255)
}

# Размер одной клетки на изображении (в пикселях)
cell_size = 20

# Максимальный возраст, учитывающийся при вычислении оттенка
max_age_color = 10

# Чтение текстового файла и его преобразование
def read_field(filename):
    f = open(filename, "r")
    field = []

    for line in f:
        line = line.strip()
        if line == "":
            continue
        row = []
        for c in line:
            if c == "#":
                row.append(1)
            else:
                row.append(0)
        field.append(row)

    f.close()
    return field

# Запись поля в текстовый файл
def write_field(field, filename):
    f = open(filename, "w")
    for row in field:
        line = ""
        for c in row:
            if c > 0:
                line += "#"
            else:
                line += "."
        f.write(line + "\n")
    f.close()

# Подсчёт количества живых соседей, где x и y - координаты клетки
def count_neighbors(field, x, y, h, w):
    count = 0
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if dx == 0 and dy == 0:
                continue
            nx = x + dx
            ny = y + dy
            if 0 <= nx < w and 0 <= ny < h:
                if field[ny][nx] > 0:
                    count += 1
    return count

# Вычисление следующего поколения
def step(field, ages, h, w):
    new_field = []
    new_ages = []

    for y in range(h):
        row_field = []
        row_ages = []
        for x in range(w):
            row_field.append(0)
            row_ages.append(0)
        new_field.append(row_field)
        new_ages.append(row_ages)

    for y in range(h):
        for x in range(w):
            neighbours = count_neighbors(field, x, y, h, w)
            if field[y][x] > 0:
                if neighbours == 2 or neighbours == 3:
                    new_field[y][x] = 1
                    new_ages[y][x] = ages[y][x] + 1
                else:
                    new_field[y][x] = 0
                    new_ages[y][x] = 0
            else:
                if neighbours == 3:
                    new_field[y][x] = 1
                    new_ages[y][x] = 1
                else:
                    new_field[y][x] = 0
                    new_ages[y][x] = 0

    return new_field, new_ages

# Преобразование возраста клетки в цветовой оттенок
def age_to_color(age, base_color):
    if age <= 0:
        return (255, 255, 255)
    k = min(age, max_age_color) / max_age_color
    r, g, b = base_color
    return (
        int(255 - (255 - r) * k),
        int(255 - (255 - g) * k),
        int(255 - (255 - b) * k)
    )

# Сохранение изображения текущего состояния поля
def save_image(field, ages, filename, base_color, h, w):
    img = Image.new(
        "RGB",
        (w * cell_size, h * cell_size),
        (255, 255, 255)
    )
    pixels = img.load()

    for y in range(h):
        for x in range(w):
            if field[y][x] > 0:
                color = age_to_color(ages[y][x], base_color)
            else:
                color = (255, 255, 255)
            for dy in range(cell_size):
                for dx in range(cell_size):
                    px = x * cell_size + dx
                    py = y * cell_size + dy
                    pixels[px, py] = color
    img.save(filename)

# Основная функция программы
def main():
    if len(sys.argv) < 4:
        print("Ошибка: недостаточно параметров")
        return

    input_file = sys.argv[1]
    steps = int(sys.argv[2])
    output_dir = sys.argv[3]
    color_name = sys.argv[4] if len(sys.argv) > 4 else "green"

    if color_name not in base_colors:
        print("Ошибка: указан недопустимый цвет")
        return
    base_color = base_colors[color_name]

    os.makedirs(output_dir, exist_ok=True)

    field = read_field(input_file)
    h = len(field)
    w = len(field[0])

    ages = []
    for y in range(h):
        row = []
        for x in range(w):
            if field[y][x] > 0:
                row.append(1)
            else:
                row.append(0)
        ages.append(row)

    write_field(field, os.path.join(output_dir, "step_0.txt"))
    save_image(field, ages, os.path.join(output_dir, "step_0.png"), base_color, h, w)

    for i in range(1, steps + 1):
        field, ages = step(field, ages, h, w)
        write_field(field, os.path.join(output_dir, f"step_{i}.txt"))
        save_image(field, ages, os.path.join(output_dir, f"step_{i}.png"), base_color, h, w)

main()
        
