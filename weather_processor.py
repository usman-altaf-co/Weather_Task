from weather_analyzer import WeatherDataAnalyzer
from weather_data import WeatherDataLoader
from weather_display import WeatherDataPresenter
from weather_parser import CommandLineArgumentParser


class WeatherDataHandler:
    def __init__(self):
        self.weather_data_loader = None
        self.parser = CommandLineArgumentParser()

    def process_weather_data(self):
        args = self.parser.parse_arguments()
        self.weather_data_loader = WeatherDataLoader(args.directory)

        if args.year:
            year_weather_data = (self.weather_data_loader.
                                 load_weather_data(args.year))
            weather_extremes = (WeatherDataAnalyzer.calculate_year_extremes
                                (year_weather_data))

            WeatherDataPresenter.show_year_extremes(weather_extremes)

        if args.year_month:
            year, month = map(int, args.year_month.split("/"))

            month_weather_data = (self.weather_data_loader.
                                  load_weather_data(year, month))
            month_weather_averages = (WeatherDataAnalyzer.
                                      calculate_month_averages
                                      (month_weather_data))

            WeatherDataPresenter.show_month_averages(month_weather_averages)

        if args.chart:
            year, month = map(int, args.chart.split("/"))

            month_weather_data = (self.weather_data_loader.
                                  load_weather_data(year, month))

            WeatherDataPresenter.display_weather_chart(month, year, month_weather_data)
