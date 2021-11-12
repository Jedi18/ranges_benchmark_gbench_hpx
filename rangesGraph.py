import json
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from os import listdir
import os

SEQ = 0
PAR = 1
RANGES = 2

def generateBenchmark():
    labelToCol = {
        'seq' : 'red',
        'par' : 'blue',
        'ranges' : 'green'
    }

    folder_path = 'C:\\Users\\targe\Documents\\ranges_csv\\ranges_benchmarks'
    folders = listdir(folder_path + '\\json_files')

    for scan_file in folders:
        fig, ax = plt.subplots()
        bm_data = {}
        bm_data[SEQ] = []
        bm_data[PAR] = []
        bm_data[RANGES] = []

        n = 0

        scan_file_path = folder_path + '\\json_files\\' + scan_file
        with open(scan_file_path) as jsonfile:
            data = json.load(jsonfile)

            for bm in data['benchmarks']:
                bm_data[bm['family_index']].append(bm)

        n = len(bm_data[SEQ])
        inputSizes = []
        seqTime = []
        parTime = []
        parRelative = []
        rangesRelative = []
        rangeTime = []

        for i in range(0, n):
            inputSizes.append(i + 5)
            seqTime.append(int(bm_data[SEQ][i]['real_time']))
            parTime.append(int(bm_data[PAR][i]['real_time']))
            rangeTime.append(int(bm_data[RANGES][i]['real_time']))
            parRelative.append(float(bm_data[SEQ][i]['real_time']) / float(bm_data[PAR][i]['real_time']))
            rangesRelative.append(float(bm_data[SEQ][i]['real_time']) / float(bm_data[RANGES][i]['real_time']))
        
        ax.set_xticks(range(5, 32, 1))

        ax.plot(inputSizes, parRelative, color=labelToCol['par'])
        ax.plot(inputSizes, rangesRelative, color=labelToCol['ranges'])
        ax.plot([5, 30], [1, 1], color=labelToCol['seq'])

        ax.set_xlabel('i where the input size is 2^i')
        ax.set_ylabel('Relative speedup to sequential')

        handles = []
        handles.append(mpatches.Patch(color=labelToCol['seq'], label="Seq"))
        handles.append(mpatches.Patch(color=labelToCol['par'], label="Par"))
        handles.append(mpatches.Patch(color=labelToCol['ranges'], label="Ranges"))
        handles.append(mpatches.Patch(color='white', label=""))
        handles.append(mpatches.Patch(color='white', label="L1 Cache - 32 KiB"))
        handles.append(mpatches.Patch(color='white', label="L2 Cache - 512 KiB"))
        handles.append(mpatches.Patch(color='white', label="L3 Cache - 16 MiB"))

        plt.legend(loc="upper left", handles=handles)
        plt.savefig(folder_path + '\\new_plots\\' + os.path.splitext(scan_file)[0] + '.png')

if __name__ == "__main__":
    generateBenchmark()