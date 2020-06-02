import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from src.constants.constants import *


def single_graph(data, col, axis, axis_name, prefix, points):
    plt_counter = 0
    for idx, arr in enumerate(data):  # Single graphs
        createPlots(col[0], col[1], data[idx], LABEL[idx], COLOUR[idx],
                    axis[0], axis[1], POINT_SIZE, NAME[idx], axis_name,
                    GRID_LINESTYLE, points)
        plt_counter += 1

        lgnd = plt.legend(loc="lower right", numpoints=1, fontsize=10)
        for i in range(0, plt_counter):
            lgnd.legendHandles[i]._legmarker.set_markersize(POINT_SIZE_LEGEND)

        plt.savefig(IMG_FOLDER_PATH + IMG[idx] + "_" + prefix + ".png", dpi=600)
        plt.close()
        plt_counter = 0


def multiple_graph(data, col, axis, axis_name, prefix, points):
    plt_counter = 0
    for idx, arr in enumerate(data):  # Multiple graphs
        name = ""
        name_plt = ""
        if idx == len(data) - 1:
            break
        else:
            name += IMG_FOLDER_PATH + IMG[idx]
            name_plt += NAME_AUX[idx]
            createPlots(col[0], col[1], data[idx], LABEL[idx], COLOUR[idx],
                        axis[0], axis[1], POINT_SIZE, NAME[idx], axis_name,
                        GRID_LINESTYLE, points, grid_colour=GRID_COLOUR)
            plt_counter += 1

        for i in range(idx + 1, len(data)):  # Each graph prints the comparison with the following ones
            createPlots(col[0], col[1], data[i], LABEL[i], COLOUR[i],
                        axis[0], axis[1], POINT_SIZE, NAME[i], axis_name,
                        GRID_LINESTYLE, points, grid_colour=GRID_COLOUR)
            plt_counter += 1

            name += " & " + IMG[i]
            name_plt += " & \n" + NAME_AUX[i]

        lgnd = plt.legend(loc="lower right", numpoints=1, fontsize=10)
        for i in range(0, plt_counter):
            lgnd.legendHandles[i]._legmarker.set_markersize(POINT_SIZE_LEGEND)

        plt.title(name_plt)
        plt.savefig(name + "_" + prefix + ".png", dpi=600)

        plt.close()
        plt_counter = 0


def create_graph():
    data_timing = readFiles([CPA_TIMING + CPA_PREFIX + ".csv",
                             ONLINE_CPA_TIMING + ONLINE_PREFIX + ".csv"], COL_TIMING)

    data_ge = readFiles([CPA_GE + CPA_PREFIX + ".csv",
                         ONLINE_CPA_GE + ONLINE_PREFIX + ".csv"], COL_GE)

    single_graph(data_timing, COL_TIMING, TIMING_AXIS, TIMING_AXIS_NM, TIMING_PREFIX, TM_POINTS)
    single_graph(data_ge, COL_GE, GE_AXIS, GE_AXIS_NM, GE_PREFIX, GE_POINTS)

    multiple_graph(data_timing, COL_TIMING, TIMING_AXIS, TIMING_AXIS_NM, TIMING_PREFIX, TM_POINTS)
    multiple_graph(data_ge, COL_GE, GE_AXIS, GE_AXIS_NM, GE_PREFIX, GE_POINTS)


def readFiles(files, col):
    data = []
    for file in files:
        data_tmp = pd.read_csv(file, sep=",", header=None, names=[col[0], col[1]])

        # round numbers and convert
        # data_tmp[c1] = round(data_tmp[c1].astype(float))

        # insert zero in both columns at index 1
        line = pd.DataFrame({col[0]: 0, col[1]: 0}, index=[0])
        data_tmp = pd.concat([data_tmp.iloc[:0], line, data_tmp.iloc[0:]]).reset_index(drop=True)
        data.append(data_tmp)
    return data


def createPlots(c1, c2, data, label, colour,
                x_axis, y_axis, point_size, name, axis,
                grid_linestyle, points, grid_colour=None):
    x = data[c1]
    y = data[c2]

    x_axis = np.arange(x_axis[0], x_axis[1], x_axis[2])
    y_axis = np.arange(y_axis[0], y_axis[1], y_axis[2])

    if points:
        plt.plot(x, y, 'o', label=label, markersize=np.sqrt(point_size[0]), color=colour)
        # plt.plot(x, y, kind='barh, label=label, markersize=np.sqrt(point_size), color=colour)

    else:
        plt.plot(x, y, label=label, marker='.', markersize=np.sqrt(point_size[1]), color=colour, linestyle=':')
        plt.fill_between(x, y, alpha=0.4, color=colour)

    plt.xlim([0, x_axis[1]])
    plt.ylim([0, y_axis[1]])

    plt.xticks(x_axis)
    plt.yticks(y_axis)

    plt.title(name)
    plt.xlabel(axis[0])
    plt.ylabel(axis[1])

    if grid_colour is None:
        plt.grid(True, color=colour, alpha=0.3, linestyle=grid_linestyle)
    else:
        plt.grid(True, color=grid_colour, linestyle=grid_linestyle)
