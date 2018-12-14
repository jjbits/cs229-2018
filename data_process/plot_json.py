import os
import numpy as np
import sys
import json
import matplotlib.pyplot as plt

dir_name = "./tub_jj3"
steering = []
throttle = []
for root, dirs, files in os.walk(dir_name):
    for filename in files:
        if ("json" in filename) and (filename != 'meta.json'):
            filename = dir_name + "/" + filename
            file = open(filename)
            data = json.load(file)
            #print(data)
            steering.append(data["user/angle"])
            throttle.append(data["user/throttle"])

#print(steering)
#print(throttle)
plt.plot(steering, '.')
plt.ylabel('steering')
plt.show()
plt.plot(throttle, '.')
plt.ylabel('throttle')
plt.show()

