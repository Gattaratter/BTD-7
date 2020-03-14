from MapElements.MapCell import MapCell
from MapElements.WayCell import WayCell


class MapLoader:
    def __init__(self):
        pass

    @staticmethod
    def from_file(file_name):
        # Todo
        pass

    @staticmethod
    def zwerg_101():
        grid = dict()
        for x in range(0, int(50)):  # 1600 pixel
            for y in range(0, int(34)):
                if y == 10 and x == 30:
                    grid[(x, y)] = WayCell(32, (x, y), (x - 1, y), (x, y + 1))
                elif 10 < y < 20 and x == 30:
                    grid[(x, y)] = WayCell(32, (x, y), (x, y - 1), (x, y + 1))
                elif y == 20 and x == 30:
                    grid[(x, y)] = WayCell(32, (x, y), (x, y - 1), (x + 1, y))
                elif y == 20 and 30 < x < 40:
                    grid[(x, y)] = WayCell(32, (x, y), (x - 1, y), (x + 1, y))
                elif y == 20 and x == 40:
                    grid[(x, y)] = WayCell(32, (x, y), (x - 1, y), (x, y - 1))
                elif 10 < y < 20 and x == 40:
                    grid[(x, y)] = WayCell(32, (x, y), (x, y + 1), (x, y - 1))
                elif y == 10 and x == 40:
                    grid[(x, y)] = WayCell(32, (x, y), (x, y + 1), (x + 1, y))
                elif y == 10 and (x > 40 or x < 30):
                    if x < 0:
                        grid[(x, y)] = WayCell(32, (x, y), (None, y), (x + 1, y))
                    elif x >= 60:
                        grid[(x, y)] = WayCell(32, (x, y), (x - 1, y), (None, y))
                    else:
                        grid[(x, y)] = WayCell(32, (x, y), (x - 1, y), (x + 1, y))
                else:
                    grid[(x, y)] = MapCell(32, (x, y), (x * 2, y * 2, x + y))
        return grid
