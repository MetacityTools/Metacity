from collections import defaultdict

class Statistics:
    def __init__(self):
        self.lods = defaultdict(lambda: 0)
        self.stats = defaultdict(lambda: 0)
        self.gtypes = defaultdict(lambda: 0)

    def __str__(self):
        return (f"{self.lods}"
                f"{self.stats}"
                f"{self.gtypes}")

    def parsed_geometry(self, lod, gtype):
        self.gtypes[gtype] += 1
        self.lods[lod] += 1
