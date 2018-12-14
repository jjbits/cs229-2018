import os
import numpy as np
import sys
import json
import matplotlib.pyplot as plt
import re

gf = './golden.json'
#filename = './tub_dagger/out'
#outdir = "./tub_dagger_mod/"
filename = './dec7_20_47_round4_iter2_mod/out'
outdir = "./dec7_20_47_round4_iter2_mod/"

mod_range1 = (239, 269)
mod_range2 = (2180, 2207)

"""
golden_val1 = [-0.04017857142857142, -0.06529017857142834, -0.07910156249999976, -0.07910156249999976, -0.07910156250000017,
 -0.07910156250000017, -0.08161272321428552, -0.08161272321428552, -0.08537946428571418, -0.08537946428571418,
 -0.08537946428571418, -0.08537946428571418, -0.08914620535714264, -0.08914620535714264, -0.08914620535714264,
 -0.09291294642857148, -0.10672433035714261, -0.10672433035714261, -0.12179129464285707, -0.12179129464285707,
 -0.12179129464285707, -0.10923549107142844, -0.05775669642857138, -0.04394531249999984, -0.003766741071428454,
 0.023856026785714513, 0.025111607142857064, 0.01757812500000011, 0.01757812500000011, 0.0037667410714287467,
 0.0037667410714287467, 7.31704252099376e-17, 7.31704252099376e-17, -0.010044642857142806, -0.010044642857142806,
 -0.017578125000000226, -0.017578125000000226, -0.02887834821428562, -0.02887834821428562, -0.038922991071428395,
 -0.038922991071428395, -0.038922991071428395, -0.038922991071428395, -0.038922991071428395, -0.038922991071428395,
 -0.038922991071428395, -0.038922991071428395, -0.056501116071428485, -0.056501116071428485, -0.060267857142857116,
 -0.060267857142857116]
"""
golden_val1 = [0.067699105, 0.13905056, 0.09128057, 0.099139825, 0.11505239,
               0.1651496, 0.1320589, 0.05126555, 0.18993466, 0.0697154,
               -0.0056912443, 0.0340681, -0.019599264, 0.0024536157, 0.11130235,
               -0.011408249, -0.13619322, -0.114079624, 0.054968264, -0.122569606,
               -0.12673785, -0.10911863, -0.11169141, -0.06420347, -0.1602879,
               -0.19697191, -0.063816056, -0.08454348, 0.0019369442, -0.15774131, -0.22118165]

golden_val2 = [0.065678835, 0.03514547, -0.052421883, -0.037723515, -0.036916144,
               0.010718604, -0.02629421, -0.03542917, -0.08699868, 0.024914889,
               0.014243519, -0.013077644, -0.09490778, -0.0009016799, -0.026683535,
               -0.017945115, -0.12054201, -0.13148525, 0.10553716, 0.056261927,
               -0.06753405, -0.06073659, -0.046916947, -0.06633068, -0.12108719,
               -0.2733592, -0.2578945, -0.1455788]



mods = [(mod_range1, golden_val1, {}), (mod_range2, golden_val2, {})]

def make_json_records():
    # prepare the golden values
    for each in mods:
        golden_dict = each[2]
        mod_start = each[0][0]
        mod_stop = each[0][1]
        golden_val = each[1]
        for i in range(0, (mod_stop-mod_start)+1):
            golden_dict[mod_start+i] = golden_val[i]

    gfile = open(gf)
    gd = json.load(gfile)

    file = open(filename, 'r')
    for line in file:
        line = line.replace("'", "")
        line = line.split('{')
        words = line[1].split(' ')

        # get the file number
        filenum = words[4].split('_')
        output_name = outdir+"record_"+filenum[0]+".json"
        of = open(output_name, 'w+')

        # get the jpg name
        words[4] = words[4].replace(",", "")
        gd["cam/image_array"] = words[4]
        gd["timestamp"] = words[1]
        gd["user/throttle"] = float(words[6].replace(",", ""))
        gd["user/mode"] = "user"
        words[10] = words[10].replace("}\n", "")
        gd["user/angle"] = float(words[10])

        if swap_golden:
            # if the rec num is in the mod range, modify
            rec = re.findall('\d+', words[4])
            recnum = int(rec[0])
            for each in mods:
                golden_dict = each[2]
                mod_start = each[0][0]
                mod_stop = each[0][1]
                if recnum in range(mod_start, mod_stop+1):
                    gd["user/angle"] = golden_dict[recnum]

        json.dump(gd, of)

swap_golden = 1
make_json_records()