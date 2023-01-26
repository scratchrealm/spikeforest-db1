from typing import List
import numpy as np
import figneuro.spike_sorting.views as ssv
import spikeinterface as si
import figneuro.saneslab.views as slv

def create_firing_rates_plot(*, recording: si.BaseRecording, sorting: si.BaseSorting):
    plot_items: List[ssv.RasterPlotItem] = []
    for unit_id in sorting.get_unit_ids():
        spike_times_sec = np.array(sorting.get_unit_spike_train(segment_index=0, unit_id=unit_id)) / sorting.get_sampling_frequency()
        plot_items.append(
            slv.FiringRatesPlotItem(
                unit_id=unit_id,
                spike_times_sec=spike_times_sec.astype(np.float32)
            )
        )

    view = slv.FiringRatesPlot(
        start_time_sec=0,
        end_time_sec=recording.get_num_frames(segment_index=0) / recording.get_sampling_frequency(),
        plots=plot_items
    )
    return view
