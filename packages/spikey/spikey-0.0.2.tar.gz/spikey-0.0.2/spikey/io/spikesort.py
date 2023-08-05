import numpy as np
import pandas as pd


def ks_phy_load(
    spike_time_file,
    spike_clusters_file,
    cluster_groups_file,
    spike_times_header="spike_times",
    spike_clusters_header="spike_clusters",
):
    """
    Load the output of a kilosort2/phy spike sorting pipeline
    :param spike_time_file: npy file of spike timings
    :param spike_clusters_file: npy file of spike clusters
    :param cluster_groups_file: csv/tsv file of cluster group labels
    (e.g. "good")
    :param spike_times_header: Label for the resulting dataframe,
    default: "spike_times"
    :param spike_clusters_header: Label for the resulting dataframe,
    default: "spike_clusters"
    :return:
        - spike_times: Dataframe of spike times (with associated cluster)
        - cluster_groups: Dataframe of spike cluster labels (e.g. "good")
    """
    spike_time_array = np.load(spike_time_file)
    spike_clusters = np.load(spike_clusters_file)
    cluster_groups = pd.read_csv(cluster_groups_file, delim_whitespace=True)
    spike_times = pd.DataFrame()
    spike_times[spike_times_header] = np.ravel(spike_time_array)
    spike_times[spike_clusters_header] = spike_clusters
    return spike_times, cluster_groups
