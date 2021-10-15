import os
import os.path
import argparse
import glob

import numpy as np
import dtw
import h5py

DEFAULT_PATH = "98:D3:51:FD:97:15/raw/channel_1"


def parse_arg():
    args = argparse.ArgumentParser(description="Apply DTW.")
    args.add_argument("-r", "--reference", type=str, nargs=1, help="The reference file.")
    args.add_argument("-p", "--path", type=str, help="A data path in HDF5.")
    args.add_argument("-d", "--dst_dir", type=str, nargs=1, help="A destination directory.")
    args.add_argument("-s", "--src_dir", type=str, nargs=1, help="A directory contains source files.")
    return args.parse_args()


def get_data(hdf5_file, data_path):
    data = None
    with h5py.File(hdf5_file, "r") as h5:
        if data_path in h5.keys():
            data = np.array(h5[data_path]).T
    return data[0]


def dtw_one(reference, src_data):
    alignment = dtw.dtw(src_data, reference)
    warp_idx = dtw.warp(alignment)
    return src_data[warp_idx]


def get_destination(src_file, src_root, dst_root):
    file = os.path.basename(src_file)
    dirs = os.path.dirname(src_file).split("/")
    if dirs[0] == src_root:
        dirs[0] = dst_root
    return "/".join(dirs), file


def save_in_CSV(csv_file, data):
    np.savetxt(csv_file, data, delimiter=",", fmt="%d")


def dtw_dir(reference, src_root, dst_root, data_path):
    src_files = glob.glob("{}/**/*.h5".format(src_root), recursive=True)
    for src_file in src_files:
        print("{} > ".format(src_file), end="", flush=True)
        print("read > ", end="", flush=True)
        src_data = get_data(src_file, data_path)
        print("DTW > ", end="", flush=True)
        dtwed_data = dtw_one(reference, src_data)
        dst_dir, hdf5_filename = get_destination(src_file, src_root, dst_root)
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        filename_base, ext_hdf5 = os.path.splitext(hdf5_filename)
        dst_file = "{}/{}.csv".format(dst_dir, filename_base)
        print("saving to {} > ".format(dst_file), end="", flush=True)
        save_in_CSV(dst_file, dtwed_data)
        print("done.")


if __name__ == "__main__":
    args = parse_arg()
    data_path = args.path if args.path is not None else DEFAULT_PATH
    reference = get_data(args.reference[0], data_path)
    dtw_dir(reference, args.src_dir[0], args.dst_dir[0], data_path)
