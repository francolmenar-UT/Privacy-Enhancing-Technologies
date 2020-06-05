import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

from src.constants.graph_const import *
from src.constants.const import *


def readFiles(files, col, round_val=None):
    """
    Read a list of csv files and returns its data
    :param round_val: It sets the decimal values to round the execution time value
    :param files: List of file names
    :param col: Column names
    :return: A list with the data of each of the files
    """
    data = []  # Data list to return

    # Read the data from each of the files
    for file in files:
        data_tmp = pd.read_csv(file, sep=",", header=None, names=[col[0], col[1]])

        # Check if it has to round execution time
        if round_val is not None:
            data_tmp[col[1]] = data_tmp[col[1]].round(decimals=2)

        # insert zero in both columns at index 1
        # line = pd.DataFrame({col[0]: 0, col[1]: 0}, index=[0])
        # data_tmp = pd.concat([data_tmp.iloc[:0], line, data_tmp.iloc[0:]]).reset_index(drop=True)

        data.append(data_tmp)  # Add the new data from the csv file to the list
    return data


def create_folder(folder):
    """
    Checks if a folder exists, if it does not it creates it
    :param folder: Folder to be created
    :return:
    """
    # Check if the folder does not exists
    if not os.path.isdir(folder):
        os.makedirs(folder)  # Create folder


def single_graph(data, col, axis, axis_name,
                 g_name, g_mode, grid_mode, colour,
                 lgn_mode, lgn_pt_size, pt_size, labels,
                 img_folder, img, img_type, img_size):
    # Go through all the list of data in data - which are the number of graphs to plot
    for idx, arr in enumerate(data):
        # Plot counter
        plt_counter = 0

        # Create the graph
        createPlots(col[0], col[1], data[idx], labels[idx], colour[idx],
                    axis[0], axis[1], pt_size, g_name[idx], axis_name,
                    grid_mode, g_mode)

        # Update plot counter
        plt_counter += 1

        # Add the legend to the graph
        # lgnd = plt.legend(loc=lgn_mode, numpoints=1, fontsize=10)

        # Set the size of the points in the legend
        # lgnd.legendHandles[0]._legmarker.set_markersize(lgn_pt_size)

        # Save graph as an image
        plt.savefig(img_folder + img[idx] + img_type, dpi=img_size)
        plt.close()


def multiple_graph(data, col, axis, axis_name,
                   g_name, g_comp_name, g_mode, grid_mode, grid_colour, colour,
                   lgn_mode, lgn_pt_size, pt_size, labels,
                   img_folder, img, img_type, img_size):
    # Go through all the list of data in data - which are the number of graphs to plot
    for idx, arr in enumerate(data):
        # Set to initial values
        name, name_plt, plt_counter = "", "", 0

        # Do not print the last graph - it assumes that the single graphs have been plot already
        if idx == len(data) - 1:
            break

        # Update the name for the graph
        name += img_folder + img[idx]
        name_plt += g_comp_name[idx]

        # Create first plot
        createPlots(col[0], col[1], data[idx], labels[idx], colour[idx],
                    axis[0], axis[1], pt_size, g_name[idx], axis_name,
                    grid_mode, g_mode, grid_colour=grid_colour)

        # Update plot counter
        plt_counter += 1

        # Each graph prints the comparison with the following graphs
        for i in range(idx + 1, len(data)):
            # Add subsequent graph points to the comparison graph
            createPlots(col[0], col[1], data[i], labels[i], colour[i],
                        axis[0], axis[1], pt_size, g_name[i], axis_name,
                        grid_mode, g_mode, grid_colour=grid_colour)
            plt_counter += 1

            # Update the name for the graph
            name += " & " + img[i]
            name_plt += " & \n" + g_comp_name[i]

        # Add the legend to the graph
        # lgnd = plt.legend(loc=lgn_mode, numpoints=1, fontsize=10)

        # Set the size of the points in the legend
        # for i in range(0, plt_counter):
        #    lgnd.legendHandles[i]._legmarker.set_markersize(lgn_pt_size)

        # Set the name for the comparison graph
        plt.title(name_plt)

        # Save graph as an image
        plt.savefig(name + img_type, dpi=img_size)
        plt.close()


def two_graphs(data, col, axis, axis_name,
               g_name, g_comp_name, g_mode, grid_mode, grid_colour, colour,
               lgn_mode, lgn_pt_size, pt_size, labels,
               img_folder, img, img_type, img_size):
    # Go through all the list of data in data - which are the number of graphs to plot
    for idx, arr in enumerate(data):
        # The two last ones are already plotted
        if idx == len(data) - 2:
            break

        # Each graph prints the comparison with one of the following ones
        for i in range(idx + 1, len(data)):
            # Plot counter
            plt_counter = 0

            # Update the name for the graph
            name = img_folder + img[idx]
            name_plt = g_comp_name[idx]

            # Base graph
            createPlots(col[0], col[1], data[idx], labels[idx], colour[idx],
                        axis[0], axis[1], pt_size, g_name[idx], axis_name,
                        grid_mode, g_mode, grid_colour=grid_colour)

            # Update plot counter
            plt_counter += 1

            # Update the name for the graph
            name += " & " + img[i]
            name_plt += " & \n" + g_comp_name[i]

            # Comparison graph
            createPlots(col[0], col[1], data[i], labels[i], colour[i],
                        axis[0], axis[1], pt_size, g_name[i], axis_name,
                        grid_mode, g_mode, grid_colour=grid_colour)

            # Update plot counter
            plt_counter += 1

            # Add the legend to the graph
            # lgnd = plt.legend(loc=lgn_mode, numpoints=1, fontsize=10)

            # Set the size of the points in the legend
            # for i in range(0, plt_counter):
            #     lgnd.legendHandles[i]._legmarker.set_markersize(lgn_pt_size)

            # Set the name for the comparison graph
            plt.title(name_plt)

            # Save graph as an image
            plt.savefig(name + img_type, dpi=img_size)
            plt.close()


def create_graph():
    """
    It creates the graphs for the CSV files created.
    Uses the data from graph_const and const
    """
    # Reads the data from the csv files
    data = readFiles([DATA_F + TIM_10_F + TIM_10_CSV,
                      DATA_F + TIM_20_F + TIM_20_CSV,
                      DATA_F + TIM_50_F + TIM_50_CSV,
                      DATA_F + TIM_100_F + TIM_100_CSV,
                      ], COL_NM, round_val=ROUND_VAL)

    # Check if there is no folder for the images
    create_folder(IMG_FOLDER_PATH)

    # Creates single graphs
    single_graph(data, COL_NM, AXIS, AXIS_NM,
                 GRAPH_NM, VLN, GRID_DISC, COLOUR,
                 LGN_LR, PTN_SIZE_LGN, PTN_SIZE, LABEL,
                 IMG_FOLDER_PATH, IMG, IMG_TYPE, IMG_SIZE)

    # Creates comparison graphs
    multiple_graph(data, COL_NM, AXIS, AXIS_NM,
                   GRAPH_NM, GRAPH_COMP_NM, VLN, GRID_DISC, GRID_COLOUR, COLOUR,
                   LGN_LR, PTN_SIZE_LGN, PTN_SIZE, LABEL,
                   IMG_FOLDER_PATH, IMG, IMG_TYPE, IMG_SIZE)

    # Creates comparison of two graphs
    two_graphs(data, COL_NM, AXIS, AXIS_NM,
               GRAPH_NM, GRAPH_COMP_NM, VLN, GRID_DISC, GRID_COLOUR, COLOUR,
               LGN_LR, PTN_SIZE_LGN, PTN_SIZE, LABEL,
               IMG_FOLDER_PATH, IMG, IMG_TYPE, IMG_SIZE)


def createPlots(c1, c2, data, label, colour,
                x_axis, y_axis, point_size, name, axis,
                grid_linestyle, mode, grid_colour=None):
    # Load the data
    x = data[c1]
    y = data[c2]

    # Arrange the data
    x_axis = np.arange(x_axis[0], x_axis[1], x_axis[2])
    y_axis = np.arange(y_axis[0], y_axis[1], y_axis[2])

    # Graph with points
    if mode is PTN:
        plt.plot(x, y, 'o', label=label, markersize=np.sqrt(point_size[0]), color=colour)

    # Line graph with discontinuous lines
    elif mode is LN_DISC:
        plt.plot(x, y, label=label, marker='.', markersize=np.sqrt(point_size[1]), color=colour, linestyle=':')
        plt.fill_between(x, y, alpha=0.4, color=colour)

    elif mode is VLN:
        violin_parts = plt.violinplot(y, [x[1]], points=100, widths=4, showmeans=True,
                                      showextrema=True, showmedians=True, bw_method=0.5)

        for part in ('cbars', 'cmins', 'cmaxes', 'cmeans', 'cmedians'):
            vp = violin_parts[part]
            vp.set_color(colour)
            vp.set_linewidth(1)

        for part in violin_parts['bodies']:
            part.set_color(colour)
            part.set_alpha(0.3)
            # part.set_edgecolor('black')

        # Incorrect plot mode
    else:
        print("ERROR: Wrong plot mode")
        return -1

    # Set the ranges for the
    plt.xlim([x_axis[0], x_axis[len(x_axis) - 1]])
    plt.ylim([y_axis[0], y_axis[len(y_axis) - 1]])

    plt.xticks(x_axis)
    plt.yticks(y_axis)

    # Set the name to the graph and the names for the axis
    plt.title(name)
    plt.xlabel(axis[0])
    plt.ylabel(axis[1])

    # Set the colour to the grid
    if grid_colour is None:
        plt.grid(True, color=colour, alpha=0.3, linestyle=grid_linestyle)
    else:
        plt.grid(True, color=grid_colour, linestyle=grid_linestyle)
