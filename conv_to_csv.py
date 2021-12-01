import os
import os.path
import argparse
import glob

import numpy as np
import h5py

DEFAULT_PATH = "98:D3:51:FD:97:15/raw/channel_1"


def parse_arg():
    args = argparse.ArgumentParser(description="Convert to CSV.")
    args.add_argument("-d", "--device", type=str, default="98:D3:51:FD:97:15", help="Device ID like 98:D3:51:XX:XX:XX")
    args.add_argument("-c", "--channels", type=int, nargs="+", help="Channes.")
    args.add_argument("-f", "--from_dir", type=str, nargs=1, help="A destination directory.")
    args.add_argument("-t", "--to_dir", type=str, nargs=1, help="A directory contains source files.")
    return args.parse_args()


def get_data(hdf5_file, device, channels):
    data = None
    with h5py.File(hdf5_file, "r") as h5:
        for c in channels:
            data_path = "{}/raw/channel_{}".format(device, c)
            if data_path in h5.keys():
                if data == None:
                    data = np.array(h5[data_path]).T
                else:
                    data = np.append(data, np.array(h5[data_path]).T, axis=0)
    return data


def get_destination(src_file, src_root, dst_root):
    hdf5_filename = os.path.basename(src_file)
    filename_base, _ = os.path.splitext(hdf5_filename)
    dst_filename = "{}.csv".format(filename_base)

    dirs = os.path.dirname(src_file).split("/")
    if dirs[0] == src_root:
        dirs[0] = dst_root
    dst_dir = "/".join(dirs)

    return dst_dir, dst_filename


def save_in_CSV(csv_file, data):
    np.savetxt(csv_file, data, delimiter=",", fmt="%d")


def to_csv_dir(src_root, dst_root, device, channels):
    src_files = glob.glob("{}/**/*.h5".format(src_root), recursive=True)
    for src_file in src_files:
        src_data = get_data(src_file, device, channels)
        dst_dir, dst_filename = get_destination(src_file, src_root, dst_root)
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        dst_file = "{}/{}".format(dst_dir, dst_filename)
        save_in_CSV(dst_file, src_data)


if __name__ == "__main__":
    args = parse_arg()
    to_csv_dir(args.from_dir[0], args.to_dir[0], args.device, args.channels)
