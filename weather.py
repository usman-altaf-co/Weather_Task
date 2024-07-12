import argparse
import calendar
import csv
import os

required_labels = [
    "PKT", "PKST", "Max TemperatureC", "Min TemperatureC", "Mean Humidity"
]


def read_weather_file(weather_file_path):
    monthly_weather_data = []
    if not os.path.isfile(weather_file_path):
        return monthly_weather_data

    with open(weather_file_path, mode="r") as file:
        csv_reader = csv.DictReader(file)
        headers = [header.strip() for header in csv_reader.fieldnames]
        for daily_weather_record in csv_reader:
            daily_weather_record = {
                key.strip(): value
                for key, value in daily_weather_record.items()
            }
            filtered_daily_record = {
                key: daily_weather_record[key]
                for key in required_labels
                if key in headers
            }
            monthly_weather_data.append(filtered_daily_record)

    return monthly_weather_data


def load_yearly_weather_data(directory_path, year):
    year_weather_data = []

    for month in range(1, 13):
        monthly_data = load_monthly_weather_data(directory_path, year, month)
        year_weather_data.extend(monthly_data)

    return year_weather_data


def load_monthly_weather_data(directory_path, year, month):
    murree_weather_file = f"Murree_weather_{year}_{calendar.month_abbr[month]}.txt"
    full_file_path = os.path.join(directory_path, murree_weather_file)
    return read_weather_file(full_file_path)


def calculate_extremes(key, weather_data, comparison, extreme_value, extreme_day):
    for daily_data in weather_data:
        if daily_data[key]:
            current_value = int(daily_data[key])
            if comparison(current_value, extreme_value):
                extreme_value = current_value
                extreme_day = daily_data.get("PKT", daily_data.get("PKST"))

    return extreme_value, extreme_day


def calculate_yearly_extremes(weather_data):
    highest_temperature = float("-inf")
    lowest_temperature = float("inf")
    highest_humidity = 0

    highest_temprature_day = None
    lowest_temprature_day = None
    highest_humidity_day = None

    highest_temperature, highest_temprature_day = calculate_extremes(
        "Max TemperatureC", weather_data, lambda x,y : x > y, highest_temperature, highest_temprature_day)

    lowest_temperature, lowest_temprature_day = calculate_extremes(
        "Min TemperatureC", weather_data, lambda x, y: x < y, lowest_temperature, lowest_temprature_day)

    highest_humidity, highest_humidity_day = calculate_extremes(
        "Mean Humidity", weather_data, lambda x, y: x > y, highest_humidity, highest_humidity_day)

    return {
        "Highest": (highest_temperature, highest_temprature_day),
        "Lowest": (lowest_temperature, lowest_temprature_day),
        "Humidity": (highest_humidity, highest_humidity_day)
    }


def calculate_monthly_averages(weather_data):
    def calculate_average(key):
        values = [
            int(daily_data[key])
            for daily_data in weather_data if daily_data.get(key)
        ]
        return sum(values) / len(values)

    avg_high_temprature = calculate_average("Max TemperatureC")
    avg_low_temprature = calculate_average("Min TemperatureC")
    avg_mean_humidity = calculate_average("Mean Humidity")

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

    print(f"Highest: {high_temprature}C on {calendar.month_abbr[int(date_high[1])]} {date_high[2]}")
    print(f"Lowest: {low_temprature}C on {calendar.month_abbr[int(date_low[1])]} {date_low[2]}")
    print(f"Humidity: {humid_val}% on {calendar.month_abbr[int(date_humid[1])]} {date_humid[2]}")


def print_monthly_stats(stats):
    print(f"Highest Average Temperature: {stats["Average Highest Temperature"]:.0f}C")
    print(f"Lowest Average Temperature: {stats["Average Lowest Temperature"]:.0f}C")
    print(f"Average Mean Humidity: {stats["Average Mean Humidity"]:.0f}%")


def create_temperature_bars(day_data):
    max_temprature = 0
    min_temprature = 0
    if day_data["Max TemperatureC"]:
        max_temprature = int(day_data["Max TemperatureC"])
        min_temprature = int(day_data["Min TemperatureC"])
    max_bar = "+" * max_temprature
    min_bar = "+" * min_temprature

    return max_bar, min_bar, max_temprature, min_temprature


def display_weather_chart(month, year, weather_data):
    RED = "\033[31m"
    BLUE = "\033[34m"
    RESET = "\033[0m"

    print(calendar.month_abbr[month], year)
    for day_data in weather_data:
        max_temp_bar , min_temp_bar, max_temprature, min_temprature = create_temperature_bars(day_data)
        day = day_data.get("PKT", day_data.get("PKST")).split("-")[2]

        if max_temprature != 0:
            print(f"{day} {BLUE}{min_temp_bar}{RESET}"
                  f"{RED}{max_temp_bar}{RESET}"
                  f" {min_temprature}C - {max_temprature}C")


def main():
    args = parse_arguments()

    if args.year:
        yearly_weather_data = load_yearly_weather_data(args.directory, args.year)
        yearly_stats = calculate_yearly_extremes(yearly_weather_data)
        print_yearly_stats(yearly_stats)

    if args.year_month:
        year, month = map(int, args.year_month.split("/"))
        monthly_weather_data = load_monthly_weather_data(args.directory, year, month)
        monthly_stats = calculate_monthly_averages(monthly_weather_data)
        print_monthly_stats(monthly_stats)

    if args.chart:
        year, month = map(int, args.chart.split("/"))
        monthly_weather_data = load_monthly_weather_data(args.directory, year, month)
        display_weather_chart(month, year, monthly_weather_data)


main()
