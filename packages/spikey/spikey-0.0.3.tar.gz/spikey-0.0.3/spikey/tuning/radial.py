from imlib.radial.temporal import angle_bin_occupancy

from spikey.histogram.radial import radial_spike_histogram


def calculate_tuning(
    angle_timeseries,
    spikes_timeseries,
    frames_per_sec,
    bin_width=6,
    degrees=True,
):
    """
    Calculate the tuning for a single time series of angle and spikes

    :param angle_timeseries: array like timeseries of angles
    :param spikes_timeseries: array like timeseries of spikes, with N spikes
    per timepoint
    :param frames_per_sec: How many angle values are recorded each second
    :param bin_width: Size of bin used for histogram
    :param degrees: Use degrees, rather than radians
    :return: Radial spike tuning histogram, and bin occupancy histogram

    """
    bin_occupancy, _ = angle_bin_occupancy(
        angle_timeseries, frames_per_sec, bin_size=bin_width
    )
    tuning, _ = radial_spike_histogram(
        angle_timeseries,
        spikes_timeseries,
        bin_width,
        bin_occupancy=bin_occupancy,
        degrees=degrees,
    )

    return tuning, bin_occupancy
