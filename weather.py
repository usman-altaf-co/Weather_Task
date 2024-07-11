import argparse
import os
import calendar
import csv

required_labels = [
    "PKT", "PKST", "Max TemperatureC", "Min TemperatureC", "Mean Humidity"
]

month_abbr_map = {index: month for index, month in enumerate(calendar.month_abbr) if month}


def read_weather_file(weather_file_path):
    murree_weather_month = []
    if not os.path.isfile(weather_file_path):
        return murree_weather_month

    with open(weather_file_path, mode="r") as file:
        csv_reader = csv.DictReader(file)
        headers = [header.strip() for header in csv_reader.fieldnames]
        for row in csv_reader:
            row = {key.strip(): value for key, value in row.items()}
            filtered_row = {key: row[key] for key in required_labels if key in headers}

            murree_weather_month.append(filtered_row)

    return murree_weather_month


def load_yearly_weather_data(directory_path, year):
    year_weather_data = []

    for month in month_abbr_map.keys():
        if not month:
            continue

        monthly_data = load_monthly_weather_data(directory_path, year, month)
        year_weather_data.extend(monthly_data)

    return year_weather_data


def load_monthly_weather_data(directory_path, year, month):
    murree_weather_file = f"Murree_weather_{year}_{month_abbr_map[month]}.txt"
    full_file_path = os.path.join(directory_path, murree_weather_file)
    return read_weather_file(full_file_path)


def calculate_yearly_stats(weather_data):
    highest_temperature = float("-inf")
    lowest_temperature = float("inf")
    highest_humidity = 0

    highest_temprature_day = None
    lowest_temprature_day = None
    highest_humidity_day = None

    for daily_data in weather_data:
        date_key = "PKT" if "PKT" in daily_data else "PKST"

        if daily_data["Max TemperatureC"]:
            max_temp = int(daily_data["Max TemperatureC"])
            if max_temp > highest_temperature:
                highest_temperature = max_temp
                highest_temprature_day = daily_data[date_key]

            if max_temp < lowest_temperature:
                lowest_temperature = max_temp
                lowest_temprature_day = daily_data[date_key]

            if daily_data["Mean Humidity"]:
                max_humidity = int(daily_data["Mean Humidity"])
                if max_humidity > highest_humidity:
                    highest_humidity = max_humidity
                    highest_humidity_day = daily_data[date_key]

    return {
        "Highest": (highest_temperature, highest_temprature_day),
        "Lowest": (lowest_temperature, lowest_temprature_day),
        "Humidity": (highest_humidity, highest_humidity_day)
    }


def calculate_monthly_stats(weather_data):
    high_temperatures = []
    low_temperatures = []
    mean_humidities = []

    for daily_data in weather_data:
        if daily_data["Max TemperatureC"]:
            high_temperatures.append(int(daily_data["Max TemperatureC"]))

        if daily_data["Min TemperatureC"]:
            low_temperatures.append(int(daily_data["Min TemperatureC"]))

        if daily_data["Mean Humidity"]:
            mean_humidities.append(int(daily_data["Mean Humidity"]))

    avg_high_temprature = sum(high_temperatures) / len(high_temperatures)
    avg_low_temprature = sum(low_temperatures) / len(low_temperatures)
    avg_mean_humidity = sum(mean_humidities) / len(mean_humidities)

    return {
        "Average Highest Temperature": avg_high_temprature,
        "Average Lowest Temperature": avg_low_temprature,
        "Average Mean Humidity": avg_mean_humidity
    }


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=str)
    parser.add_argument("-e", "--year", type=int)
    parser.add_argument("-a", "--year_month", type=str)
    parser.add_argument("-c", "--chart", type=str,)
    return parser.parse_args()


def print_yearly_stats(stats):
    high_temprature, high_day = stats["Highest"]
    low_temprature, low_day = stats["Lowest"]
    humid_val, humid_day = stats["Humidity"]

    date_high = high_day.split("-")
    date_low = low_day.split("-")
    date_humid = humid_day.split("-")

    print(f"Highest: {high_temprature}C on {month_abbr_map[int(date_high[1])]} {date_high[2]}")
    print(f"Lowest: {low_temprature}C on {month_abbr_map[int(date_low[1])]} {date_low[2]}")
    print(f"Humidity: {humid_val}% on {month_abbr_map[int(date_humid[1])]} {date_humid[2]}")
    print("\n")


def print_monthly_stats(stats):
    print(f"Highest Average Temperature: {stats["Average Highest Temperature"]:.0f}C")
    print(f"Lowest Average Temperature: {stats["Average Lowest Temperature"]:.0f}C")
    print(f"Average Mean Humidity: {stats["Average Mean Humidity"]:.0f}%")
    print("\n")


def display_weather_chart(month, year, weather_data):
    RED = "\033[31m"
    BLUE = "\033[34m"
    RESET = "\033[0m"

    print(month_abbr_map[month], year)

    for day_data in weather_data:
        max_str = []
        min_str = []
        max_temprature = 0
        min_temprature = 0
        if day_data["Max TemperatureC"]:
            max_temprature = int(day_data["Max TemperatureC"])
            min_temprature = int(day_data["Min TemperatureC"])

        for i in range(0, max_temprature):
            max_str.append("+")
        for i in range(0, min_temprature):
            min_str.append("+")

        if "PKT" in day_data:
            day = day_data["PKT"].split("-")[2]
        else:
            day = day_data["PKST"].split("-")[2]

        maxString = "".join(max_str)
        minString = "".join(min_str)

        if max_temprature != 0:
            # print(f"{day} {RED}{maxString}{RESET} {max_temp}C")
            # print(f"{day} {BLUE}{minString}{RESET} {min_temp}C")

            # Bonus Task
            print(f"{day} {BLUE}{minString}{RESET}{RED}{maxString}{RESET} {min_temprature}C - {max_temprature}C")


def main():
    args = parse_arguments()

    if args.year:
        yearly_weather_data = load_yearly_weather_data(args.directory, args.year)
        yearly_stats = calculate_yearly_stats(yearly_weather_data)
        print_yearly_stats(yearly_stats)

    if args.year_month:
        year, month = map(int, args.year_month.split("/"))
        monthly_weather_data = load_monthly_weather_data(args.directory, year, month)
        monthly_stats = calculate_monthly_stats(monthly_weather_data)
        print_monthly_stats(monthly_stats)

    if args.chart:
        year, month = map(int, args.chart.split("/"))
        monthly_weather_data = load_monthly_weather_data(args.directory, year, month)
        display_weather_chart(month, year, monthly_weather_data)


main()
