import re

from tsp.city import City


class CitiesReader:
    @staticmethod
    def read(file_path: str, scaling_factor=1):
        cities = []
        with open(file_path, "r") as f:
            lines = f.readlines()
            sep = "," if "," in lines[0] else "\s+"
            for line in lines:
                temp = re.compile(sep).split(line)
                cities.append(City(float(temp[0]) * scaling_factor, float(temp[1]) * scaling_factor))
        return cities
