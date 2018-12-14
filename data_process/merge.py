import os
import numpy as np
import sys
from shutil import copyfile


#directories = ["tub_nov_28_19_47_round3", "tub_nov_28_19_52_round4", "tub_nov_28_19_57_round5",
#               "tub_nov_28_19_57_round1_clockwise", "tub_nov_28_19_57_round2_clockwise", ]
directories = ["tub_expert", "tub_dagger_mod_iter1_solo"]

jpg_counter = 0
json_counter = 0
all_files_jpg = []
#all_files_json = []
jpg_json_dir = {}

out_dir = "./tub_dagger_mod_iter1_merged/"

# create directory name string
#prename = "./tub_nov_28/"
prename = "./"
f_list = []
for each in directories:
    f_list.append(prename+each)
#print(f_list)

for each_dir in f_list:
    for root, dirs, files in os.walk(each_dir):
        for filename in files:
            if "jpg" in filename:
                # extract the number part from the file name
                splited = filename.split("_")
                #print(splited)
                file_num = splited[0]
                # construct the corresponding json file name
                json_name = "record_" + file_num + ".json"
                if not json_name in files:
                    print("missing corresponding json file!!! " + filename + " " + json_name)
                    sys.exit()

                jpg_counter += 1
                json_counter += 1
                jpg_name = each_dir + "/" + filename
                json_name = each_dir + "/" + json_name
                all_files_jpg.append(jpg_name)
                jpg_json_dir[jpg_name] = json_name

print(len(all_files_jpg))
#print(jpg_json_dir)

np.random.shuffle(all_files_jpg)

if (1):
    for i in range(len(all_files_jpg)):
        out_name_jpg = out_dir + str(i) + "_cam-image_array_.jpg"
        out_name_json = out_dir + "record_" + str(i) + ".json"
        #print("processing: " + all_files_jpg[i] + " " + jpg_json_dir[all_files_jpg[i]])
        #print("output: " + out_name_jpg + " " + out_name_json)
        copyfile(all_files_jpg[i], out_name_jpg)
        copyfile(jpg_json_dir[all_files_jpg[i]], out_name_json)