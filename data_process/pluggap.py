from shutil import copyfile


dirname = 'dec7_20_47_round4_iter2_mod/'
srcfilename = './dec7_20_47_round4_iter2_mod/2207_cam-image_array_.jpg'
srcj = './dec7_20_47_round4_iter2_mod/record_2207.json'

for i in range(2208, 2288):
    dstfilename = dirname + str(i) + '_cam-image_array_.jpg'
    copyfile(srcfilename, dstfilename)

for i in range(2208, 2288):
    dstfilename = dirname + 'record_' + str(i) + '.json'
    copyfile(srcj, dstfilename)