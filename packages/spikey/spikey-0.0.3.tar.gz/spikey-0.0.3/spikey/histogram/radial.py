import numpy as np

from imlib.radial.misc import radial_bins
from imlib.array.misc import midpoints_of_series


def radial_spike_histogram_multiple(
    angle_timeseries_list,
    spikes_timeseries_list,
    bin_width=6,
    bin_occupancy=None,
    normalise=False,
    degrees=True,
):
    """
    Calculates a radial spiking histogram for a list of cells. From a list
    of angles and spikes timeseries, calculate radial spiking histograms for
    each cell, and return a list of histogram bin centers and spike histograms
    (optionally normalised for the occupancy of each bin).

    N.B. THIS FUNCTION CONVERTS DEGREE INPUT TO RADIANS

    :param angle_timeseries_list: list of array like timeseries of angles
    (in degrees)
    :param spikes_timeseries_list: list of array like timeseries of spikes,
    with N spikes per timepoint
    :param bin_width: Size of bin used for histogram
    :param bin_occupancy: Array like timeseries of temporal occupancy of bins.
    If specified, the relative spike rates will be returned.
    :param normalise: Normalise the resulting histogram
    :param degrees: Use degrees, rather than radians
    :return: List of spikes per radial bin (possibly normalised for occupancy),
    and the bin centers of the histogram used (in radians)

    """
    assert len(angle_timeseries_list) == len(spikes_timeseries_list)

    spikes_per_bin = []
    number_of_cells = len(angle_timeseries_list)
    for idx, v in enumerate(range(number_of_cells)):
        hist_weight = spikes_timeseries_list[idx]
        spikes_per_bin_cell, histogram_bin_center = radial_spike_histogram(
            angle_timeseries_list[idx],
            hist_weight,
            bin_width,
            bin_occupancy=bin_occupancy,
            normalise=normalise,
            degrees=degrees,
        )
        spikes_per_bin.append(spikes_per_bin_cell)

    return spikes_per_bin, histogram_bin_center


def radial_spike_histogram(
    angle_timeseries,
    spikes_timeseries,
    bin_width,
    bin_occupancy=None,
    normalise=False,
    degrees=True,
):
    """
    From a timeseries of angles and spikes, calculate a radial spiking
    histogram

    :param angle_timeseries: array like timeseries of angles
    :param spikes_timeseries: array like timeseries of spikes, with N spikes
    per timepoint
    :param bin_width: Size of bin used for histogram
    :param bin_occupancy: Array like timeseries of temporal occupancy of bins.
    If specified, the relative spike rates will be returned.
    :param normalise: Normalise the resulting histogram
    :param degrees: Use degrees, rather than radians
    :return: Spikes (or spike rate) per radial bin and histogram bin centers
    (in radians)

    """
    spikes_per_bin, bins = np.histogram(
        angle_timeseries,
        weights=spikes_timeseries,
        bins=radial_bins(bin_width, degrees=degrees),
        density=normalise,
    )
    if bin_occupancy is not None:
        spikes_per_bin = np.divide(spikes_per_bin, bin_occupancy)
    if degrees:
        bin_centers = np.deg2rad(midpoints_of_series(bins))
    return spikes_per_bin, bin_centers
