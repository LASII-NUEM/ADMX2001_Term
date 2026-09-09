from utils import plot_utils
import os
import glob
import matplotlib.pyplot as plt
import numpy as np


# =============================================================================
# ADMX2001 Terminal Framework
# =============================================================================
# File:
#   ADMX_plot.py
#
# Description:
#   Load and Plot ADMX2001 measurement result file (.npy)
#
# Author:
#   Everton Trento Jr.
#
# Institution:
#   NUEM - Multiphase Flow Research Center
#   UTFPR - Federal University of Technology - Paraná
#
# Hardware:
#   Analog Devices EVAL-ADMX2001
#
# Language:
#   Python
# =============================================================================

folder = r"./results/Testes-03.09"
files = []
files.extend(glob.glob(os.path.join(folder, "*.npy")))

Data = []
for file in files:
    data = plot_utils.ReadNPY(file)
    data.plot()
    Data.append(data)
