import argparse
import os

months = ['Jan', 'Feb', 'Mar', 'Apr',
        'May', 'Jun', 'Jul', 'Aug',
        'Sep', 'Oct', 'Nov', 'Dec']

labels = [
            'PKT', 'Max TemperatureC', 'Mean TemperatureC',
            'Min TemperatureC', 'Dew PointC', 'MeanDew PointC',
            'Min DewpointC', 'Max Humidity', 'Mean Humidity',
            'Min Humidity', 'Max Sea Level PressurehPa',
            'Mean Sea Level PressurehPa', 'Min Sea Level PressurehPa',
            'Max VisibilityKm', 'Mean VisibilityKm', 'Min VisibilitykM',
            'Max Wind SpeedKm/h', 'Mean Wind SpeedKm/h', 'Max Gust SpeedKm/h',
            'Precipitationmm', 'CloudCover', 'Events', 'WindDirDegrees'
            ]

month_abbr = {
                  1: 'Jan', 2: 'Feb', 3: 'Mar',
                  4: 'Apr', 5: 'May', 6: 'Jun',
                  7: 'Jul', 8: 'Aug', 9: 'Sep',
                  10: 'Oct', 11: 'Nov', 12: 'Dec'
                }


def load_weather_data(file_path, year):
    weather_data = []

    for month_abbr in months:
        file_name = f"Murree_weather_{year}_{month_abbr}.txt"
        full_path = os.path.join(file_path, file_name)

        if not os.path.isfile(full_path):
            continue

        with open(full_path, mode='r') as file:
            next(file)

            for line in file:
                line = line.strip()

                values = line.split(',')

                # Dictionary Comprehension, Creating and Converting tuple into dictionary's key-value pairs
                day_data = {label: value for label, value in zip(labels, values)}
                weather_data.append(day_data)

    return weather_data


def load_weather_data_month(file_path, year, month):
    weather_data_month = []

    months = {
    1: 'Jan', 2: 'Feb', 3: 'Mar',
    4: 'Apr', 5: 'May', 6: 'Jun',
    7: 'Jul', 8: 'Aug', 9: 'Sep',
    10: 'Oct',11: 'Nov', 12: 'Dec'
}

    file_name = f"Murree_weather_{year}_{months[month]}.txt"
    full_path = os.path.join(file_path, file_name)

    if not os.path.isfile(full_path):
        print('Year or Months Data does not exist')

    with open(full_path, mode='r') as file:
        next(file)

        for line in file:
            line = line.strip()

            values = line.split(',')

            # Dictionary Comprehension, Creating and Converting tuple into dictionary's key-value pairs
            day_data = {label: value for label, value in zip(labels, values)}
            weather_data_month.append(day_data)

    return weather_data_month


def calculate_stats(weather_data):
    highest_temp = float('-inf')
    highest_temp_day = None
    lowest_temp = float('inf')
    lowest_temp_day = None
    highest_humidity = 0
    highest_humidity_day = None

    for day_data in weather_data:
        if day_data['Max TemperatureC']:
            temp = int(day_data['Max TemperatureC'])
            if temp > highest_temp:
                highest_temp = temp
                highest_temp_day = day_data['PKT']

            if temp < lowest_temp:
                lowest_temp = temp
                lowest_temp_day = day_data['PKT']

        if day_data['Max Humidity']:
            humidity = int(day_data['Max Humidity'])
            if humidity > highest_humidity:
                highest_humidity = humidity
                highest_humidity_day = day_data['PKT']

    return {
        'Highest': (highest_temp, highest_temp_day),
        'Lowest': (lowest_temp, lowest_temp_day),
        'Humidity': (highest_humidity, highest_humidity_day)
    }


def calculate_stats_month(weather_data):
    highest_temp = float('-inf')
    lowest_temp = float('inf')
    highest_humidity = 0

    high_temps = []
    low_temps = []
    mean_humidity = []

    for day_data in weather_data:
        if day_data['Max TemperatureC']:
            high_temps.append((int)(day_data['Max TemperatureC']))

        if day_data['Min TemperatureC']:
            low_temps.append((int)(day_data['Min TemperatureC']))

        if day_data['Mean Humidity']:
            mean_humidity.append((int)(day_data['Mean Humidity']))

    avg_high_temp = sum(high_temps) / len(high_temps)
    avg_low_temp = sum(low_temps) / len(low_temps)
    avg_mean_humidity = sum(mean_humidity) / len(mean_humidity)

    return {
        'avgHighest': avg_high_temp,
        'avgLowest': avg_low_temp,
        'avgMeanHumidity': avg_mean_humidity
    }


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=str)
    parser.add_argument("-e", type=int)
    parser.add_argument("-a", type=str)
    parser.add_argument("-c", type=str)

    return parser.parse_args()


def main():
    args = parse_args()

    if args.e:
        year = args.e
        weather_data = load_weather_data(args.path, year)
        stats = calculate_stats(weather_data)

        date_high = stats['Highest'][1].split('-')
        date_low = stats['Lowest'][1].split('-')
        date_humid = stats['Humidity'][1].split('-')

        high_val = stats['Highest'][0]
        low_val = stats['Lowest'][0]
        humid_val = stats['Highest'][0]

        print(f"Highest: {high_val} on {month_abbr[(int)(date_high[1])]} {date_high[2]} ")
        print(f"Lowest: {low_val} on {month_abbr[(int)(date_low[1])]} {date_low[2]} ")
        print(f"Humidity: {humid_val}% on {month_abbr[(int)(date_humid[1])]} {date_humid[2]} ")
        print("\n")

    if args.a:
        year_str, month_str = args.a.split('/')
        year = int(year_str)
        month = int(month_str)

        weather_data_month = load_weather_data_month(args.path, year, month)
        month_stats = calculate_stats_month(weather_data_month)
        print(f"Highest Average: {month_stats['avgHighest']:.0f}")
        print(f"Lowest Average: {month_stats['avgLowest']:.0f}")
        print(f"Average Mean Humidiy: {month_stats['avgMeanHumidity']:.0f}%")
        print("\n")

    if args.c:
        year_str, month_str = args.c.split('/')
        year = int(year_str)
        month = int(month_str)

        weather_data_month = load_weather_data_month(args.path, year, month)

        RED = "\033[31m"
        BLUE = "\033[34m"
        RESET = "\033[0m"

        print(month_abbr[month], year)

        for day_data in weather_data_month:
            max_str = []
            min_str = []
            max_temp = 0
            min_temp = 0
            if day_data['Max TemperatureC']:
                max_temp = (int)(day_data['Max TemperatureC'])
                min_temp = (int)(day_data['Min TemperatureC'])

            for i in range (0, max_temp):
                max_str.append('+')
            for i in range (0, min_temp):
                min_str.append('+')

            date = day_data['PKT']
            date_list = date.split('-')
            day = date_list[2]
            maxString = "".join(max_str)
            minString = "".join(min_str)

            if(max_temp != 0):
                #print(f"{day} {RED}{maxString}{RESET} {max_temp}C")
                #print(f"{day} {BLUE}{minString}{RESET} {min_temp}C")

                # Bonus Task
                print(f"{day} {BLUE}{minString}{RESET}{RED}{maxString}{RESET} {max_temp}C - {min_temp}C")


if __name__ == "__main__":
    main()
