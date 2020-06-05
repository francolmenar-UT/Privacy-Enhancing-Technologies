# Global parameters
KEY_LEN = 2048  # In bits
# KEY_LEN = 32  # In bits
SEC_PARAM = 1010580409767

# Paillier Testing
TEST_RANGE = 1  # Amount of executions for test-pail
TEST_MSG = 9589489438
TICK = u'\u2713'

# SQP Testing
# TEST_NUM1 = 1500000000
# TEST_NUM1 = 1219776944015764000107391119181
TEST_NUM1 = 600

# TEST_NUM2 = 1219776944015764000107391119180
TEST_NUM2 = 500

# String auxiliary variables for debugging
SQP_TXT_AUX = "***************"
DEB_AUX_TXT = "++++++++++++++++"
DEB_AUX2_TXT = "----------------"


# Timing Variables
TIM_L = [10, 20, 50, 100]  # Lengths to be tested
TIM_AMOUNT = 4  # Total amount of numbers to be tested
TIM_PAIRS = TIM_AMOUNT / 2  # Amount of pairs to be tested, based on TIM_AMOUNT
EXE_REP = 1  # Just one execution per pair of values

# Folders
DATA_F = "data/"
TIM_10_F = "timing_length_10/"
TIM_20_F = "timing_length_20/"
TIM_50_F = "timing_length_50/"
TIM_100_F = "timing_length_100/"
CREATE_FOLDERS = [DATA_F, TIM_10_F, TIM_20_F, TIM_50_F, TIM_100_F]

# Files
TIM_10_CSV = "timing_length_10.csv"
TIM_20_CSV = "timing_length_20.csv"
TIM_50_CSV = "timing_length_50.csv"
TIM_100_CSV = "timing_length_100.csv"
