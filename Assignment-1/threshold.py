import csv
from dateutil import parser

filename = 'mixer1/exit.csv'

file = open(filename)

reader = csv.reader(file)

data = [line for line in reader]

# Array with only timings
times = [ parser.parse(a[0]) for a in data ]

time_str = [ str(time.hour) + str(time.minute) + str(time.second) for time in times ]


# This creates a dict with keys the number of messages sent in the same second
# and as value the number of times this threshold appears in the log
time_val = 0
t_val = 0
values = dict()
for val in time_str + [0]:
    if val == time_val:
        t_val += 1
    else:
        # Save previous value
        if t_val in values:
            values[t_val] += 1
        else:
            if t_val != 0:
                values[t_val] = 1

        # Reset counter
        t_val = 1
        time_val = val

# Print results
if len([k for k in values.keys()]) == 1:
    print("Threshold: {}".format([k for k in values.keys()][0]))
else:
    print("Multiple thresholds found!")
    for t in values:
        print("T: {}\t#: {}".format(t, values[t]))
