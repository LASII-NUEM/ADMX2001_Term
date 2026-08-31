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

ADMXport = "COM13"

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
        calibrate_utils.freq_calib(Cal_load=True, Cal_short=True, Cal_load=True,
                                   serialCom=ser,
                                   calib_type="Spectrum",
                                   init_freq=1e3, final_freq=1e6, scale="LOG", points=136, gainCh0=1, gainCh1=1, mag=1,
                                   count=20)

except serial.SerialException as error:
    print(f"Serial connection failed: {error}")
    ser = None
