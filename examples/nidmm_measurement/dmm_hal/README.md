## DMM Measurement 

This is a MeasurementLink example that acquires a single measurement from either NI-DMM or NI-VISA DMM.

### Features

- Uses the `nidmm` package and the open-source `PyVISA` package to access NI-DMM and NI-VISA from Python, respectively.
- Uses the open-source `PyVISA-sim` package to simulate instruments in software
- Pin-aware, supporting one session and one pin
  - Uses the same selected measurement function and range for all selected pin/site combinations.
- Includes InstrumentStudio project files
- Includes a TestStand sequence showing how to configure the pin map, register
  instrument sessions with the session management service, and run a measurement.
  - For the sake of simplicity, the TestStand sequence handles pin map and session registration and unregistration in the `Setup` and `Cleanup` sections of the main sequence. For **Test UUTs** and batch process model use cases, these steps should be moved to the `ProcessSetup` and `ProcessCleanup` callbacks.
- Uses the NI gRPC Device Server to allow sharing instrument sessions with other 
  measurement services when running measurements from TestStand

### Required Driver Software

- MeasurementLink 2024 Q1 or later
- NI-DMM 2023 Q1 or later
- NI-VISA 2024 Q1 or later
- NI-488.2 and/or NI-Serial
- Recommended: InstrumentStudio 2024 Q1 or later (matching MeasurementLink)
- Recommended: TestStand 2021 SP1 or later
- Optional: NI Instrument Simulator software

### Required Hardware

This example requires :

- NI DMM (e.g. PXIe-4081).
- HP/Agilent/Keysight 34401A.
- NI Instrument Simulator v2.0.

By default, this example uses a physical instrument or a simulated instrument
created in NI MAX. To automatically simulate an instrument without using NI MAX,
follow the steps below:

- Create a `.env` file in the measurement service's directory or one of its
  parent directories (such as the root of your Git repository or
  `C:\ProgramData\National Instruments\MeasurementLink\Services` for statically
  registered measurement services).
- Add the following options to the `.env` file to enable simulation via the
  driver's option string:

  ```
  MEASUREMENTLINK_NIDMM_SIMULATE=1
  MEASUREMENTLINK_NIDMM_BOARD_TYPE=PXIe
  MEASUREMENTLINK_NIDMM_MODEL=4081
  ```

  ```
  MEASUREMENTLINK_VISA_DMM_SIMULATE=1
  ```

### To simulate VISA DMM Using PyVISA-sim
The `_visa_dmm.py` instrument driver implements simulation using PyVISA-sim.
[`_visa_dmm_sim.yaml`](./_visa_dmm_sim.yaml) defines the behavior of the
simulated instrument.

To use a physical instrument:
- Connect the instrument to a supported interface, such as GPIB or serial.
- By default, the pin map included with this example uses the resource name
  `GPIB0::3::INSTR`, which matches the NI Instrument Simulator's factory default
  settings when connected via GPIB.
  - If this doesn't match your instrument's configuration, edit
    [`NIVisaDmmMeasurement.pinmap`](./NIVisaDmmMeasurement.pinmap) and replace
    `GPIB0::3::INSTR` with the desired resource name (e.g. `ASRL1::INSTR`).
  - To modify the NI Instrument Simulator configuration (e.g. GPIB address,
    serial configuration), use the `Instrument Simulator Wizard` included with
    the NI Instrument Simulator software.
  - To configure third party instruments, see the documentation provided with
    the instrument.
