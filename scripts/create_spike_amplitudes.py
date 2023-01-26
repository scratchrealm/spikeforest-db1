import numpy as np
from typing import List
import figneuro.spike_sorting.views as ssv
import spikeinterface as si
import kachery_cloud as kcl
from create_average_waveforms import extract_snippets


def create_spike_amplitudes(*, recording: si.BaseRecording, sorting: si.BaseSorting, hide_unit_selector: bool=True):
    traces = recording.get_traces(segment_index=0)
    plot_items: List[ssv.SpikeAmplitudesItem] = []
    for unit_id in sorting.get_unit_ids():
        spike_times = np.array(sorting.get_unit_spike_train(segment_index=0, unit_id=unit_id))
        spike_times_sec = spike_times / recording.get_sampling_frequency()
        snippets = extract_snippets(traces=traces, times=spike_times, snippet_len=(5, 5))
        plot_items.append(
            ssv.SpikeAmplitudesItem(
                unit_id=unit_id,
                spike_times_sec=spike_times_sec.astype(np.float32),
                spike_amplitudes=np.max(np.abs(snippets.reshape((snippets.shape[0], snippets.shape[1] * snippets.shape[2]))), axis=1).astype(np.float32)
            )
        )

    view = ssv.SpikeAmplitudes(
        start_time_sec=0,
        end_time_sec=recording.get_num_frames(segment_index=0) / recording.get_sampling_frequency(),
        plots=plot_items,
        hide_unit_selector=hide_unit_selector
    )
    return view

if __name__ == '__main__':
    main()
