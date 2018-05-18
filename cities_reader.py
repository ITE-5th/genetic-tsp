import re

from tsp.city import City


class CitiesReader:
    @staticmethod
    def read(file_path: str, sep="\s+"):
        cities = []
        with open(file_path, "r") as f:
            for line in f:
                temp = re.compile(sep).split(line)
                cities.append(City(float(temp[0]), float(temp[1])))
        return cities
