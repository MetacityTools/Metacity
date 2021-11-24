from metacity.geometry import Interval
from metacity.io.sim.parser import parse
from metacity.filesystem.base import write_json

interval_length = 3600

#create intervals for the timeline
intervals = []
for i in range(0, 90000, interval_length):
    intervals.append(Interval(i, interval_length))

#parse trips
#file = "tests/data/car_sec_3962.json"
file = "car_sec_11.json"
objects = parse(file)

#insert objects into intervals
for o in objects:
    for m in o.models:
        if m.type != "timepoint":
            continue
        for i in intervals:
            i.insert(m, 1)


intervals_s = [i.serialize() for i in intervals]



#write_json("test.json", intervals_s[10])

#i = Interval()
#i.deserialize(a)

