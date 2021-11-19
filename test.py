import json
from metacity.io.sim import parser
#from metacity.io.shapefile import parser

def main():
    input_file = "car_sec_0.json"
    #input_file2 = '/home/metakocour/Projects/Metacity/metacity/io/sim/OBYVATELSTVO/'

    asd = parser.parse(input_file)
    print(asd)

if __name__ == "__main__":
    main()