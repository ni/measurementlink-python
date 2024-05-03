# HAL in MeasurementLink examples - Workflow for measurement creation or porting existing HAL

The measurements in MeasurementLink can be easily modified to implement hardware abstraction to switch between different instrument models of same instrument type easily via pinmap file.

A new instrument model can be included with help of existing HAL libraries in the `nidmm_measurement` example or an existing HAL implementation in different framework can be ported.

## Pre-requisites

* Basic MeasurementLink plugin workflow understanding.
* Python experience.
* Basic understanding of existing HAL implementation in case of porting existing HAL implementation from other framework.

## Existing HAL Helper Libraries in MeasurmentLink

The `nidmm_measurement` [example](https://github.com/ni/measurementlink-python/tree/users/vikram/dmm-hal-implementation/examples/nidmm_measurement) implements HAL for different dmm instruments.

This Hal library can be reused to implement an instrument-based solution.

The HAL library implementation is placed in `dmm_hal` folder which involves the following classes or modules:

* ***dmm.py*** - Base class for all instrument models for DMM instruments, which initializes the corresponding instrument based on the selected pin map and returns the session object.
  * ***DmmHal*** - Assists in mapping the corresponding instrument model for the given pin.
* ***dmm_ni.py*** - NI DMM-related methods are placed here.
* ***dmm_visa.py*** - VISA DMM-related methods are placed here.

## Measurement creation with Hardware Abstraction

![DMM HAL](DMM%20Hal%20hierarchy.png)

### Steps to create new instrument model with the help of existing HAL libraries

Consider the need to create a generic measurement for an `NI DMM` and `VISA DMM` instrument to acquire a single DC voltage. The following workflow will assist in integrating the new DMM instrument model:

1. Create a file with the instrument name (`dmm.py`) containing a class with an initialize API, which will perform the following operations sequentially:
   1. Reserve the session.
   2. Use a helper method (`DmmHal`) to find the corresponding model object:
      1. Users should create a class and methods for any instrument model they require.
      2. Link the class with its actual instrument name in the `DmmHal` helper method so that it returns the proper instrument object based on the chosen instrument type.
   3. Initialize the session using the instrument object.
   4. Return the initialized session.
2. Create the necessary classes for the required instrument models.
3. Add configuration and session read in the `measurement.py`.
4. In `instudioproj`, `measui`, `TestStand sequence`, and `pin map`, create all the necessary files following the same format as the MeasurementLink workflow. There are no changes needed there.