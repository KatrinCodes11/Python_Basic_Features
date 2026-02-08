"""
Поиск данных по почтовым индексам США

Программа предназначена для работы с набором данных, содержащим информацию о почтовых индексах США. Программа позволяет пользователю получать информацию о местоположении по почтовому индексу, находить почтовые
индексы по названию города и штата, вычислять геодезическое расстояние между двумя точками, заданными почтовыми индексами. Работа программы осуществляется в режиме REPL.

Входные данные: csv-файл zip_codes_states.csv
Файл должен находиться в той же директории, что и файл программы. Файл содержит следующие столбцы: zip_code, latitude, longtitude, city, state, county

Запуск программы: осуществляется из командной строки (команда python pract6.py). После запуска выводится предложение ввода команды.

После запуска пользователь видит предложение ввести какую-либо из следующих команд: loc, zip, dist, end (команды не чувствительны к регистру символов).

Команда loc: ищет информацию по почтовому индексу. После ввода команды программа запрашивает почтовый индекс. Результат работы команды: город, штат, географические координаты (формат: градусы/минуты/секунды и
направление)

Команда zip: ищет все почтовые индексы по названию города и штата. После ввода команды программа запрашивает названия города и штата. Результат - список всех найденных почтовых индексов, отсортированных по
возрастанию.

Команда dist: вычисляет расстояние между двумя географическими точками, заданными их почтовыми индексами. После ввода команды программа запрашивает 2 почтовых индекса. Результат - расстояние, вычисленное по
формуле гаверсинусов (в милях).

Если введённые по запросу данные отсутствуют в csv-файле, выводится сообщение об ошибке. (строки файла с некорректными или отсутствующими координатами автоматически пропускаются при чтении данных)

Команда end:  завершает работу программы.

Если введённая команда не относится к списку допустимых команд, программа выводит сообщение об ошибке и продолжает работу.

"""


import csv
import math

# Чтение данных из csv-файла

def read_zip(filename):
    data = []

    with open(filename, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)

        next(reader, None)

        for row in reader:
            if len(row) < 6 or row[1] == "" or row[2] == "":
                continue
            try:
                zip_code = row[0]
                latitude = float(row[1])
                longtitude = float(row[2])
                city = row[3]
                state = row[4]
                county = row[5]
            except ValueError:
                continue
            
            data.append([zip_code, latitude, longtitude, city, state, county])
    return data

# Перевод координаты в градусы (мин и с)

def to_dms(value, direction_type):

    if direction_type == 'lat':
        dir_letter = 'N' if value >= 0 else 'S'
    else:
        dir_letter = 'E' if value >= 0 else 'W'

    value = abs(value)
    deg = int(value)
    minutes_full = (value - deg) * 60
    minutes = int(minutes_full)
    seconds = (minutes_full - minutes) * 60

    return f'{deg:03d}\u00B0{minutes:02d}\'{seconds:05.2f}"{dir_letter}'

# Вычисление расстояния между двумя точками (в милях)
def haversine_miles(lat1, lon1, lat2, lon2):
    r_km = 6371.0
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + \
        math.cos(lat1) * math.cos(lat2) * \
        math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    km = r_km * c
    return km * 0.621371

# Создание словарей для быстрого поиска по данным

def indexes(data):
    by_zip = {}
    by_city_state = {}
    for row in data:
        zip_code = row[0]
        city = row[3]
        state = row[4]
        by_zip[zip_code] = row
        key = (city.lower(), state.lower())
        by_city_state.setdefault(key, []).append(zip_code)
    return by_zip, by_city_state

# Основная функция

def main():

    data = read_zip("zip_codes_states.csv")

    by_zip, by_city_state = indexes(data)

    while True:
        cmd = input("Command ('loc', 'zip', 'dist', 'end') => ").strip()
        print(cmd)
        cmd = cmd.lower()

        if cmd == "end":
            print("Done")
            break

        elif cmd == "loc":
            zip_code = input("Enter a zip code to lookup => ")
            print(zip_code)
            if zip_code not in by_zip:
                print("Error: zip code not found")
                continue
            row = by_zip[zip_code]
            z, lat, lon, city, state, county = row
            lat_dms = to_dms(lat, 'lat')
            lon_dms = to_dms(lon, 'lon')
            print(f"Zip code {z} is in [city], {state}, {county} county, ")
            print(f"coordinates: ({lat_dms}, {lon_dms})")

        elif cmd == "zip":
            city = input("Enter a city name to lookup => ")
            print(city)
            state = input("Enter the state name to lookup => ")
            print(state)
            key = (city.lower(), state.lower())
            if key not in by_city_state:
                print("Error: city/state not found")
                continue
            zips = sorted(by_city_state[key])
            print(f"The following zip code(s) found for {city}, {state}: "+", ".join(zips))

        elif cmd == "dist":
            z1 = input("Enter the first zip code => ")
            print(z1)
            z2 = input("Enter the second zip code => ")
            print(z2)
            if z1 not in by_zip or z2 not in by_zip:
                print("Error: zip code not found")
                continue
            r1 = by_zip[z1]
            r2 = by_zip[z2]
            lat1, lon1 = r1[1], r1[2]
            lat2, lon2 = r2[1], r2[2]
            d = haversine_miles(lat1, lon1, lat2, lon2)
            print(f"The distance between {z1} and {z2} is {d:.2f} miles")

        else:
            print("Invalid command")

main()
        
            
