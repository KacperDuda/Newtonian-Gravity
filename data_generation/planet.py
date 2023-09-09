class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Planet:
    def __init__(self, m, x, y, vx, vy):
        self.m: float = m
        self.positions = [Position(x, y)]  # array of positions
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