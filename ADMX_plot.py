from utils import plot_utils

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

filename = "./results/ADMX_test_20260902_194357.npy"

data = plot_utils.ReadNPY(filename)

data.plot()