import os
import numpy as np
import sys
import json
import matplotlib.pyplot as plt
import re

def plot_json_range(start, stop, dir_name):
    steering = {}
    throttle = {}
    for root, dirs, files in os.walk(dir_name):
        for filename in files:
            if ("json" in filename) and (filename != 'meta.json'):
                filename = dir_name + "/" + filename
                file = open(filename)
                each_name = filename.split("/")
                rec = re.findall('\d+', each_name[2])
                recnum = int(rec[0])
                data = json.load(file)
                # print(data)
                steering[recnum] = data["user/angle"]
                throttle[recnum] = data["user/throttle"]

    plotlist = []
    for i in range(start, stop+1):
        plotlist.append(steering[i])

    #print(plotlist)
    #plt.plot(range(start, stop+1), plotlist, '.')
    #plt.ylabel('steering')
    #plt.show()
    return [range(start, stop+1), plotlist]

def plot_out_range(start, stop, filename):
    line_dict = {}
    file = open(filename)
    for line in file:
        line = line.replace("'", "")
        line = line.split('{')
        words = line[1].split(' ')
        if 'jpg' not in words[4]:
            print("sanity check on string for jpg name failed.")
            break
        rec = re.findall('\d+', words[4])
        recnum = int(rec[0])
        line_dict[recnum] = words

    plotlist = []
    for i in range(start, stop + 1):
        each_records = line_dict[i]
        steering_str = each_records[10].replace("}\n", "")
        plotlist.append(float(steering_str))

    # print(plotlist)
    #plt.plot(range(start, stop+1), plotlist, '.')
    #plt.ylabel('steering')
    #plt.show()
    return [range(start, stop+1), plotlist]

#golden = plot_json_range(405, 455, "./tub_golden")
golden = plot_json_range(1251, 1278, "./dec7_20_47_round4_iter2_mod")
# fault seg 1
#out = plot_out_range(691, 741, "./tub_dagger/out")
# fault seg 2
#out = plot_out_range(966, 1016, "./tub_dagger/out")
out = plot_out_range(2180, 2207, "./dec7_20_47_round4_iter2_mod/out")

_, (ax1, ax2) = plt.subplots(2, 1)
plt.xlabel("state s")
plt.ylabel("steering angle")
ax1.plot(golden[0], golden[1], '.')
#ax1.set_title("expert driver")
print(golden[1])
ax2.plot(out[0], out[1], '.')
#ax2.set_title("autopilot at iteration 1")
plt.show()