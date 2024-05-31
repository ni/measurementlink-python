# import necessary modules
import nidcpower
from typing import List, Tuple


def dcpower_measure(
    record_length: int = 1,
    is_finite: bool = True,
    voltage_level: float = 5.0,
) -> Tuple[List[float], List[float], List[bool]]:
    with nidcpower.Session(resource_name="DCPower1") as session:
        session.measure_record_length = record_length
        session.measure_record_length_is_finite = is_finite
        session.measure_when = nidcpower.MeasureWhen.AUTOMATICALLY_AFTER_SOURCE_COMPLETE
        session.voltage_level = voltage_level

        session.commit()

        samples_acquired = 0

        voltage : List[float] = []
        current : List[float] = []
        in_compliance : List[bool] = []

        with session.initiate():
            channel_indices = "0-{}".format(session.channel_count - 1)
            channels = session.get_channel_names(channel_indices)
            for i, channel_name in enumerate(channels):
                samples_acquired = 0
                while samples_acquired < record_length:
                    measurements = session.channels[channel_name].fetch_multiple(
                        count=session.fetch_backlog
                    )
                    samples_acquired += len(measurements)

                    for i in range(len(measurements)):
                        voltage.append(measurements[i].voltage)
                        current.append(measurements[i].current)
                        in_compliance.append(measurements[i].in_compliance)

    return (voltage, current, in_compliance)


def main():
        result = dcpower_measure(record_length = 1, is_finite = True, voltage_level = 5.0)
        print("Return value:", result)


if __name__ == "__main__":
    main()
