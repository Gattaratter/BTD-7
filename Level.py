import json

from Bloons.BasicBloons import RedBloon, BlueBloon, GreenBloon, YellowBloon


class Level:
    """ class representing a level including waves and bloons with their respective spawn times """

    def __init__(self, waves):
        self.spawn_pos = (0, 10)
        self.spawn = False
        self.curr_wave_time = 0
        self.curr_wave = 1
        self.waves = waves

    def update(self, bloons):
        for bloon_type in self.waves[self.curr_wave].get(self.curr_wave_time, []):
            if bloon_type == "RedBloon":
                bloons.append(RedBloon(*self.spawn_pos))
            elif bloon_type == "BlueBloon":
                bloons.append(BlueBloon(*self.spawn_pos))
            elif bloon_type == "GreenBloon":
                bloons.append(GreenBloon(*self.spawn_pos))
            elif bloon_type == "YellowBloon":
                bloons.append(YellowBloon(*self.spawn_pos))
            else:
                print("Can't parse bloon type: %s", bloon_type)

        if self.is_wave_finished():
            self.spawn = False
            if self.curr_wave < max(self.waves.keys()):
                self.curr_wave += 1
                self.curr_wave_time = 0

        # FixMe keeping track of time is not the levels responsibility
        if self.spawn:
            self.curr_wave_time += 1

    @staticmethod
    def from_file(file_name):
        """
        load a level from a json file
        :returns a new Level instance
        """
        with open(file_name) as fh:
            data = json.load(fh)

        waves = dict()
        for number, lines in data["waves"].items():
            waves[int(number)] = Level.parse_wave(lines)

        return Level(waves)

    @staticmethod
    def parse_wave(wave_data):
        """ :return a dict formated as key: spawn_time, value: list of bloons to spawn"""
        wave = dict()
        for line in wave_data:
            spawn_time = int(line["spawn_time"])
            bloon_type = line["type"]

            if spawn_time not in wave:
                wave[spawn_time] = []
            wave[spawn_time].append(bloon_type)
        return wave

    def is_wave_finished(self):
        """ return if any bloons are left to spawn based on current time point in wave"""
        return self.curr_wave_time > max(self.waves[self.curr_wave].keys())
