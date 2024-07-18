import calendar


class WeatherDataPresenter:
    @staticmethod
    def show_year_extremes(weather_extremes):
        """
        Print yearly extremes for maximum temperature, minimum temperature, and
        mean humidity.

        Args:
        - weather_extremes (dict): Dictionary containing the extremes.
          Keys: "Highest", "Lowest", "Humidity".
          Values: Tuples (extreme_value, extreme_day) for each category.
        """
        (highest_temperature,
         highest_temperature_day) = weather_extremes["Highest"]

        (lowest_temperature,
         lowest_temperature_day) = weather_extremes["Lowest"]

        (max_humidity_value,
         most_humid_day) = weather_extremes["Humidity"]

        highest_temperature_day = highest_temperature_day.split("-")
        lowest_temperature_day = lowest_temperature_day.split("-")
        most_humid_day = most_humid_day.split("-")

        highest_temperature_month = highest_temperature_day[1]
        lowest_temperature_month = lowest_temperature_day[1]
        most_humid_month = most_humid_day[1]

        highest_temperature_day = highest_temperature_day[2]
        lowest_temperature_day = lowest_temperature_day[2]
        most_humid_day = most_humid_day[2]

        print(
            f"Highest: {highest_temperature}C on "
            f"{calendar.month_abbr[int(highest_temperature_month)]} "
            f"{highest_temperature_day}"
        )
        print(
            f"Lowest: {lowest_temperature}C on "
            f"{calendar.month_abbr[int(lowest_temperature_month)]} "
            f"{lowest_temperature_day}"
        )
        print(
            f"Humidity: {max_humidity_value}% on "
            f"{calendar.month_abbr[int(most_humid_month)]} "
            f"{most_humid_day}"
        )

    @staticmethod
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

    @staticmethod
    def create_temperature_bars(day_weather_record):
        """
        Create temperature bars based on the maximum and minimum temperatures
        for a given day's weather record.

        Args:
        - day_weather_record (dict): Dictionary representing a day's weather record.

        Returns:
        - tuple: Tuple containing the created temperature bars and the respective temperatures.
        """
        max_temperature = int(day_weather_record.get("Max TemperatureC", 0))
        min_temperature = int(day_weather_record.get("Min TemperatureC", 0))

        max_temperature_bar = "+" * max_temperature
        min_temperature_bar = "+" * min_temperature

        return (
            max_temperature_bar,
            min_temperature_bar,
            max_temperature,
            min_temperature
        )

    @staticmethod
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
            (max_temperature_bar,
             min_temperature_bar,
             max_temperature,
             min_temperature) = (WeatherDataPresenter.
                                 create_temperature_bars(daily_weather_record))
            day = daily_weather_record.get("PKT",
                                           daily_weather_record.get("PKST")).split("-")[2]

            print(f"{day} {BLUE}{min_temperature_bar}{RESET}"
                  f"{RED}{max_temperature_bar}{RESET}"
                  f" {min_temperature}C - {max_temperature}C")
