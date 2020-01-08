#!/usr/bin/env python3
import pandas as pd
import matplotlib

import authpath

matplotlib.use("Agg")

def plot_dist_sphincs(fname):
    tests = 2**16
    numleaves = 32
    height = 16
    data = [authpath.sample_authset(numleaves, height,
                                    authpath.efficient_auth_set_indices) \
            for i in range(0, tests)]
    df = pd.DataFrame(data, columns=["Size"])
    df["Height"] = height
    df["# given leaves"] = numleaves

    plot = df['Size'].plot.hist(by="Size", bins = 350, legend=True)
    fig = plot.get_figure()
    fig.savefig(fname)

def plot_num_leaves(fname):
    tests = 2**10
    height = 16
    data = [(leaves, \
             authpath.sample_authset(leaves, height, \
                                     authpath.efficient_auth_set_indices)) \
            for i in range(0, tests) \
            for leaves in {1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048}]
    df = pd.DataFrame(data, columns=["# given leaves","Size"])
    df["ratio"] = df["Size"] / (df["# given leaves"] * height)

    plot = df.boxplot(column="ratio", by="# given leaves")
    fig = plot.get_figure()
    fig.savefig(fname)

if __name__ == '__main__':
    pass
