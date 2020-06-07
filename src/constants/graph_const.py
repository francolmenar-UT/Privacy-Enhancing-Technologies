########################### Values for reading the CSV files ###########################
# Rounding value for the execution time. If it is set to None no round is performed
ROUND_VAL = 2

# Names for the columns of the np array
COL_NM = ["Bit Length",
          "Execution time"]

########################### Constants for Graph Creation  ###########################
# Range of values for the axis
AXIS = [
    [0, 120, 10],
    [0, 33, 3]
]

# Names for the axis
AXIS_NM = [
    "Bit Length",
    "Execution time (s)"
]

# Colours for the different graphs
COLOUR = [
    "tab:blue",
    "tab:orange",
    "tab:green",
    "tab:cyan"
]

# Default colour for the grid for comparison graphs
GRID_COLOUR = '#cfe0e8'

IMG_FOLDER_PATH = "img/"

# Name for the images files
IMG = [
    "Bit_length_10",
    "Bit_length_20",
    "Bit_length_50",
    "Bit_length_100"
]

IMG_SIZE = 600

# Type of the output image file
IMG_TYPE = ".png"

# Names for the labels from the legend
LABEL = [
    "Bit Length 10",
    "Bit Length 20",
    "Bit Length 50",
    "Bit Length 100"
]

# Names for the different graphs
GRAPH_NM = [
    "Bit length 10",
    "Bit length 20",
    "Bit length 50",
    "Bit length 100"
]

# Names for the comparison graphs
GRAPH_COMP_NM = [
    "Bit_length_10",
    "Bit_length_20",
    "Bit_length_50",
    "Bit_length_100"
]

# Size of the points for the graph
PTN_SIZE = [3,  # For graph with points
              3]  # For discontinuous line graphs

# Size for the points for the legend
PTN_SIZE_LGN = 3

############# Modes for the legend of the graphs  #############
LGN_LR = "lower right"

############# Modes for the graphs  #############
PTN = "POINT"
PTN_F = "points/"

LN_DISC = "LN_DISC"
LN_DISC_F = "line_disc/"

LN_MEDIAN = "LN_MEDIAN"
LN_MEDIAN_F = "line_median/"

VLN = "VLN"
VLN_F = "violin/"

MODE_F = [PTN_F, LN_DISC_F, VLN_F, LN_MEDIAN_F]

############# Modes for the Grid Linestyle  #############
GRID_DISC = '--'

