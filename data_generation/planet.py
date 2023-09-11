class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Planet:
    def __init__(self, m, x=0, y=0, vx=0, vy=0, init_first_position=True):
        self.m: float = m
        if init_first_position:
            self.positions = [Position(x, y)]  # array of positions
        else:
            self.positions = []
        self.vx: float = vx
        self.vy: float = vy
        self.Fwx: float = 0
        self.Fwy: float = 0

    def next(self, delta):
        ax = self.Fwx / self.m
        ay = self.Fwy / self.m

        # order is important
        self.positions.append(Position(
            self.positions[-1].x + (self.vx * delta) + (0.5 * ax * (delta ** 2)),
            self.positions[-1].y + (self.vy * delta) + (0.5 * ay * (delta ** 2))
        ))

        self.vx += ax * delta
        self.vy += ay * delta

        self.Fwx = 0
        self.Fwy = 0

    def toDict(self):
        result = {
            "mass": self.m,
            "positions": []
        }

        for position in self.positions:
            result["positions"].append({
                "x": position.x,
                "y": position.y
            })

        return result
