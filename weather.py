import argparse
import calendar
import csv
import os

required_labels = [
    "PKT", "PKST", "Max TemperatureC", "Min TemperatureC", "Mean Humidity"
]


def read_weather_file(weather_data_file):
    """
    Opens a CSV weather data file and reads the data into a list of dictionaries,
    filtering out unnecessary keys based on required_labels.

    Args:
    - weather_data_file (str): Path to the weather data file in CSV format.

    Returns:
    - list: A list of dictionaries, where each dictionary represents a day's
      weather record for a month. Each dictionary contains only the keys specified
      in required_labels.
    """
    month_weather_data = []
    if not os.path.isfile(weather_data_file):
        return month_weather_data

    with open(weather_data_file, mode="r") as file:
        csv_reader = csv.DictReader(file)
        headers = [header.strip() for header in csv_reader.fieldnames]
        for daily_weather_record in csv_reader:
            daily_weather_record = {
                key.strip(): value
                for key, value in daily_weather_record.items()
            }
            filtered_daily_weather_record = {
                key: daily_weather_record[key]
                for key in required_labels
                if key in headers
            }
            month_weather_data.append(filtered_daily_weather_record)

    return month_weather_data


def load_year_weather_data(weather_files_directory, year):
    """
    Loads weather data for a specified year from multiple monthly files.

    Args:
    - weather_files_directory (str): Directory path where weather files are stored.
    - year (int): Year for which weather data is to be loaded.

    Returns:
    - list: Combined list of weather records for the entire year.
    """
    year_weather_data = []

    for month_abbr in calendar.month_abbr[1:]:
        month_weather_data = load_month_weather_data(weather_files_directory, year, month_abbr)
        year_weather_data.extend(month_weather_data)

    return year_weather_data


def load_month_weather_data(weather_files_directory, year, month):
    """
    Loads weather data for a specified month from a file.

    Args:
    - weather_files_directory (str): Directory path where weather files are stored.
    - year (int): Year of the weather data.
    - month (int/str): Month of the weather data (numeric or abbreviation).

    Returns:
    - list: List of dictionaries where each dictionary represents daily weather
      records for the specified month.
    """
    if isinstance(month, int):
        month_abbr = calendar.month_abbr[month]
    else:
        month_abbr = month
    murree_weather_file = f"Murree_weather_{year}_{month_abbr}.txt"
    weather_data_file_path = os.path.join(weather_files_directory, murree_weather_file)
    return read_weather_file(weather_data_file_path)


def calculate_year_extremes(year_weather_data):
    """
    Calculates yearly extremes for maximum temperature, minimum temperature, and
    mean humidity based on the provided weather data.

    Args:
    - year_weather_data (list): List of dictionaries where each dictionary represents
      daily weather records for a year.

    Returns:
    - dict: Dictionary containing the calculated extremes.
      Keys: "Highest", "Lowest", "Humidity".
      Values: Tuples (extreme_value, extreme_day) for each category.
    """
    def calculate_extremes(key, comparison):
        """
        Helper function to calculate extremes for a specific key (Weather Parameter).

        Args:
        - key (str): Key representing the weather parameter ("Max TemperatureC",
          "Min TemperatureC", or "Mean Humidity").
        - comparison (function): Comparison function (e.g., lambda x, y: x > y) to
          determine whether a value is an extreme.

        Returns:
        - tuple: Tuple containing the extreme value and the corresponding day.
        """
        if key == "Max TemperatureC":
            extreme_value = float("-inf")
        elif key == "Min TemperatureC":
            extreme_value = float("inf")
        else:
            extreme_value = 0

        extreme_day = None

        for daily_weather_record in year_weather_data:
            if daily_weather_record[key]:
                current_value = int(daily_weather_record[key])
                if comparison(current_value, extreme_value):
                    extreme_value = current_value
                    extreme_day = daily_weather_record.get("PKT", daily_weather_record.get("PKST"))

        return extreme_value, extreme_day

    highest_temperature, highest_temperature_day = calculate_extremes(
        "Max TemperatureC", lambda x, y: x > y
    )

    lowest_temperature, lowest_temperature_day = calculate_extremes(
        "Min TemperatureC", lambda x, y: x < y
    )

    highest_humidity, highest_humidity_day = calculate_extremes(
        "Mean Humidity", lambda x, y: x > y
    )

    return {
        "Highest": (highest_temperature, highest_temperature_day),
        "Lowest": (lowest_temperature, lowest_temperature_day),
        "Humidity": (highest_humidity, highest_humidity_day)
    }


def calculate_month_averages(month_weather_data):
    """
    Calculates monthly averages for highest temperature, lowest temperature, and
    mean humidity based on the provided month's weather data.

    Args:
    - month_weather_data (list): List of dictionaries where each dictionary represents
      daily weather records for a month.

    Returns:
    - dict: Dictionary containing the calculated averages.
      Keys: "Average Highest Temperature", "Average Lowest Temperature", "Average Mean Humidity".
    """
    def calculate_average(key):
        """
        Helper function to calculate the average value for a specific weather parameter.

        Args:
        - key (str): Key representing the weather parameter ("Max TemperatureC",
          "Min TemperatureC", or "Mean Humidity").

        Returns:
        - float: Average value of the specified key across all days with available data.
        """
        values = [
            int(daily_weather_record[key])
            for daily_weather_record in month_weather_data if daily_weather_record.get(key)
        ]
        return int(sum(values) / len(values))

    avg_high_temperature = calculate_average("Max TemperatureC")
    avg_low_temperature = calculate_average("Min TemperatureC")
    avg_mean_humidity = calculate_average("Mean Humidity")

    return {
        "Average Highest Temperature": avg_high_temperature,
        "Average Lowest Temperature": avg_low_temperature,
        "Average Mean Humidity": avg_mean_humidity
    }


def parse_arguments():
    """
    Parse command-line arguments using argparse.

    Returns:
    - argparse.Namespace: Parsed arguments object containing parsed arguments
      as attributes.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=str)
    parser.add_argument("-e", "--year", type=int)
    parser.add_argument("-a", "--year_month", type=str)
    parser.add_argument("-c", "--chart", type=str)
    return parser.parse_args()


def show_year_extremes(weather_extremes):
    """
    Print yearly extremes for maximum temperature, minimum temperature, and
    mean humidity.

    Args:
    - weather_extremes (dict): Dictionary containing the extremes.
      Keys: "Highest", "Lowest", "Humidity".
      Values: Tuples (extreme_value, extreme_day) for each category.
    """
    highest_temperature, highest_temperature_day = weather_extremes["Highest"]
    lowest_temperature, lowest_temperature_day = weather_extremes["Lowest"]
    max_humidity_value, most_humid_day = weather_extremes["Humidity"]

    highest_temperature_day = highest_temperature_day.split("-")
    lowest_temperature_day = lowest_temperature_day.split("-")
    most_humid_day = most_humid_day.split("-")

    print(
        f"Highest: {highest_temperature}C on "
        f"{calendar.month_abbr[int(highest_temperature_day[1])]} "
        f"{highest_temperature_day[2]}"
    )
    print(
        f"Lowest: {lowest_temperature}C on "
        f"{calendar.month_abbr[int(lowest_temperature_day[1])]} "
        f"{lowest_temperature_day[2]}"
    )
    print(
        f"Humidity: {max_humidity_value}% on "
        f"{calendar.month_abbr[int(most_humid_day[1])]} "
        f"{most_humid_day[2]}"
    )


def show_month_averages(month_weather_averages):
    """
    Print monthly averages for highest temperature, lowest temperature, and
    mean humidity.

    Args:
    - month_weather_averages (dict): Dictionary containing the averages.
      Keys: "Average Highest Temperature", "Average Lowest Temperature", "Average Mean Humidity".
      Values: Average values for each category.
    """
    print(
        f"Highest Average Temperature: "
        f"{month_weather_averages['Average Highest Temperature']}C"
    )
    print(
        f"Lowest Average Temperature: "
        f"{month_weather_averages['Average Lowest Temperature']}C"
    )
    print(
        f"Average Mean Humidity: "
        f"{month_weather_averages['Average Mean Humidity']}%"
    )


def create_temperature_bars(day_weather_record):
    """
    Create temperature bars based on the maximum and minimum temperatures
    for a given day's weather record.

    Args:
    - day_weather_record (dict): Dictionary representing a day's weather record.

    Returns:
    - tuple: Tuple containing the created temperature bars and the respective temperatures.
    """
    max_temperature = 0
    min_temperature = 0
    if day_weather_record["Max TemperatureC"]:
        max_temperature = int(day_weather_record["Max TemperatureC"])
        min_temperature = int(day_weather_record["Min TemperatureC"])
    max_temperature_bar = "+" * max_temperature
    min_temperature_bar = "+" * min_temperature

    return (
        max_temperature_bar,
        min_temperature_bar,
        max_temperature,
        min_temperature
    )


def display_weather_chart(month, year, month_weather_data):
    """
    Display a weather chart for a given month's weather data, showing
    temperature bars for each day.

    Args:
    - month (int): Month number (1-12).
    - year (int): Year of the weather data.
    - month_weather_data (list): List of dictionaries where each dictionary
      represents daily weather records for the specified month.
    """
    RED = "\033[31m"
    BLUE = "\033[34m"
    RESET = "\033[0m"

    print(calendar.month_abbr[month], year)
    for daily_weather_record in month_weather_data:
        (max_temperature_bar, min_temperature_bar,
         max_temperature, min_temperature) = create_temperature_bars(daily_weather_record)
        day = daily_weather_record.get("PKT", daily_weather_record.get("PKST")).split("-")[2]

        print(f"{day} {BLUE}{min_temperature_bar}{RESET}"
              f"{RED}{max_temperature_bar}{RESET}"
              f" {min_temperature}C - {max_temperature}C")


def main():
    """
    Main function to handle command-line arguments and execute weather data operations.
    """
    args = parse_arguments()

    if args.year:
        year_weather_data = load_year_weather_data(args.directory, args.year)
        weather_extremes = calculate_year_extremes(year_weather_data)
        show_year_extremes(weather_extremes)

    if args.year_month:
        year, month = map(int, args.year_month.split("/"))
        month_weather_data = load_month_weather_data(args.directory, year, month)
        month_weather_averages = calculate_month_averages(month_weather_data)
        show_month_averages(month_weather_averages)

    if args.chart:
        year, month = map(int, args.chart.split("/"))
        month_weather_data = load_month_weather_data(args.directory, year, month)
        display_weather_chart(month, year, month_weather_data)


main()
