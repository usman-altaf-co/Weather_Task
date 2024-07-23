class WeatherDataAnalyzer:
    year_weather_readings = None

    @classmethod
    def set_year_weather_readings(cls, year_weather_readings):
        cls.year_weather_readings = year_weather_readings

    @classmethod
    def calculate_extreme_weather_values(cls, weather_attribute):
        """
        Helper function to calculate extremes for a specific weather_attribute (Weather Parameter).

        Args:
        - weather_attribute (str): weather_attribute representing the weather parameter ("Max TemperatureC",
          "Min TemperatureC", or "Mean Humidity").
          determine whether a value is an extreme.

        Returns:
        - tuple: Tuple containing the extreme value and the corresponding day.
        """
        weather_attribute_values = [
            int(weather_record[weather_attribute])
            for weather_record in cls.year_weather_readings
            if weather_record[weather_attribute]
        ]

        if weather_attribute == "Max TemperatureC" or weather_attribute == "Mean Humidity":
            extreme_weather_value = max(weather_attribute_values)
        elif weather_attribute == "Min TemperatureC":
            extreme_weather_value = min(weather_attribute_values)
        else:
            raise ValueError(f"Unknown weather attribute: {weather_attribute}")

        extreme_weather_day = None

        for daily_weather_record in cls.year_weather_readings:
            if (daily_weather_record[weather_attribute] and
                    int(daily_weather_record[weather_attribute]) == extreme_weather_value):

                extreme_weather_day = daily_weather_record.get("PKT", daily_weather_record.get("PKST"))

        return extreme_weather_value, extreme_weather_day

    @classmethod
    def calculate_year_weather_extremes(cls):
        """
        Calculates yearly extremes for maximum temperature, minimum temperature, and
        mean humidity based on the provided weather data.

        Returns:
        - dict: Dictionary containing the calculated extremes.
          weather_attributes: "Highest", "Lowest", "Humidity".
          Values: Tuples (extreme_value, extreme_day) for each category.
        """

        return {
            "Highest": cls.calculate_extreme_weather_values("Max TemperatureC"),
            "Lowest": cls.calculate_extreme_weather_values("Min TemperatureC"),
            "Humidity": cls.calculate_extreme_weather_values("Mean Humidity")
        }

    @staticmethod
    def calculate_average(month_weather_readings, weather_attribute):
        """
        Helper function to calculate the average value for a specific weather parameter.

        Args:
        - month_weather_data (List): List of dictionaries containing whole month's weather records.
        - weather_attribute (str): weather_attribute representing the weather parameter ("Max TemperatureC",
          "Min TemperatureC", or "Mean Humidity").

        Returns:
        - float: Average value of the specified weather_attribute across all days with available readings.
        """
        values = [
            int(daily_weather_record[weather_attribute])
            for daily_weather_record
            in month_weather_readings
            if daily_weather_record.get(weather_attribute)
        ]

        return int(sum(values) / len(values))

    @classmethod
    def calculate_month_averages(cls, month_weather_readings):
        """
        Calculates monthly averages for highest temperature, lowest temperature, and
        mean humidity based on the provided month's weather data.

        Args:
        - month_weather_data (list): List of dictionaries where each dictionary represents
          daily weather records for a month.

        Returns:
        - dict: Dictionary containing the calculated averages.
          weather_attributes: "Average Highest Temperature", "Average Lowest Temperature", "Average Mean Humidity".
        """
        return {
            "Average Highest Temperature": cls.calculate_average(
                month_weather_readings,
                "Max TemperatureC"
            ),
            "Average Lowest Temperature": cls.calculate_average(
                month_weather_readings,
                "Min TemperatureC"
            ),
            "Average Mean Humidity": cls.calculate_average(
                month_weather_readings,
                "Mean Humidity"
            )
        }
