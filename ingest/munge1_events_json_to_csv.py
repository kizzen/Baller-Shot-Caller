##
# Script to convert single event file to CSV

import sys
import json
import csv

##
# Convert event file to string
##
def to_string(s):
    try:
        return str(s)
    except:
        #Encoding type changed if needed
        return s.encode('utf-8')

def reduce_item(key, value):
    global reduced_item

    #Condition for Reduction 1 events
    if type(value) is list:
        i=0
        for sub_item in value:
            reduce_item(key+'_'+to_string(i), sub_item)
            i=i+1


    #Condition for Reduction 2 events
    elif type(value) is dict:
        sub_keys = value.keys()
        for sub_key in sub_keys:
            reduce_item(key+'_'+to_string(sub_key), value[sub_key])

    #Base Condition for Events
    else:
        reduced_item[to_string(key)] = to_string(value)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("\nUsage: python json_to_csv.py <node_name> <json_in_file_path> <csv_out_file_path>\n")
    else:
        # arguments for event file
        node = sys.argv[1]
        json_file_path = sys.argv[2]
        csv_file_path = sys.argv[3]

        fp = open(json_file_path, 'r')
        json_value = fp.read()
        raw_data = json.loads(json_value)

        try:
            data_to_be_processed = raw_data[node]
        except:
            data_to_be_processed = raw_data

        processed_data = []
        header = []
        for item in data_to_be_processed:
            reduced_item = {}
            reduce_item(node, item)

            header += reduced_item.keys()

            processed_data.append(reduced_item)

        header = list(set(header))
        header.sort()

        with open(csv_file_path, 'w') as f:
            writer = csv.DictWriter(f, header, quoting=csv.QUOTE_ALL)
            writer.writeheader()
            for row in processed_data:
                writer.writerow(row)

        print("Completion of Csv writing file with %d columns" % len(header))
