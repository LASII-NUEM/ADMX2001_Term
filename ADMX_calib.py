# =============================================================================
# ADMX2001 Terminal Framework
# =============================================================================
# File:
#   admx_calib.py
#
# Description:
#   Implements the full-spectrum calibration procedure for the Analog Devices
#   EVAL-ADMX2001. This module uses the calibration utilities provided by the
#   calibrate_utils.py class to perform and manage the calibration process.
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
from utils import calibrate_utils

# =============================================================================
# USER CONFIGURATION
# =============================================================================

ADMXport = "COM5"

CALIBRATION_CONFIG = {
    # -------------------------------------------------------------------------
    # Calibration Standards
    # Select which calibration standards will be performed.
    # Set True to enable or False to skip the calibration step.

    "cal_open": True,
    "cal_short": True,
    "cal_load": True,

    # -------------------------------------------------------------------------
    # Load Standard
    # To obtain the resistive and reactive components beforehand, use an
    # LCR meter and select Rs (series resistance) and X (reactance) as the
    # display parameters.
    # rt : Resistive component [Ohm]
    # xt : Reactive component [Ohm]
    #
    # These parameters are only required when cal_load = True.
    "rt": 1e3,
    "xt": 1.3e-3,

    # -------------------------------------------------------------------------
    # Calibration Type
    # Defines the calibration procedure:
    #   "freq"     -> Single-frequency calibration
    #   "spectrum" -> Frequency-spectrum calibration
    "calib_type": "spectrum",

    # -------------------------------------------------------------------------
    # Frequency Spectrum
    # init_freq  : Initial frequency [Hz]
    # final_freq : Final frequency [Hz]
    # scale      : Frequency spacing ("LOG" or "LINEAR")
    # points     : Number of frequency points
    #
    # These parameters are used when calib_type = "spectrum".

    "init_freq": 1e3,
    "final_freq": 1e6,
    "scale": "LOG",
    "points": 4,

    # -------------------------------------------------------------------------
    # ADMX2001 Measurement Settings
    # gain_ch0 : Voltage channel gain
    # gain_ch1 : Current channel gain
    # mag      : Excitation signal magnitude [V]
    # count    : Number of measurements used for averaging

    "gain_ch0": 1,
    "gain_ch1": 1,
    "mag": 1.0,
    "count": 20,
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
        calibration = calibrate_utils.freq_calib(serialCom=ser, **CALIBRATION_CONFIG)

except serial.SerialException as error:
    print(f"Serial error: {error}")

except Exception as error:
    print(f"Error: {error}")

finally:
    if ser is not None and ser.is_open:
        ser.close()
        print("Serial port closed.")
