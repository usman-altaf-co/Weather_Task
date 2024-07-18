class WeatherDataAnalyzer:
    @staticmethod
    def calculate_extremes(year_weather_data, key, comparison):
        """
        Helper function to calculate extremes for a specific key (Weather Parameter).

        Args:
        - year_weather_data (str): List having whole year's weather data.
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
                    extreme_day = daily_weather_record.get(
                        "PKT", daily_weather_record.get("PKST")
                    )

        return extreme_value, extreme_day

    @staticmethod
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
        (highest_temperature,
         highest_temperature_day) = WeatherDataAnalyzer.calculate_extremes(
            year_weather_data, "Max TemperatureC", lambda x, y: x > y
        )

        (lowest_temperature,
         lowest_temperature_day) = WeatherDataAnalyzer.calculate_extremes(
            year_weather_data, "Min TemperatureC", lambda x, y: x < y
        )

        (highest_humidity,
         highest_humidity_day) = WeatherDataAnalyzer.calculate_extremes(
            year_weather_data, "Mean Humidity", lambda x, y: x > y
        )

        return {
            "Highest": (highest_temperature, highest_temperature_day),
            "Lowest": (lowest_temperature, lowest_temperature_day),
            "Humidity": (highest_humidity, highest_humidity_day)
        }

    @staticmethod
    def calculate_average(month_weather_data, key):
        """
        Helper function to calculate the average value for a specific weather parameter.

        Args:
        - month_weather_data (List): List of dictionaries containing whole month's weather records.
        - key (str): Key representing the weather parameter ("Max TemperatureC",
          "Min TemperatureC", or "Mean Humidity").

        Returns:
        - float: Average value of the specified key across all days with available data.
        """
        values = [
            int(daily_weather_record[key])
            for daily_weather_record
            in month_weather_data
            if daily_weather_record.get(key)
        ]

        return int(sum(values) / len(values))

    @staticmethod
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
        avg_high_temperature = (WeatherDataAnalyzer.calculate_average
                                (month_weather_data, "Max TemperatureC"))
        avg_low_temperature = (WeatherDataAnalyzer.calculate_average
                               (month_weather_data, "Min TemperatureC"))
        avg_mean_humidity = (WeatherDataAnalyzer.calculate_average
                             (month_weather_data, "Mean Humidity"))

        return {
            "Average Highest Temperature": avg_high_temperature,
            "Average Lowest Temperature": avg_low_temperature,
            "Average Mean Humidity": avg_mean_humidity
        }
