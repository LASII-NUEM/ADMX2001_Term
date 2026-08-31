import numpy as np
import tkinter as tk
from tkinter import messagebox


class freq_calib:

    def __init__(
            self,
            serialCom,
            rt: float,
            xt: float,
            calib_type: str,
            init_freq: float,
            final_freq: float,
            scale: str,
            points: int,
            Cal_open: bool = True,
            Cal_short: bool = True,
            Cal_load: bool = True,
            freq: float = 1e6,
            gainCh0: int = 1,
            gainCh1: int = 1,
            mag: float = 1,
            count: int = 20,
            offset: float = 0,
            delay: float = 0
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
        self.caltype = calib_type.lower()
        self.Freq = freq
        self.init_freq = init_freq
        self.final_freq = final_freq
        self.scale = scale.lower()
        self.Freqpoints = points
        self.gainCh0 = gainCh0
        self.gainCh1 = gainCh1
        self.mag = mag
        self.count = count
        self.offset = offset
        self.delay = delay

        self.Cal_open = Cal_open
        self.Cal_short = Cal_short
        self.Cal_load = Cal_load

        self.rt = rt
        self.xt = xt

        scaleType = ("log", "linear")
        if self.scale not in scaleType:
            raise TypeError(f"[ADMX_Calibrate] Unknown Scale Type! Available Types:{type(scaleType)}")

        CalType = ("freq", "spectrum")
        if self.caltype not in CalType:
            raise TypeError(f"[ADMX_Calibrate] Unknown Calibration Type! Available Types:{type(CalType)}")

        if self.caltype == "freq":
            self.freq_calib()

        elif self.caltype == "spectrum":

            if self.scale == "log":
                self.freq_array = np.logspace(np.log10(self.init_freq), np.log10(self.final_freq), self.Freqpoints)
            elif self.scale == "linear":
                self.freq_array = np.linspace(self.init_freq, self.final_freq, self.Freqpoints)

            self.Spectrum_calib()

        else:
            raise TypeError(f"[ADMX_Calibrate] Unknown Calibration Type! Available Types:{type(CalType)}")

    def cmd(self, command):

        if self.ser is None or not self.ser.is_open:
            raise ConnectionError("Serial connection is not open.")

        self.ser.write((command + "\n").encode())

        response = self.ser.readline().decode().strip()

        return response

    def confirm_hardware_setup(self,calib_type):

        root = tk.Tk()
        root.withdraw()

        message = (f"Prepare the hardware for {calib_type.upper()} calibration.\n\n"
                   "Confirm that the correct calibration setup is set"
                   "to the ADMX2001 before continuing.")

        confirmed = messagebox.askyesno(title="ADMX2001 Calibration", message=message)

        root.destroy()

        return confirmed

    def check_calibration(self, response, calib_type):

        target = calib_type.lower()

        for line in response:

            if line.lower().startswith(f"{target}:"):

                status = line.split(":", 1)[1].strip()

                if status.lower() == "done":
                    return True

                return False

        return False

    def freq_calib(self):

        self.cmd(f"setgain ch0 {self.gainCh0}")
        self.cmd(f"setgain ch1 {self.gainCh1}")
        self.cmd(f"frequency {self.Freq}")
        self.cmd(f"magnitude {self.mag}")
        self.cmd(f"offset {self.offset}")
        self.cmd(f"average {self.count}")
        self.cmd(f"tdelay {self.delay}")

        if self.Cal_open is True:

            if not self.confirm_hardware_setup("open"):
                print("Open calibration cancelled by user.")
                return False

            open_cal_response = self.cmd(f"calibrate open")

            if self.check_calibration(open_cal_response, "open"):
                print("Open calibration completed successfully.")

                self.cmd(f"calibrate commit")
                self.cmd(f"Analog123")

            else:
                raise RuntimeError(f" Open calibration was not completed.")

        if self.Cal_short is True:

            if not self.confirm_hardware_setup("short"):
                print("Short Calibration cancelled by user.")
                return False

            self.cmd(f"magnitude 0.2")

            short_cal_response = self.cmd(f"calibrate short")

            if self.check_calibration(short_cal_response, "short"):
                print("short calibration completed successfully.")

                self.cmd(f"calibrate commit")
                self.cmd(f"Analog123")

            else:
                raise RuntimeError(f" Short calibration was not completed.")

            self.cmd(f"magnitude {self.mag}")

        if self.Cal_load is True:

            if not self.confirm_hardware_setup("load"):
                print("Load Calibration cancelled by user.")
                return False

            load_cal_response = self.cmd(f"calibrate load rt {self.rt} xt {self.xt}")

            if self.check_calibration(load_cal_response, "load"):
                print("load calibration completed successfully.")

                self.cmd(f"calibrate commit")
                self.cmd(f"Analog123")

            else:
                raise RuntimeError(f" Load calibration was not completed.")

    def Spectrum_calib(self):

        return
