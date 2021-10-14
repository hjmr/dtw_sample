import argparse

import numpy as np
import dtw
import h5py

def parse_arg():
    args = argparse.ArgumentParser(description="Apply DTW.")
    args.add_argument("-p", "--data_path", type=str, nargs=1, help="A path to data in HDF5.")
    args.add_argument("-r", "--reference", type=str, nargs=1, help="Specify the reference HDF5 file.")
    args.add_argument("-o", "--output", type=str, nargs=1, help="Specify the output file.")
    args.add_argument("-k", "--key", type=str, nargs=1, help="Specify the key to store converted data.")
    args.add_argument("FILE", type=str, nargs=1, help="Specify a HDF5 file to convert.")
    return args.parse_args()

def get_data(hdf5_file, data_path):
    data = None
    with h5py.File(hdf5_file, "r") as h5:
        if data_path in h5.keys():
            data = np.array(h5[data_path]).T
    return data[0]

def dtw_one(reference, target):
    alignment = dtw.dtw(target, reference)
    warp_idx = dtw.warp(alignment)
    return target[warp_idx]

if __name__ == "__main__":
    args = parse_arg()
    reference = get_data(args.reference[0], args.data_path[0])
    for f in args.FILES:
        target = get_data(f, args.data_path[0])
        converted = dtw_one(reference, target)
