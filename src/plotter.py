import os
import math
import logging
import argparse
from itertools import groupby
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as mpl

def transpose(l):
    return list(map(list, zip(*l)))

def process_data(data_path):
    # Open and parse data
    try:
        with open(data_path, "r") as f:
            str_data = (line.split(";") for line in f.read().splitlines())
            data = [[sample[0]] + [list(map(float, sample[1:]))]
                    for sample in str_data]
    except Exception as e:
        logging.error(e)
        exit(-1)

    # Calculate and add means
    gdata = [(k, [e[1] for e in gr]) for k, gr in groupby(data, lambda x: x[0])]
    gdata_t = [list(zip(*gr)) for k, gr in gdata]
    gmeans = [[sum(s)/len(s) for s in gr] for gr in gdata_t]

    gstd = []
    for (means, tsamples) in zip(gmeans, gdata_t):
        stds = []
        for (mean, tsample) in zip(means, tsamples):
            stds.append(math.sqrt(
                sum(map(lambda x: (mean - x)**2, tsample))/len(tsample)))
        gstd.append(stds)

    # Construct processed data
    keys = [k for k, gr in gdata]
    return [keys, transpose(gmeans), transpose(gstd)]

COLORS = ['r', 'g', 'b', 'c']
def plot_data(pdata, i, ind, bar_width):
    ind = [x for x in range(len(pdata[0]))]
    x_ind = [x + i*(bar_width) + bar_width/2 for x in ind]
    bar_x_ind = list(map(lambda x: x + i*(bar_width), ind))

    mpl.errorbar(x_ind, pdata[1][i], color=COLORS[i], linewidth=2.0)
    mpl.bar(bar_x_ind, pdata[1][i], yerr=pdata[2][i],
            width=bar_width, color=COLORS[i], ecolor='k')

def plot(pdata):
    bar_width = 1.0/5.0
    fig = mpl.figure(0)
    splot = fig.add_subplot(1, 1, 1)
    ind = [x for x in range(len(pdata[0]))]

    plot_data(pdata, 0, ind, bar_width)
    plot_data(pdata, 1, ind, bar_width)
    plot_data(pdata, 2, ind, bar_width)
    plot_data(pdata, 3, ind, bar_width)

    splot.set_xticks([x + 2*bar_width for x in ind])
    splot.set_xticklabels(pdata[0])

    return fig

def main():
    argpar = argparse.ArgumentParser(description='Plotter')
    argpar.add_argument("-d", "--data-path",
                        required=True,
                        help="File with data to plot")
    argpar.add_argument("-s", "--show",
                        action="store_true",
                        help="Show plot instead of save it")
    args = argpar.parse_args()

    fig = plot(process_data(args.data_path))
    mpl.savefig(os.path.splitext(args.data_path)[0] + ".png")
    if args.show:
        mpl.show()

if __name__ == "__main__":
    main()
