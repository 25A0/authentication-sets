#!/usr/bin/env python3
import pandas as pd
import authset

def measure_dist_sphincs(path):
    tests = 2**16
    numleaves = 32
    height = 16
    data = [authset.sample_authset(numleaves, height,
                                    authset.efficient_auth_set_indices) \
            for i in range(0, tests)]
    df = pd.DataFrame(data, columns=["Size"])
    df["Height"] = height
    df["leaves"] = numleaves

    print(df.describe())

    # Export to csv
    df.to_csv(path)

def measure_num_leaves(path):
    tests = 2**10
    height = 16
    data = [(leaves, \
             authset.sample_authset(leaves, height, \
                                     authset.efficient_auth_set_indices)) \
            for i in range(0, tests) \
            for leaves in {1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048}]
    df = pd.DataFrame(data, columns=["# given leaves","Size"])
    df["ratio"] = df["Size"] / (df["# given leaves"] * height)

    # Export to csv
    df.to_csv(path)

if __name__ == '__main__':
    pass
