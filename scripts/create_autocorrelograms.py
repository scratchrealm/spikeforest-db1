from typing import List
import spikeinterface as si
import figneuro.spike_sorting.views as ssv
from helpers.compute_correlogram_data import compute_correlogram_data


def create_autocorrelograms(*, sorting: si.BaseSorting, height=400):
    autocorrelogram_items: List[ssv.AutocorrelogramItem] = []
    for unit_id in sorting.get_unit_ids():
        a = compute_correlogram_data(sorting=sorting, unit_id1=unit_id, unit_id2=None, window_size_msec=50, bin_size_msec=1)
        bin_edges_sec = a['bin_edges_sec']
        bin_counts = a['bin_counts']
        autocorrelogram_items.append(
            ssv.AutocorrelogramItem(
                unit_id=unit_id,
                bin_edges_sec=bin_edges_sec,
                bin_counts=bin_counts
            )
        )
    view = ssv.Autocorrelograms(
        autocorrelograms=autocorrelogram_items,
        height=height
    )
    return view