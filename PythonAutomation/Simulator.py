import os
import csv
import xml.etree.ElementTree as ET

TEMPLATE_FILE = "template.rou.xml"
ROUTE_OUTPUT = "density.rou.xml"
SUMO_OUTPUT_1 = "output/sumo_output_general.xml"
SUMO_OUTPUT_2 = "output/sumo_output_network.xml"
SUMO_OUTPUT_3 = "output/sumo_output_arteries.xml"
SUMO_OUTPUT_4 = "output/sumo_output_secondaries.xml"
CSV_OUTPUT_2 = "output/statistics_network_intelligent5.csv"
CSV_OUTPUT_3 = "output/statistics_arteries_intelligent5.csv"
CSV_OUTPUT_4 = "output/statistics_secondaries_intelligent5.csv"

DATA_FILE = "collect_data.xml"

NETWORK_FILES = ["networks/intelligent1.net.xml",
                 "networks/intelligent3.net.xml",
                 "networks/intelligent5.net.xml",
                 "networks/intelligent7.net.xml",
                 "networks/sync1.net.xml",
                 "networks/sync3.net.xml",
                 "networks/sync5.net.xml",
                 "networks/sync7.net.xml"]


# Generate traffic using a template and save the result into ROUTE_OUTPUT
def generate_traffic(upward: int, downward:int, left: int, right: int):
    with open(TEMPLATE_FILE, 'r') as file :
        filedata = file.read()

    filedata = filedata.replace('UPWARD', str(upward))
    filedata = filedata.replace('DOWNWARD', str(downward))
    filedata = filedata.replace('LEFT', str(left))
    filedata = filedata.replace('RIGHT', str(right))


    with open(ROUTE_OUTPUT, 'w') as file:
        file.write(filedata)
    
    
# Run a sumo simulation and store ouput
def run_sumo(network_file: str):
    command = f"sumo --net-file {network_file} --route-files {ROUTE_OUTPUT} --junction-taz 1 --additional-files {DATA_FILE} --statistic-output {SUMO_OUTPUT_1}"
    os.system(command)
    
    
# Run sumo_gui
def run_sumo_gui(network_file: str):
    command = f"sumo-gui --net-file {network_file} --route-files {ROUTE_OUTPUT} --junction-taz 1 --additional-files {DATA_FILE} --statistic-output {SUMO_OUTPUT_1}"
    os.system(command)
    
    
# Write header of the csv file
def write_header(network_files: list[str]):
    for network_file in network_files:
        f = open(network_file, 'a')
        writer = csv.writer(f)
        writer.writerow(["loaded", "inserted", "running", "waiting", "id", "sampledSeconds", "numEdges", "traveltime", "overlapTraveltime", "density", "laneDensity", "occupancy", "waitingTime", "timeLoss", "speed", "speedRelative", "departed", "arrived", "entered", "left", "laneChangedFrom", "laneChangedTo"])
        f.close()
    
        
# Read the output file and return a csv line
def output_to_str():
    result = ""
    
    tree = ET.parse(SUMO_OUTPUT_1)
    attributes1 = tree.getroot()[0][0].attrib
    
    tree = ET.parse(SUMO_OUTPUT_2)
    attributes2 = tree.getroot()[0].attrib
        
    return list(attributes1.values()) + list(attributes2.values())


# Write the outputs of sumo to a CSV file
def output_to_file():
    result = ""
    tree = ET.parse(SUMO_OUTPUT_1)
    attributes_general = list(tree.getroot()[0].attrib.values())
    
    tree = ET.parse(SUMO_OUTPUT_2)
    attributes = list(tree.getroot()[0][0].attrib.values())
    f = open(CSV_OUTPUT_2, 'a')
    writer = csv.writer(f)
    writer.writerow(attributes_general + attributes)
    f.close()
    
    tree = ET.parse(SUMO_OUTPUT_3)
    attributes = list(tree.getroot()[0][0].attrib.values())
    f = open(CSV_OUTPUT_3, 'a')
    writer = csv.writer(f)
    writer.writerow(attributes_general + attributes)
    f.close()
        
    tree = ET.parse(SUMO_OUTPUT_4)
    attributes = list(tree.getroot()[0][0].attrib.values())
    f = open(CSV_OUTPUT_4, 'a')
    writer = csv.writer(f)
    writer.writerow(attributes_general + attributes)
    f.close()
    

    
os.chdir("PythonAutomation")

start = 800
step = 700
end = 5001

for network_file in NETWORK_FILES:
    for veh_density in range(start, end, step):
        generate_traffic(veh_density, veh_density//4, veh_density//3, veh_density//3)
        run_sumo(network_file)
        output_to_file() 
        
write_header([CSV_OUTPUT_2, CSV_OUTPUT_3, CSV_OUTPUT_4])
        