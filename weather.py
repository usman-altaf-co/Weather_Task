import argparse
import os


def load_weather_data(file_path, year):
    weather_data = []
    #day_data = {}

    months = ['Jan', 'Feb', 'Mar', 'Apr',
        'May', 'Jun', 'Jul', 'Aug',
        'Sep', 'Oct', 'Nov', 'Dec']

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

                #for label, value in zip(labels, values):
                #    day_data[label] = value

                # Dictionary Comprehension, Creating and Converting tuple into dictionary's key-value pairs
                day_data = {label: value for label, value in zip(labels, values)}
                #for i in range(len(labels)):
                #    day_data[labels[i]] = values[i]
                weather_data.append(day_data)

    return weather_data

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

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=str)
    parser.add_argument("-e", type=int)
    parser.add_argument("-a", type=str)
    parser.add_argument("-c", type=str)

    return parser.parse_args()


def main():
    args = parse_args()

    #print("Path to files directory:", args.path)

    if args.e:
        year = args.e
        #print("Year for -e option:", args.e)
        weather_data = load_weather_data(args.path, year)
        #print(weather_data[30])
        stats = calculate_stats(weather_data)

        month_abbr = {1: 'Jan', 2: 'Feb', 3: 'Mar',
                      4: 'Apr', 5: 'May', 6: 'Jun',
                      7: 'Jul', 8: 'Aug', 9: 'Sep',
                      10: 'Oct', 11: 'Nov', 12: 'Dec'}


        date_high = stats['Highest'][1].split('-')
        date_low = stats['Lowest'][1].split('-')
        date_humid = stats['Humidity'][1].split('-')

        high_val = stats['Highest'][0]
        low_val = stats['Lowest'][0]
        humid_val = stats['Highest'][0]


       # print(month_abbr[(int)(date_high[1])])
        print(f"Highest: {high_val} on {month_abbr[(int)(date_high[1])]} {date_high[2]} ")
        print(f"Lowest: {low_val} on {month_abbr[(int)(date_low[1])]} {date_low[2]} ")
        print(f"Humidity: {humid_val}% on {month_abbr[(int)(date_humid[1])]} {date_humid[2]} ")


    if args.a:
        year_str, month_str = args.a.split('/')
        year = int(year_str)
        month = int(month_str)
        print("Year for -c option:", year)
        print("Month for -c option:", month)

    if args.c:
        year_str, month_str = args.a.split('/')
        year = int(year_str)
        month = int(month_str)
        print("Year for -c option:", year)
        print("Month for -c option:", month)


if __name__ == "__main__":
    main()
