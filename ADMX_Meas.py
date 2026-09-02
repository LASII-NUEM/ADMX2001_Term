# =============================================================================
# ADMX2001 Terminal Framework
# =============================================================================
# File:
#   admx_meas.py
#
# Description:
#   Implements the measurement procedure for the Analog Devices
#   EVAL-ADMX2001. This module configures the measurement parameters,
#   performs the requested measurements, and acquires the resulting data.
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

import serial
from utils import meas_utils

# =============================================================================
# USER CONFIGURATION
# =============================================================================

ADMXport = "COM6"

MEASUREMENT_CONFIG = {
    # -------------------------------------------------------------------------
    # Measurement Type
    # Defines the measurement procedure:
    #   "freq"     -> Single-frequency calibration
    #   "spectrum" -> Frequency-spectrum calibration
    "meas_type": "spectrum",

    # Measurement Mode
    # Defines the measurement mode
    # DISPLAY_MODES = {
    #     0:  ("Cs", "Rs"),
    #     1:  ("Cs", "D"),
    #     2:  ("Cs", "Q"),
    #     3:  ("Ls", "Rs"),
    #     4:  ("Ls", "D"),
    #     5:  ("Ls", "Q"),
    #     6:  ("R", "X"),
    #     7:  ("Z", "deg"),
    #     8:  ("Z", "rad"),
    #     9:  ("Cp", "Rp"),
    #     10: ("Cp", "D"),
    #     11: ("Cp", "Q"),
    #     12: ("Lp", "Rp"),
    #     13: ("Lp", "D"),
    #     14: ("Lp", "Q"),
    #     15: ("G", "B"),
    #     16: ("Y", "deg"),
    #     17: ("Y", "rad"),
    #     18: ("None", "None")}
    "mode":9,

    # -------------------------------------------------------------------------
    # Frequency measurement
    #
    # These parameters are used when meas_type = "freq".
    "freq" : 1e6,

    # Frequency Spectrum
    # init_freq  : Initial frequency [Hz]
    # final_freq : Final frequency [Hz]
    # scale      : Frequency spacing ("LOG" or "LINEAR")
    # points     : Number of frequency points
    #
    # These parameters are used when meas_type = "spectrum".
    "init_freq": 1e3,
    "final_freq": 1e6,
    "scale": "LOG",
    "points": 136,

    # -------------------------------------------------------------------------
    # ADMX2001 Measurement Settings
    # gain_ch0 : Voltage channel gain
    # gain_ch1 : Current channel gain
    # mag      : Excitation signal magnitude [V]
    # count    : Number of measurements used for averaging
    "gain_ch0": 0,
    "gain_ch1": 0,
    "Autogain": False,
    "mag": 1.0,
    "count": 5,
    "avg": 10,

    # Calibration Standards
    # Select which calibration standards was performed.
    # Set True to enable or False to skip the calibration step.
    "cal_open": True,
    "cal_short": True,
    "cal_load": True,

    # Measurement filename
    "filename": "test",
}

try:

    ser = serial.Serial(
        port=ADMXport,
        baudrate=115200,
        timeout=1,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS
    )

    if ser.is_open:
        measurement = meas_utils.freq_meas(serialCom=ser, **MEASUREMENT_CONFIG)

except serial.SerialException as error:
    print(f"Serial error: {error}")

except Exception as error:
    print(f"Error: {error}")

finally:
    if ser is not None and ser.is_open:
        ser.close()
        print("Serial port closed.")
