#!/usr/bin/env python3
"""
This is part of a seminar I'm taking about random numbers.

I deal with the randomness of the linear congruential generator and how the
choices of parameters influences the quality of the random numbers.

Plot the results.

"""
import sys
import argparse
import pickle
import numpy as np
from matplotlib import pyplot as plt

from util.logging.logger import CoreLog as cl
from util.opt.greet import ngreeting

def parse_arguments():
    """
    Parse the command line arguments.

    """
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("-l", "--log", help="set logging level",
                        choices=["quiet", "debug", "verbose", "info",
                                 "warning", "error", "critical"],
                        default="info")

    parser.add_argument("-i", "--input", help="perform tests on input file",
                        required=True)

    excl_group = parser.add_mutually_exclusive_group()
    excl_group.add_argument("-a", type=str, help="a in (a*x + c) mod m")
    excl_group.add_argument("-c", type=str, help="c in (a*x + c) mod m")
    excl_group.add_argument("-m", type=str, help="m in (a*x + c) mod m")

    parser.add_argument("-o", "--output", help="name of output files",
                        action="store_true")

    args = parser.parse_args()
    return args

def setup_loggers(logging_level):
    """
    Setup the logging level.

    """
    cl(logging_level)
    cl.verbose("starting logging")
    cl.verbose("logging level is set to {}".format(logging_level))
    if logging_level == "verbose" or logging_level == "debug":
        print()                 # newline

def greet():
    """
    Print a greeting.

    """
    print(ngreeting())

def parse_input(input_file):
    """
    Unpickle the input file.

    """
    # see what we have to expect from this input file
    try:
        res = input_file.split("results/results_")
        res.pop(0)
        res = res[0].split("_")
        res.remove("x0")
        res.remove("a")
        res.remove("c")
        res.remove("m")

    except ValueError:
        cl.error("Could not determine parameter ranges from input file name")
        sys.exit()

    x0, amin, amax, cmin, cmax, mmin, mmax = res

    x0 = int(x0)
    amin = int(amin)
    amax = int(amax)
    cmin = int(cmin)
    cmax = int(cmax)
    mmin = int(mmin)
    mmax = int(mmax.split(".")[0])

    expected = dict()
    expected["x0"] = x0
    expected["amin"] = amin
    expected["amax"] = amax
    expected["cmin"] = cmin
    expected["cmax"] = cmax
    expected["mmin"] = mmin
    expected["mmax"] = mmax

    cl.debug("Parsed parameter ranges from input file name")

    return_dict = dict()

    with open(input_file, "rb") as ifile:
        input_data = pickle.load(ifile)

    cl.debug("Loaded dictionary from file")

    for a in range(amin, amax+1):
        for c in range(cmin, cmax+1):
            for m in range(mmin, mmax+1):
                try:
                    assert(isinstance(input_data[x0][a][c][m], dict))
                except KeyError as e:
                    cl.error("Could not find parameter x0 {} a {} c {} m {} in "
                             "input file".format(x0, a, c, m))
                    cl.error("Input file appears to be corrupted or incomplete")
                    sys.exit()

    cl.debug("Input file appears to be in ship shape, proceeding")

    return_dict["ranges"] = expected
    return_dict["input_data"] = input_data
    return return_dict

def eval_pass(result_dict):
    """
    Evaluate the passing of a test run.

    """
    mono_pass = result_dict["monobit"]
    poker_pass = result_dict["poker"]
    runs_pass = result_dict["runs"]
    longruns_pass = result_dict["long_runs"]
    auto_pass = result_dict["autocorrelation"]

    sv2_pass = result_dict["spectral"]["v2"]["pass"]
    sv3_pass = result_dict["spectral"]["v3"]["pass"]
    sv4_pass = result_dict["spectral"]["v4"]["pass"]
    sv5_pass = result_dict["spectral"]["v5"]["pass"]

    stat_passes = mono_pass + poker_pass + runs_pass + longruns_pass + auto_pass
    spectral_passes = sv2_pass + sv3_pass + sv4_pass + sv5_pass

    return stat_passes, spectral_passes

def main():
    """
    Main entry point.

    """
    args = parse_arguments()
    greet()

    logging_level = args.log
    setup_loggers(logging_level)

    cl.info("Using {}".format(args.input))

    input_data = parse_input(args.input)

    x0 = input_data["ranges"]["x0"]
    amin = input_data["ranges"]["amin"]
    amax = input_data["ranges"]["amax"]
    cmin = input_data["ranges"]["cmin"]
    cmax = input_data["ranges"]["cmax"]
    mmin = input_data["ranges"]["mmin"]
    mmax = input_data["ranges"]["mmax"]

    if not args.a and not args.c and not args.m:
        cl.info(" a is in [{}, {}]".format(amin, amax))
        cl.info(" c is in [{}, {}]".format(cmin, cmax))
        cl.info(" m is in [{}, {}]".format(mmin, mmax))
        cl.info("Pick ONE value from the ranges to generate a plot")
        sys.exit()

    if args.a:
        a = int(args.a)
        if not a >= amin or not a <= amax:
            cl.error("'a' not in provided range")
            sys.exit()
        title = "x0 = {}, a fixed to {}, c and m change".format(x0, a)
        descr = "a_is_{}".format(a)
        x_key = "c"
        y_key = "m"
        x_range = np.arange(cmin, cmax+1)
        y_range = np.arange(mmin, mmax+1)
        xx_range = np.arange(cmin, cmax+2)
        yy_range = np.arange(mmin, mmax+2)

    if args.c:
        c = int(args.c)
        if not c >= cmin or not c <= cmax:
            cl.error("'c' not in provided range")
            sys.exit()
        title = "x0 = {}, c fixed to {}, a and m change".format(x0, c)
        descr = "c_is_{}".format(c)
        x_key = "a"
        y_key = "m"
        x_range = np.arange(amin, amax+1)
        y_range = np.arange(mmin, mmax+1)
        xx_range = np.arange(amin, amax+2)
        yy_range = np.arange(mmin, mmax+2)

    if args.m:
        m = int(args.m)
        if not m >= mmin or not m <= mmax:
            cl.error("'m' not in provided range")
            sys.exit()
        title = "x0 = {}, m fixed to {}, a and c change".format(x0, m)
        descr = "m_is_{}".format(m)
        x_key = "a"
        y_key = "c"
        x_range = np.arange(amin, amax+1)
        y_range = np.arange(cmin, cmax+1)
        xx_range = np.arange(amin, amax+2)
        yy_range = np.arange(cmin, cmax+2)

    xx, yy = np.meshgrid(x_range, y_range)
    xxx, yyy = np.meshgrid(xx_range, yy_range)  # for plotting
    stat_res = np.zeros_like(xx)
    spect_res = np.zeros_like(xx)
    spect_if_stat_res = np.zeros_like(xx)

    for i, x in enumerate(x_range):
        for j, y in enumerate(y_range):

            if args.a:
                stat_passes, spectral_passes = eval_pass(
                    input_data["input_data"][x0][a][x][y])

            if args.c:
                stat_passes, spectral_passes = eval_pass(
                    input_data["input_data"][x0][x][c][y])

            if args.m:
                stat_passes, spectral_passes = eval_pass(
                    input_data["input_data"][x0][x][y][m])

            stat_res[j, i] = stat_passes
            spect_res[j, i] = spectral_passes
            if (stat_passes == 5):
                spect_if_stat_res[j, i] = spectral_passes
            else:
                spect_if_stat_res[j, i] = -1


    # mask the spect_if_stat array
    spect_if_stat_res = np.ma.masked_where(spect_if_stat_res == -1, spect_if_stat_res)


    # statistical plot
    fig, ax = plt.subplots(1)
    stat_cmap = plt.get_cmap("viridis", 6)

    p = plt.pcolormesh(xxx, yyy, stat_res, edgecolor="k", cmap=stat_cmap, vmin=0, vmax=5)
    cbar = fig.colorbar(p)

    cbar.ax.get_yaxis().set_ticks([])
    for j, lab in enumerate(["$0$","$1$","$2$","$3$", "$4$", "$5$"]):
        cbar.ax.text(1.55, (2 * j + 1) / 12.0, lab, ha="left", va="center")
        cbar.ax.get_yaxis().labelpad = 15
    cbar.ax.set_ylabel("\nNumber of tests passed", rotation=90)

    # some voodoo for the exponential notation stuff
    ax.ticklabel_format(useOffset=False)
    plt.gca().get_yaxis().get_major_formatter().set_powerlimits((-1000, 1000))

    xticks = ax.get_xticks()
    xticks = np.asarray(xticks, dtype=int)
    ax.set_xticks(xticks[1:-1] + 0.5)
    ax.set_xticklabels(xticks[1:-1], rotation=90)

    yticks = ax.get_yticks()
    yticks = np.asarray(yticks, dtype=int)
    ax.set_yticks(yticks[1:-1] + 0.5)
    ax.set_yticklabels(yticks[1:-1])

    ax.set_xlabel("{}".format(x_key))
    ax.set_ylabel("{}".format(y_key))

    ax.set_title("Statistical Test results\n{}".format(title))
    plt.tight_layout()

    if args.output:
        out_name = "{}_statistical_{}.png".format(args.input.split(".")[0], descr)
        cl.info("Generating {}".format(out_name))
        plt.savefig(out_name)
    else:
        plt.show(0)


    # spectral plot
    fig, ax = plt.subplots(1)
    stat_cmap = plt.get_cmap("viridis", 5)

    p = plt.pcolormesh(xxx, yyy, spect_res, edgecolor="k", cmap=stat_cmap, vmin=0, vmax=4)
    cbar = fig.colorbar(p)

    cbar.ax.get_yaxis().set_ticks([])
    for j, lab in enumerate(["$0$","$1$","$2$","$3$", "$4$"]):
        cbar.ax.text(1.55, (2 * j + 1) / 10.0, lab, ha="left", va="center")
        cbar.ax.get_yaxis().labelpad = 15
    cbar.ax.set_ylabel("\nNumber of tests passed", rotation=90)

    # some voodoo for the exponential notation stuff
    ax.ticklabel_format(useOffset=False)
    plt.gca().get_yaxis().get_major_formatter().set_powerlimits((-1000, 1000))

    xticks = ax.get_xticks()
    xticks = np.asarray(xticks, dtype=int)
    ax.set_xticks(xticks[1:-1] + 0.5)
    ax.set_xticklabels(xticks[1:-1], rotation=90)

    yticks = ax.get_yticks()
    yticks = np.asarray(yticks, dtype=int)
    ax.set_yticks(yticks[1:-1] + 0.5)
    ax.set_yticklabels(yticks[1:-1])

    ax.set_xlabel("{}".format(x_key))
    ax.set_ylabel("{}".format(y_key))

    ax.set_title("Spectral Test results\n{}".format(title))
    plt.tight_layout()

    if args.output:
        out_name = "{}_spectral_{}.png".format(args.input.split(".")[0], descr)
        cl.info("Generating {}".format(out_name))
        plt.savefig(out_name)
    else:
        plt.show(0)


    # spectral if statistical plot
    fig, ax = plt.subplots(1)
    stat_cmap = plt.get_cmap("viridis", 5)

    p = plt.pcolormesh(xxx, yyy, spect_if_stat_res, edgecolor="k", cmap=stat_cmap, vmin=0, vmax=4)
    cbar = fig.colorbar(p)

    cbar.ax.get_yaxis().set_ticks([])
    for j, lab in enumerate(["$0$","$1$","$2$","$3$", "$4$"]):
        cbar.ax.text(1.55, (2 * j + 1) / 10.0, lab, ha="left", va="center")
        cbar.ax.get_yaxis().labelpad = 15
    cbar.ax.set_ylabel("\nNumber of tests passed", rotation=90)

    # some voodoo for the exponential notation stuff
    ax.ticklabel_format(useOffset=False)
    plt.gca().get_yaxis().get_major_formatter().set_powerlimits((-1000, 1000))

    xticks = ax.get_xticks()
    xticks = np.asarray(xticks, dtype=int)
    ax.set_xticks(xticks[1:-1] + 0.5)
    ax.set_xticklabels(xticks[1:-1], rotation=90)

    yticks = ax.get_yticks()
    yticks = np.asarray(yticks, dtype=int)
    ax.set_yticks(yticks[1:-1] + 0.5)
    ax.set_yticklabels(yticks[1:-1])

    ax.set_xlabel("{}".format(x_key))
    ax.set_ylabel("{}".format(y_key))

    ax.set_title("Spectral Test results (where Statistical Tests passed)\n{}".format(title))
    plt.tight_layout()

    if args.output:
        out_name = "{}_spectral_if_statistical_{}.png".format(args.input.split(".")[0], descr)
        cl.info("Generating {}".format(out_name))
        plt.savefig(out_name)
    else:
        plt.show()



if __name__ == "__main__":
    main()
