import numpy as np
import tkinter as tk
from tkinter import messagebox

from datetime import datetime
import time


class freq_meas:

    def __init__(
            self,
            serialCom,
            meas_type: str,
            init_freq: float,
            final_freq: float,
            scale: str,
            points: int,
            freq: float,
            gain_ch0: int,
            gain_ch1: int,
            mag: float,
            count: int,
            mode: int,
            avg: int,
            cal_open: bool,
            cal_short: bool,
            cal_load: bool,
            offset: float = 0,
            delay: float = 200,
    ):

        """
        :param calib_type: Type of calibration procedure. Defines whether the
                           calibration is performed over a frequency spectrum or
                           at a single frequency.

        :param freq: Frequency used for a single-frequency calibration, in Hz.
                     Ignored when calib_type is set to "Spectrum".

        :param init_freq: Initial frequency of the calibration spectrum, in Hz.

        :param final_freq: Final frequency of the calibration spectrum, in Hz.

        :param scale: Frequency spacing used for the spectrum. Supported values
                      are "LOG" for logarithmic spacing and "LIN" for linear spacing.

        :param points: Number of frequency points between init_freq and final_freq.

        :param gainCh0: Gain setting applied to ADMX2001 measurement channel 0.

        :param gainCh1: Gain setting applied to ADMX2001 measurement channel 1.

        :param mag: Excitation signal magnitude used during the calibration.

        :param count: Number of measurements/acquisitions performed at each
                      frequency point.
        """
        self.ser = serialCom
        self.meastype = meas_type.lower()
        self.Freq = freq * 1e-3
        self.init_freq = init_freq * 1e-3
        self.final_freq = final_freq * 1e-3
        self.scale = scale.lower()
        self.Freqpoints = points
        self.gain_Ch0 = gain_ch0
        self.gain_Ch1 = gain_ch1
        self.mag = mag
        self.count = count
        self.offset = offset
        self.delay = delay
        self.mode = mode
        self.avg = avg

        self.Cal_open = cal_open
        self.Cal_short = cal_short
        self.Cal_load = cal_load

        scaleType = ("log", "linear")
        if self.scale not in scaleType:
            raise TypeError(f"[ADMX_Calibrate] Unknown Scale Type! Available Types:{type(scaleType)}")

        MeasType = ("freq", "spectrum")
        if self.meastype not in MeasType:
            raise TypeError(f"[ADMX_Calibrate] Unknown Calibration Type! Available Types:{type(MeasType)}")

        DISPLAY_MODES = {0: ("Cs", "Rs"), 1: ("Cs", "D"), 2: ("Cs", "Q"), 3: ("Ls", "Rs"), 4: ("Ls", "D"),
                         5: ("Ls", "Q"), 6: ("R", "X"), 7: ("Z", "deg"), 8: ("Z", "rad"), 9: ("Cp", "Rp"),
                         10: ("Cp", "D"), 11: ("Cp", "Q"), 12: ("Lp", "Rp"), 13: ("Lp", "D"), 14: ("Lp", "Q"),
                         15: ("G", "B"), 16: ("Y", "deg"), 17: ("Y", "rad"), 18: ("None", "None"), }
        if self.mode not in DISPLAY_MODES:
            raise ValueError(f"[ADMX_Measure] Unknown Display Mode '{self.mode}'. "
                             f"Available modes: {tuple(DISPLAY_MODES.keys())}")

        calibrate_list = self.cmd("calibrate list")[:-1]
        # if not self.calibration_check(calibrate_list):
        #     raise RuntimeError("[ADMX_Measure] Missing calibration. "
        #                        "Please recalibrate the ADMX2001 before measuring.")

        if self.meastype == "freq":
            self.freq_meas()

        elif self.meastype == "spectrum":

            if self.scale == "log":
                self.freq_array = np.logspace(np.log10(self.init_freq), np.log10(self.final_freq), self.Freqpoints)
            elif self.scale == "linear":
                self.freq_array = np.linspace(self.init_freq, self.final_freq, self.Freqpoints)

            self.Spectrum_meas()

        else:
            raise TypeError(f"[ADMX_Calibrate] Unknown Calibration Type! Available Types:{type(MeasType)}")

    def cmd(self, command):
        """
        :param command:
        :return:
        """
        if self.ser is None or not self.ser.is_open:
            raise ConnectionError("Serial connection is not open.")

        command_lower = command.lower().strip()

        print(f"TX: {command}\n")

        self.ser.write((command + "\n").encode())
        self.ser.flush()

        time.sleep(0.1)

        # Discard terminal input/echo
        self.ser.readline()

        if command_lower.startswith("z") or command_lower.startswith("calibrate list"):
            response = []
            while True:

                line = self.ser.readline().decode(errors="ignore").strip()

                if not line:
                    break

                response.append(line)
                if line.startswith("Status:"):
                    break

            print("RX:")
            for line in response[:-1]:
                print(line)
            print("\n")

            return response

        # NORMAL SINGLE-LINE RESPONSE
        response = self.ser.readline().decode(errors="ignore").strip()
        print(f"RX: {response}\n")

        return response

    def calibration_check(self, calibrate_list):

        for freq_line in calibrate_list:

            freq = float(freq_line.split(":")[1].split()[0])
            response = self.cmd(f"calibrate list {freq}")

            status = {"open": False, "short": False, "load": False, }

            for line in response:
                line_lower = line.lower()
                for cal_type in status:
                    if line_lower.startswith(f"{cal_type}:"):
                        status[cal_type] = (
                                line_lower.split(":", 1)[1].strip() == "done")

            required = {
                "open": self.Cal_open,
                "short": self.Cal_short,
                "load": self.Cal_load,
            }

            for cal_type, required_cal in required.items():
                if required_cal and not status[cal_type]:
                    raise RuntimeError(
                        f"[ADMX_Calibrate] {cal_type.upper()} calibration "
                        f"missing at {freq} kHz."
                    )
        return True

    def saveCSV(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = f"./results/ADMX_{timestamp}.npy"

        data = {key: value for key, value in self.__dict__.items() if key != "ser"}
        np.save(filepath, data, allow_pickle=True)

        print(f"[ADMX_Measure] Measurement saved:\n{filepath}")

        return True

    def freq_meas(self):

        self.cmd(f"setgain ch0 {self.gain_Ch0}")
        self.cmd(f"setgain ch1 {self.gain_Ch1}")
        self.cmd(f"frequency {self.Freq}")
        self.cmd(f"magnitude {self.mag}")
        self.cmd(f"offset {self.offset}")
        self.cmd(f"average {self.avg}")
        self.cmd(f"tdelay {self.delay}")
        self.cmd(f"count {self.count}")
        self.cmd(f"display {self.mode}")

        self.freq_meas_result = self.cmd(f"z")

        if not self.saveCSV():
            raise TypeError(f"[ADMX_Measure] Unable to save to measurement in (.npy) file.")

        return None

    def Spectrum_meas(self):

        self.cmd(f"setgain ch0 {self.gain_Ch0}")
        self.cmd(f"setgain ch1 {self.gain_Ch1}")
        self.cmd(f"magnitude {self.mag}")
        self.cmd(f"offset {self.offset}")
        self.cmd(f"average {self.avg}")
        self.cmd(f"tdelay {self.delay}")
        self.cmd(f"count {self.count}")
        self.cmd(f"display {self.mode}")

        self.freq_meas_result = []

        for i, freq in enumerate(self.freq_array):
            self.cmd(f"frequency {freq}")
            response = self.cmd("z")[:-1]
            self.freq_meas_result.append(response)

        self.freq_meas_result = np.array(self.freq_meas_result)

        if not self.saveCSV():
            raise TypeError(f"[ADMX_Measure] Unable to save to measurement in (.npy) file.")


        return None
