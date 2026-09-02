# ADMX2001_Term Framework

A Python-based framework for communicating with and controlling the **Analog Devices EVAL-ADMX2001B** evaluation board.

The framework provides a terminal-like interface for instrument configuration, impedance measurement, frequency sweep acquisition, and calibration procedures.

## Objectives

The main objectives of this project are:

- Establish communication with the EVAL-ADMX2001.
- Provide a terminal-like interface for sending commands and reading responses.
- Configure impedance measurement parameters.
- Perform frequency spectrum measurements.
- Acquire and store impedance data.
- Perform full-spectrum calibration.
- Store frequency-dependent calibration data.
- Apply calibration or compensation to subsequent measurements.

## Calibration

The framework is intended to perform calibration across the complete measurement frequency spectrum.

The calibration procedure will include:

1. Open calibration
2. Short calibration
3. Load calibration
4. Frequency-dependent calibration data storage
5. Calibration/compensation of measured impedance data

Each calibration point will be associated with its corresponding measurement frequency, allowing the correction to be applied across the complete impedance spectrum.

## Measurement Workflow

EVAL-ADMX2001  
↓  
Terminal Framework  
↓  
Instrument Configuration  
↓  
Calibration procedure
↓  
Electrical Impedance Spectroscopy  

## Project Structure

ADMX2001-Term/

    ADMX_calib.py
    
    ADMX_meas.py

    ADMX_plot.py
    
    utils/
        calibrate_utils.py
        meas_utils.py
        plot_utils.py

    requirements.txt

    README.md

## Requirements

The framework is developed in **Python**.

Required Python packages will be added to `requirements.txt` as the project evolves.

## Hardware

The initial development setup consists of:

- Analog Devices EVAL-ADMX2001B
- Impedance measurement fixture or sensor
- PC running the Python terminal framework

## Current Development

The project is currently under development.

The initial development focuses on:

- ADMX2001 communication
- Open, Short, and Load Calibration
- Full-spectrum Calibration
- Frequency sweep acquisition




## License

MIT License
