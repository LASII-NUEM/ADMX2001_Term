import numpy as np
import os
import matplotlib.pyplot as plt


class ReadNPY:
    DISPLAY_MODES = {
        0: ("Cs", "Rs"),
        1: ("Cs", "D"),
        2: ("Cs", "Q"),
        3: ("Ls", "Rs"),
        4: ("Ls", "D"),
        5: ("Ls", "Q"),
        6: ("R", "X"),
        7: ("Z", "deg"),
        8: ("Z", "rad"),
        9: ("Cp", "Rp"),
        10: ("Cp", "D"),
        11: ("Cp", "Q"),
        12: ("Lp", "Rp"),
        13: ("Lp", "D"),
        14: ("Lp", "Q"),
        15: ("G", "B"),
        16: ("Y", "deg"),
        17: ("Y", "rad"),
        18: ("None", "None")
    }

    UNITS = {
        "Cs": "F",
        "Cp": "F",
        "Ls": "H",
        "Lp": "H",
        "Rs": "Ω",
        "Rp": "Ω",
        "R": "Ω",
        "X": "Ω",
        "Z": "Ω",
        "G": "S",
        "B": "S",
        "Y": "S",
        "D": "",
        "Q": "",
        "deg": "°",
        "rad": "rad",
        "None": ""
    }

    def __init__(self, filepath):

        self.filepath = filepath

        if not os.path.isfile(filepath):
            raise FileNotFoundError(f'[file_utils] Filename {filepath} does not exist!')

        self.data = np.load(filepath, allow_pickle=True).item()

        self.meastype = self.data["meastype"].lower()
        self.count = int(self.data["count"])
        self.mode = int(self.data["mode"])
        self.axis = self.data["scale"]

        MeasType = ("freq", "spectrum")
        if self.meastype == "freq":
            self.freq = np.array([self.data["Freq"]], dtype=float)
            self.raw = np.asarray(self.data["freq_meas_result"][:-1])

        elif self.meastype == "spectrum":
            self.freq = np.asarray(self.data["freq_array"], dtype=float)
            self.raw = np.asarray(self.data["freq_meas_result"])

        else:
            raise TypeError(f"[ADMX_meas] Unknown Calibration Type! Available Types:{type(MeasType)}")

        if self.mode not in self.DISPLAY_MODES:
            raise ValueError(f"[ADMX_Read] Unknown display mode - current mode:{self.mode}.")

        if self.mode == 18:
            raise ValueError("[ADMX_Read] Display mode 18 contains "
                             "no measurement parameters.")

        self.meas1, self.meas2 = \
            self.DISPLAY_MODES[self.mode]

        self.unit1 = self.UNITS[self.meas1]
        self.unit2 = self.UNITS[self.meas2]

        if self.raw.ndim == 1:
            self.raw = self.raw.reshape(1, -1)

        expected_shape = (len(self.freq), self.count)

        if self.raw.shape != expected_shape:
            raise ValueError(f"[ADMX_Read] Result array has "
                             f"incorrect shape. "
                             f"Expected {expected_shape}, "
                             f"got {self.raw.shape}.")

        # ---------------------------------------------------------------------
        # Process data
        # ---------------------------------------------------------------------

        self.retry = np.zeros(expected_shape, dtype=int)
        self.meas1_array = np.zeros(expected_shape, dtype=float)
        self.meas2_array = np.zeros(expected_shape, dtype=float)

        self._process()

        self.meas1_mean = np.mean(self.meas1_array, axis=1)
        self.meas2_mean = np.mean(self.meas2_array, axis=1)

        self.meas1_std = np.std(self.meas1_array, axis=1)
        self.meas2_std = np.std(self.meas2_array, axis=1)

    def _process(self):

        for f_idx in range(len(self.freq)):

            for retry_idx in range(self.count):

                response = str(self.raw[f_idx, retry_idx]).strip()

                values = response.split(",")

                if len(values) != 3:
                    raise ValueError(f"[ADMX_Read] Invalid response:'{response}'")

                try:
                    retry = int(values[0])
                    value1 = float(values[1])
                    value2 = float(values[2])

                except ValueError as exc:
                    raise ValueError(f"[ADMX_Read] Could not parse '{response}'.") from exc

                if retry != retry_idx:
                    raise ValueError(f"[ADMX_Read] Retry mismatch."
                                     f"Expected {retry_idx}, received {retry}.")

                self.retry[f_idx, retry_idx] = retry

                self.meas1_array[f_idx, retry_idx] = value1
                self.meas2_array[f_idx, retry_idx] = value2

    def plot(self):

        data = self

        ylabel1 = (f"{data.meas1} [{data.unit1}]"
                   if data.unit1 else data.meas1)

        ylabel2 = (f"{data.meas2} [{data.unit2}]"
                   if data.unit2 else data.meas2)

        if data.meastype == "spectrum":

            fig, ax1 = plt.subplots(figsize=(10, 6))
            ax2 = ax1.twinx()
            for retry in range(data.count):

                if self.axis == "log":
                    ax1.semilogx(data.freq, data.meas1_mean, color="b", label=f"Retry {retry}")
                    ax2.semilogx(data.freq, data.meas2_mean, color="r", label=f"Retry {retry}")
                if self.axis == "linear":
                    ax1.loglog(data.freq, data.meas1_mean, color="b", label=f"Retry {retry}")
                    ax2.loglog(data.freq, data.meas2_mean, color="r", label=f"Retry {retry}")

            ax1.set_xlabel("Frequency [Hz]")
            ax1.set_ylabel(ylabel1)
            ax2.set_ylabel(ylabel2)

            ax1.set_title(f"ADMX2001 - Average {data.meas1} | {data.meas2}")
            ax1.grid(True)
            plt.tight_layout()
            plt.show()

        elif data.meastype == "freq":

            fig, ax1 = plt.subplots(figsize=(10, 6))
            ax2 = ax1.twinx()
            retries = np.arange(data.count)

            ax1.plot(retries, data.meas1_array[0, :], color="b", label=data.meas1)
            ax2.plot(retries, data.meas2_array[0, :], color="r", label=data.meas2)

            ax1.set_xlabel("Frequency [Hz]")
            ax1.set_ylabel(ylabel1)
            ax2.set_ylabel(ylabel2)

            ax1.set_title(f"ADMX2001 - {data.meas1} | {data.meas2} "
                          f"@ {data.freq[0]:g} Hz")

            ax1.grid(True)

            # Mean and standard deviation text
            text = (f"{data.meas1}: "
                    f"mean = {data.meas1_mean[0]:.4e}, std = {data.meas1_std[0]:.4e}\n"
                    f"{data.meas2}: "
                    f"mean = {data.meas2_mean[0]:.4e}, std = {data.meas2_std[0]:.4e}")

            ax1.text(0.3, 0.98, text,
                     transform=ax1.transAxes,
                     verticalalignment="top",
                     bbox=dict(boxstyle="round", alpha=0.2))

            lines1, labels1 = ax1.get_legend_handles_labels()
            lines2, labels2 = ax2.get_legend_handles_labels()
            ax1.legend(lines1 + lines2, labels1 + labels2)

            plt.tight_layout()
            plt.show()

        else:
            raise ValueError(f"[ADMX_plot] Unknown measurement type. Curr. type {data.meastype}.")
