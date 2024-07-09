import argparse
import os
import csv


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=str, help="Path to files directory")
    parser.add_argument("-e", type=int, help="Specify the year to load data for")
    parser.add_argument("-a", type=str, help="Option A")
    parser.add_argument("-c", type=str, help="Option C")
    return parser.parse_args()


def load_weather_data(file_path, year):
    weather_data = []

    # Loop through months to find the appropriate files
    for month in range(1, 13):
        file_name = f"Murree_weather_{year}_{month:02d}.txt"
        full_path = os.path.join(file_path, file_name)

        if not os.path.isfile(full_path):
            continue

        with open(full_path, mode='r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                weather_data.append(dict(row))

    return weather_data


def main():
    args = parse_args()

    print("Path to files directory:", args.path)

    if args.e:
        year = args.e
        print("Loading weather data for year:", year)
        weather_data = load_weather_data(args.path, year)
        print(f"Loaded {len(weather_data)} records for year {year}")

    if args.a:
        year_str, month_str = args.a.split('/')
        year = int(year_str)
        month = int(month_str)
        print("Year for -a option:", year)
        print("Month for -a option:", month)

    if args.c:
        year_str, month_str = args.c.split('/')
        year = int(year_str)
        month = int(month_str)
        print("Year for -c option:", year)
        print("Month for -c option:", month)


if __name__ == "__main__":
    main()
