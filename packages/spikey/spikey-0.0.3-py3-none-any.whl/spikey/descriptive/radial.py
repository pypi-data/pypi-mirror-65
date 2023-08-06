from math import isclose
from pycircstat.descriptive import corrcc
from imlib.array.misc import split_array_half

from spikey.tuning.radial import calculate_tuning


def radial_tuning_stability(
    angle_timeseries,
    spikes_timeseries,
    bin_width,
    frames_per_sec,
    degrees=True,
):
    """
    For a given cell, split the recording into two halves, and a tuning curve
    will be generated for each half separately. The correlation between
    these two tuning curves is then calcuated as the "stability_index"

    :param angle_timeseries: array like timeseries of angles
    :param spikes_timeseries: array like timeseries of spikes, with N spikes
    per timepoint
    :param bin_width: Size of bin used for histogram
    :param frames_per_sec: How many angle values are recorded each second
    :param degrees: Use degrees, rather than radians
    :return:
    """
    assert len(angle_timeseries) == len(spikes_timeseries)

    angle_timeseries_a, angle_timeseries_b = split_array_half(angle_timeseries)
    spikes_timeseries_a, spikes_timeseries_b = split_array_half(
        spikes_timeseries
    )

    tuning_a, angle_bin_occupancy_a = calculate_tuning(
        angle_timeseries_a,
        spikes_timeseries_a,
        frames_per_sec,
        bin_width=bin_width,
        degrees=degrees,
    )
    tuning_b, angle_bin_occupancy_b = calculate_tuning(
        angle_timeseries_b,
        spikes_timeseries_b,
        frames_per_sec,
        bin_width=bin_width,
        degrees=degrees,
    )

    # make sure total occupancy is the same as the length of the timeseries
    assert isclose(
        sum(angle_bin_occupancy_a) + sum(angle_bin_occupancy_b),
        len(angle_timeseries) / frames_per_sec,
        abs_tol=0.0001,
    )

    # Stability of the same time half against itself should be 1
    assert corrcc(tuning_a, tuning_a) == 1
    assert corrcc(tuning_b, tuning_b) == 1

    return corrcc(tuning_a, tuning_b)
