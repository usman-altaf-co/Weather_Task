import calendar
import csv
import os


class WeatherDataLoader:
    def __init__(self, weather_files_directory):
        self.weather_files_directory = weather_files_directory
        self.required_labels = [
            "PKT",
            "PKST",
            "Max TemperatureC",
            "Min TemperatureC",
            "Mean Humidity"
        ]

    def read_weather_file(self, year, month_abbr):
        """
        Opens a CSV weather data file and reads the data into a list of dictionaries,
        filtering out unnecessary keys based on required_labels.

        Args:
        - year (int): The specific year for which data is required.
        - month_abbr (str):

        Returns:
        - list: A list of dictionaries, where each dictionary represents a day's
          weather record for a month. Each dictionary contains only the keys specified
          in required_labels.
        """
        murree_weather_file = f"Murree_weather_{year}_{month_abbr}.txt"

        weather_data_file_path = os.path.join(
            self.weather_files_directory, murree_weather_file
        )

        month_weather_readings = []

        if not os.path.isfile(weather_data_file_path):
            return month_weather_readings

        with open(weather_data_file_path, mode="r") as weather_data_file:
            csv_reader = csv.DictReader(weather_data_file)
            weather_data_headers = [header.strip() for header in csv_reader.fieldnames]

            for daily_weather_record in csv_reader:
                daily_weather_record = {
                    key.strip(): value
                    for key, value in daily_weather_record.items()
                }
                filtered_daily_weather_record = {
                    key: daily_weather_record[key]
                    for key in self.required_labels
                    if key in weather_data_headers
                }
                month_weather_readings.append(filtered_daily_weather_record)

        return month_weather_readings

    def load_weather_readings(self, year, month=None):
        """
        Loads weather readings for a specified year or month.

        Args:
        - year (int): Year for which weather data is to be loaded.
        - month (int/str, optional): Month for which weather data is to be loaded.
          If None, data for the entire year is loaded.

        Returns:
        - list: Combined list of weather records for the specified time period.
        """
        months_to_load = []
        weather_readings = []

        if month:
            month_abbr = calendar.month_abbr[month]
            months_to_load.append(month_abbr)
        else:
            months_to_load = calendar.month_abbr[1:]

        for month_abbr in months_to_load:
            month_weather_data = self.read_weather_file(year, month_abbr)
            weather_readings.extend(month_weather_data)

        return weather_readings
