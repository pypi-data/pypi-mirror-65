def get_good(cluster_groups, group="group", identifier="good"):
    """
    Given a dataframe of spike clusters, return only those labelled as "good"

    :param cluster_groups: Dataframe of clusters and groups
    :param group: Label for the groups in "cluster_groups"
    :param identifier: String identifying the "good" group in "cluster_groups"
    :return:
    """
    cluster_groups = cluster_groups[cluster_groups[group] == identifier]
    return cluster_groups


def get_good_spikes(
    spike_times,
    cluster_groups,
    cluster_id_label="cluster_id",
    group="group",
    identifier="good",
    spike_clusters_label="spike_clusters",
):
    """
    Clean up a dataframe of spike times based on the "good" clusters in
    cluster_groups

    :param spike_times: Dataframe of spike times and clusters
    :param cluster_groups: Dataframe of clusters and groups
    :param cluster_id_label: Label for the cluster ID label in "cluster_groups"
    :param group: Label for the groups in "cluster_groups"
    :param identifier: String identifying the "good" group in "cluster_groups"
    :param spike_clusters_label: Label identifying spike clusters
    in "spike_times"
    :return: "spike_times" dataframe with only the spikes  belonging to
    clusters labelled as "good"
    """
    good_clusters = get_good(
        cluster_groups, group=group, identifier=identifier
    )
    good_cluster_list = list(good_clusters[cluster_id_label])
    spike_times = spike_times[
        spike_times[spike_clusters_label].isin(good_cluster_list)
    ]
    return spike_times
