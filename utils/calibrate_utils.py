import numpy as np
import tkinter as tk
from tkinter import messagebox
import time


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
            cal_open: bool = True,
            cal_short: bool = True,
            cal_load: bool = True,
            freq: float = 1e6,
            gain_ch0: int = 1,
            gain_ch1: int = 1,
            mag: float = 1,
            count: int = 20,
            offset: float = 0,
            delay: float = 200):

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

        self.Cal_open = cal_open
        self.Cal_short = cal_short
        self.Cal_load = cal_load

        self.open_cal_response = None
        self.short_cal_response = None
        self.load_cal_response = None

        self.rt = rt
        self.xt = xt

        # First of all Erase the previous calibration
        self.cmd(f"calibrate erase")
        erase_response = self.cmd(f"Analog123")

        if erase_response.lower().startswith("erase : success"):
            print(f"Erase calibration completed. \n")
        else:
            raise RuntimeError(f" Erase Calibration was not completed.")

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

        # CALIBRATE COMMIT
        if command_lower.startswith("calibrate commit"):
            return None

        # CALIBRATE ERASE
        if command_lower.startswith("calibrate erase"):
            return None

        # CALIBRATE COMMIT
        if command_lower.startswith("calibrate list") and self.caltype == "freq":
            response = self.ser.readline().decode(errors="ignore").strip()
            print(f"RX: {response}\n")
            return response

        # MULTILINE CALIBRATION RESPONSE
        if command_lower.startswith("calibrate"):

            response = []

            while True:

                line = self.ser.readline().decode(errors="ignore").strip()

                if not line:
                    break

                response.append(line)
                if line.startswith("Status:"):
                    break

            print("RX:")
            for line in response:
                print(line)

            return response

        # NORMAL SINGLE-LINE RESPONSE
        response = self.ser.readline().decode(errors="ignore").strip()
        print(f"RX: {response}\n")

        return response

    def confirm_hardware_setup(self, calib_type):
        """
        :param calib_type:
        :return:
        """
        root = tk.Tk()
        root.withdraw()

        message = (f"Prepare the hardware for {calib_type.upper()} calibration.\n\n"
                   "Confirm that the correct calibration setup is set"
                   "to the ADMX2001 before continuing.")

        confirmed = messagebox.askyesno(title="ADMX2001 Calibration", message=message)

        root.destroy()

        return confirmed

    def check_calibration(self, calib_type):

        target = calib_type.lower()
        response = getattr(self, f"{calib_type}_cal_response")

        for line in response:

            if line.lower().startswith(f"{target}:"):

                status = line.split(":", 1)[1].strip()

                if status.lower() == "done":
                    return True

                return False

        return False

    def calibrate(self, calib_type, first_freq = True):

        if first_freq:
            if not self.confirm_hardware_setup(calib_type):
                print(f"{calib_type} calibration cancelled by user.\n")
                return False

        if calib_type == "load":
            setattr(self, f"{calib_type}_cal_response", self.cmd(f"calibrate rt {self.rt} xt {self.xt}"))
        else:
            setattr(self, f"{calib_type}_cal_response", self.cmd(f"calibrate {calib_type}"))

        if self.check_calibration(calib_type):
            print(f"{calib_type} calibration completed successfully.\n")

            self.cmd(f"calibrate commit")
            commit_response = self.cmd(f"Analog123")

            if commit_response.lower().startswith("commit : success"):
                print(f"{calib_type} calibration commited. \n")
            else:
                raise RuntimeError(f"{calib_type} Calibration was not commited.")

        else:
            raise RuntimeError(f" {calib_type} calibration was not completed.")

        return True

    def freq_calib(self):
        """
        :return:
        """
        self.cmd(f"setgain ch0 {self.gain_Ch0}")
        self.cmd(f"setgain ch1 {self.gain_Ch1}")
        self.cmd(f"frequency {self.Freq}")
        self.cmd(f"magnitude {self.mag}")
        self.cmd(f"offset {self.offset}")
        self.cmd(f"average {self.count}")
        self.cmd(f"tdelay {self.delay}")

        if self.Cal_open:
            self.calibrate("open", True)

        if self.Cal_short:
            self.cmd(f"magnitude 0.2")
            self.calibrate("short", True)
            self.cmd(f"magnitude {self.mag}")

        if self.Cal_load:
            self.calibrate("load", True)

        Checkout_list = self.cmd(f"calibrate list")
        List_freq = float(Checkout_list.split(":")[1].split()[0])

        if List_freq == self.Freq:
            root = tk.Tk()
            root.withdraw()

            message = (f"Calibration at {self.Freq} kHz completed and saved successfully.\n\n"
                       "To begin measurements, run ADMX_MEAS.")

            messagebox.showinfo(title="ADMX2001 Calibration", message=message)

            root.destroy()

        return None

    def Spectrum_calib(self):
        """
        :return:
        """
        self.cmd(f"setgain ch0 {self.gain_Ch0}")
        self.cmd(f"setgain ch1 {self.gain_Ch1}")
        self.cmd(f"magnitude {self.mag}")
        self.cmd(f"offset {self.offset}")
        self.cmd(f"average {self.count}")
        self.cmd(f"tdelay {self.delay}")

        if self.Cal_open:
            for i, freq in enumerate(self.freq_array):
                self.cmd(f"frequency {freq}")
                self.calibrate("open", first_freq = (i == 0))

        if self.Cal_short:
            self.cmd(f"magnitude 0.2")
            for i, freq in enumerate(self.freq_array):
                self.cmd(f"frequency {freq}")
                self.calibrate("short", first_freq = (i == 0))
            self.cmd(f"magnitude {self.mag}")

        if self.Cal_load:
            for i, freq in enumerate(self.freq_array):
                self.cmd(f"frequency {freq}")
                self.calibrate("load", first_freq=(i == 0))

        Checkout_list = self.cmd("calibrate list")[:-1]

        if len(Checkout_list) == self.Freqpoints:
            root = tk.Tk()
            root.withdraw()

            message = (f"Spectrum Calibration at: \n"
                       f"{self.init_freq} - {self.final_freq} [kHz] | {self.Freqpoints} points \n\n"
                       f"Completed and saved successfully.\n\n"
                       "To begin measurements, run ADMX_MEAS.py")
            messagebox.showinfo(title="ADMX2001 Calibration", message=message)
            root.destroy()
        else:
            raise RuntimeError(f" Calibration List was not completed.")


        return None
