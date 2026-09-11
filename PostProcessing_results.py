from utils import plot_utils
import os
import glob
import matplotlib.pyplot as plt
import numpy as np

# =============================================================================
# ADMX2001 Terminal Framework
# =============================================================================
# File:
#   PostProcessing_results.py
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

folder = r"./results/Teste2 - LoadComDodecan"

# =============================================================================
files = []
files.extend(glob.glob(os.path.join(folder, "*.npy")))

Data = []
for file in files:
    data = plot_utils.ReadNPY(file)
    data.plot(file)
    data.nyquist(file)
    Data.append(data)

# =============================================================================
#  Electrical Permittivity |  EPS =  Cp / C0

meas1 = np.array([d.meas1_mean for d in Data])

eps_line_alcool_W_auto = meas1[0] / meas1[1]
# eps_line_alcool_Wo_auto = meas1[1] / meas1[3]

eps_line_dodecane_W_auto = meas1[2] / meas1[1]
# eps_line_dodecane_Wo_auto = meas1[5] / meas1[3]

eps_line_hexadecane_W_auto = meas1[3] / meas1[1]
# eps_line_hexadecane_Wo_auto = meas1[7] / meas1[3]

freq = data.freq*1e3

#  Plot over frequency
fig, ax = plt.subplots(figsize=(9, 6))

ax.semilogy(freq, eps_line_alcool_W_auto, label="Alcohol - W auto", color = "b")
# ax.semilogy(freq, eps_line_alcool_Wo_auto, label="Alcohol - Wo auto", color = "b", linestyle="--")
ax.semilogy(freq, eps_line_dodecane_W_auto, label="Dodecane - W auto", color = "r")
# ax.semilogy(freq, eps_line_dodecane_Wo_auto, label="Dodecane - Wo auto", color = "r", linestyle="--")
ax.semilogy(freq, eps_line_hexadecane_W_auto, label="Hexadecane - W auto", color = "g")
# ax.semilogy(freq, eps_line_hexadecane_Wo_auto, label="Hexadecane - Wo auto", color = "g", linestyle="--")

ax.set_xscale("log")
ax.set_xlabel("Frequency [Hz]")
ax.set_ylabel(r"$\varepsilon_r$")
ax.grid(True, which="both", alpha=0.3)
ax.legend()

plt.tight_layout()
plt.show()

#  plot over sample
labels = [
    "Alcohol\nW auto",
    # "Alcohol\nWo auto",
    "Dodecane\nW auto",
    # "Dodecane\nWo auto",
    "Hexadecane\nW auto",
    # "Hexadecane\nWo auto"
]

eps_last = [
    eps_line_alcool_W_auto[-1],
    # eps_line_alcool_Wo_auto[-1],
    eps_line_dodecane_W_auto[-1],
    # eps_line_dodecane_Wo_auto[-1],
    eps_line_hexadecane_W_auto[-1],
    # eps_line_hexadecane_Wo_auto[-1]
]

fig, ax = plt.subplots(figsize=(9, 6))

ax.plot(labels, eps_last, "o", markersize=8)

# Add permittivity value above each point
for label, eps in zip(labels, eps_last):
    ax.annotate(
        f"{eps:.2f}",
        xy=(label, eps),
        xytext=(0, 8),
        textcoords="offset points",
        ha="center"
    )

ax.set_ylabel(r"$\varepsilon_r$")
ax.set_xlabel("Sample")
ax.set_title(f"Relative Permittivity at {freq[-1]:.2f} Hz")

ax.grid(True, axis="y", alpha=0.3)

plt.tight_layout()
plt.show()

