class Heading:
    def __init__(self, w, x, y, z):
        self.w = w
        self.x = x
        self.y = y
        self.z = z


class Position:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


class SensorPose:
    def __init__(self, heading: Heading, position: Position):
        self.heading = heading
        self.position = position
