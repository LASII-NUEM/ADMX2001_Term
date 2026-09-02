import numpy as np
import matplotlib.pyplot as plt
from utils import plot_utils

filename = "ADMX_testC0_20260901_194906.npy"
data = np.load(f"results/{filename}", allow_pickle=True).item()

MeasType = ("freq", "spectrum")
if data["meastype"] == "freq":
    freq = data["freq"]
elif data["meastype"] == "spectrum":
    freq = data["freq_array"]
else:
    raise TypeError(f"[ADMX_meas] Unknown Calibration Type! Available Types:{type(MeasType)}")

count = data["count"]
result = data["freq_meas_result"]

if result.shape != (len(freq),count):
    raise ValueError(f"[ADMX_meas] Result array has incorrect shape. "
                     f"Expected {(count, len(freq))}, got {result.shape}.")


mode = data["mode"]

DISPLAY_MODES = {
    0:  ("Cs", "Rs"),
    1:  ("Cs", "D"),
    2:  ("Cs", "Q"),
    3:  ("Ls", "Rs"),
    4:  ("Ls", "D"),
    5:  ("Ls", "Q"),
    6:  ("R", "X"),
    7:  ("Z", "deg"),
    8:  ("Z", "rad"),
    9:  ("Cp", "Rp"),
    10: ("Cp", "D"),
    11: ("Cp", "Q"),
    12: ("Lp", "Rp"),
    13: ("Lp", "D"),
    14: ("Lp", "Q"),
    15: ("G", "B"),
    16: ("Y", "deg"),
    17: ("Y", "rad"),
    18: ("None", "None")}


if mode not in DISPLAY_MODES:
    raise ValueError(
        f"[ADMX_meas] Unknown display mode '{mode}'."
    )

meas1, meas2 = DISPLAY_MODES[mode]


