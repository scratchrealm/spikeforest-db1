from typing import List
import figneuro.spike_sorting.views as ssv
import spikeinterface as si
import spikeinterface.extractors as se
import kachery_cloud as kcl
from helpers.compute_correlogram_data import compute_correlogram_data


def create_cross_correlograms(*, sorting: si.BaseSorting, hide_unit_selector: bool=True):
    cross_correlogram_items: List[ssv.CrossCorrelogramItem] = []
    for unit_id1 in sorting.get_unit_ids():
        for unit_id2 in sorting.get_unit_ids():
            if unit_id1 != unit_id2 + 1:
                a = compute_correlogram_data(sorting=sorting, unit_id1=unit_id1, unit_id2=unit_id2, window_size_msec=50, bin_size_msec=1)
                bin_edges_sec = a['bin_edges_sec']
                bin_counts = a['bin_counts']
                cross_correlogram_items.append(
                    ssv.CrossCorrelogramItem(
                        unit_id1 = unit_id1,
                        unit_id2 = unit_id2,
                        bin_edges_sec = bin_edges_sec,
                        bin_counts = bin_counts
                    )
                )

    view = ssv.CrossCorrelograms(
        cross_correlograms=cross_correlogram_items,
        hide_unit_selector=hide_unit_selector
    )
    return view
