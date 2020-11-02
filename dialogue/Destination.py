from dialogue import NavHelper


class Destination:
    def __init__(self, name, coordinate, distance):
        self.name = name
        self.coordinate = coordinate
        self.distance = distance
        self.dest_type = NavHelper.parse_destination_type(name)




