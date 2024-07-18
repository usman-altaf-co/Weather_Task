import argparse


class CommandLineArgumentParser:
    @staticmethod
    def parse_arguments():
        """
        Parse command-line arguments using argparse.
        """
        parser = argparse.ArgumentParser()

        parser.add_argument("directory", type=str)
        parser.add_argument("-e", "--year", type=int)
        parser.add_argument("-a", "--year_month", type=str)
        parser.add_argument("-c", "--chart", type=str)

        return parser.parse_args()
