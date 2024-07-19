from weather_analyzer import WeatherDataAnalyzer
from weather_data_loader import WeatherDataLoader
from weather_display import WeatherDataPresenter
from cmd_line_argument_parser import CommandLineArgumentParser


class WeatherDataProcessor:
    def __init__(self):
        self.weather_data_loader = None
        self.parser = CommandLineArgumentParser()
        self.weather_data_analyzer = None

    def process_weather_data(self):
        args = self.parser.parse_arguments()
        self.weather_data_loader = WeatherDataLoader(args.directory)

        if args.year:
            year_weather_data = (self.weather_data_loader.load_weather_readings(args.year))

            WeatherDataAnalyzer.set_year_weather_readings(year_weather_data)

            weather_extremes = (WeatherDataAnalyzer.calculate_year_weather_extremes())

            WeatherDataPresenter.display_year_weather_extremes(weather_extremes)

        if args.year_month:
            year, month = map(int, args.year_month.split("/"))

            month_weather_readings = (
                self.weather_data_loader.load_weather_readings(year, month)
            )
            month_weather_averages = (
                WeatherDataAnalyzer.calculate_month_averages(month_weather_readings)
            )

            WeatherDataPresenter.display_month_averages(month_weather_averages)

        if args.chart:
            year, month = map(int, args.chart.split("/"))

            month_weather_readings = (self.weather_data_loader.
                                      load_weather_readings(year, month))

            WeatherDataPresenter.display_weather_chart(args.chart, month_weather_readings)
