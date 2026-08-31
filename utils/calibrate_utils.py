import numpy as np
import serial


class freq_calib:

    def __init__(self,
                 Cal_load=True,
                 Cal_short=True,
                 Cal_load=True,
                 serialCom=ser,
                 calib_type="Spectrum",
                 freq = 1e6,
                 init_freq=1e3,
                 final_freq=1e6,
                 scale="LOG",
                 points=136,
                 gainCh0 = 1,
                 gainCh1 =1,
                 mag = 1,
                 count = 20,
                 offset = 0,
                 delay = 0):

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
        self.caltype = calib_type
        self.Freq = freq
        self.init_freq = init_freq
        self.final_freq = final_freq
        self.scale = scale
        self.Freqpoints = points
        self.gainCh0 = gainCh0
        self.gainCh1 = gainCh1
        self.mag = mag
        self.count = count
        self.offset = offset
        self.delay = delay

        self.Cal_load = Cal_load
        self.Cal_short = Cal_short
        self.Cal_load = Cal_load

        scaleType = ("LOG", "Linear")
        if scaleType not in  self.scale:
            raise TypeError(f"[ADMX_Calibrate] Unknown Scale Type! Available Types:{type(scaleType)}")

        CalType = ("Freq", "Spectrum")
        if CalType not in  self.caltype:
            raise TypeError(f"[ADMX_Calibrate] Unknown Calibration Type! Available Types:{type(CalType)}")

        if self.caltype == "Freq":
            self.freq_calib(self.Freq)
        elif CalType == "Spectrum":
            if self.scale == "LOG":
                self.freq_array = np.logspace(self.init_freq, self.final_freq, self.Freqpoints)
                self.Spectrum_calib(self.freq_array)
            elif self.scale == "Linear":
                self.freq_array = np.linspace(self.init_freq, self.final_freq, self.Freqpoints)
                self.Spectrum_calib(self.freq_array)
            else:
                raise TypeError(f"[ADMX_Calibrate] Unknown Scale Type! Available Types:{type(scaleType)}")
        else:
            raise TypeError(f"[ADMX_Calibrate] Unknown Calibration Type! Available Types:{type(CalType)}")

    def cmd(self, command):

        if self.ser is None or not self.ser.is_open:
            raise ConnectionError("Serial connection is not open.")

        self.ser.write((command + "\n").encode())

        response = self.ser.readline().decode().strip()

        return response


    def freq_calib(self):

        self.cmd(f"setgain ch0 {self.gainCh0}")
        self.cmd(f"setgain ch1 {self.gainCh1}")
        self.cmd(f"frequency {self.Freq}")
        self.cmd(f"magnitude {self.mag}")
        self.cmd(f"offset {self.offset}")
        self.cmd(f"average {self.count}")
        self.cmd(f"tdelay {self.delay}")

        if self.Cal_open is True:
            self.cmd(f"calibrate open")
        if self.Cal_short is True:
            self.cmd(f"calibrate short")
        if self.Cal_load is True:
            self.cmd(f"calibrate load rt {self.rt} xt {self.xt}")

        response = self.cmd(f"calibrate")




    def Spectrum_calib(self):

        return
