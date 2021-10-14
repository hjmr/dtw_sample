import argparse

import numpy as np
import dtw
import h5py

def parse_arg():
    args = argparse.ArgumentParser(description="Apply DTW.")
    args.add_argument("-r", "--reference", type=str, nargs=1, help="Specify the reference HDF5 file.")
    args.add_argument("-I", "--input_path", type=str, nargs=1, help="A path to input data.")
    args.add_argument("-o", "--output", type=str, nargs=1, help="Specify the output file.")
    args.add_argument("-O", "--output_path", type=str, nargs=1, help="A path to output data.")
    args.add_argument("FILE", type=str, nargs=1, help="Specify a HDF5 file to convert.")
    return args.parse_args()

def get_data(hdf5_file, input_path):
    data = None
    with h5py.File(hdf5_file, "r") as h5:
        if input_path in h5.keys():
            data = np.array(h5[input_path]).T
    return data[0]

def put_data(hdf5_file, output_path, data):
    with h5py.File(hdf5_file, "a") as h5:
        h5[output_path] = data

def dtw_one(reference, target):
    alignment = dtw.dtw(target, reference)
    warp_idx = dtw.warp(alignment)
    return target[warp_idx]

if __name__ == "__main__":
    args = parse_arg()
    reference = get_data(args.reference[0], args.input_path[0])
    target = get_data(args.FILE[0], args.input_path[0])
    converted = dtw_one(reference, target)
    put_data(args.output[0], args.output_path[0], converted)
