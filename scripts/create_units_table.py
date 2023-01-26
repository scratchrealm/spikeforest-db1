from typing import List
import figneuro.spike_sorting.views as ssv
import spikeinterface as si


def create_units_table(*, recording: si.BaseRecording, sorting: si.BaseSorting):
    columns: List[ssv.UnitsTableColumn] = [
        ssv.UnitsTableColumn(
            key='unitId',
            label='Unit',
            dtype='int'
        ),
        ssv.UnitsTableColumn(
            key='firingRateHz',
            label='FR (Hz)',
            dtype='float'
        )
    ]
    rows: List[ssv.UnitsTableRow] = []
    for unit_id in sorting.get_unit_ids():
        spike_train = sorting.get_unit_spike_train(unit_id=unit_id)
        fr = len(spike_train) / (recording.get_num_frames() / recording.get_sampling_frequency())
        rows.append(
            ssv.UnitsTableRow(
                unit_id=unit_id,
                values={
                    'unitId': unit_id,
                    'firingRateHz': round(fr, 2)
                }
            )
        )
    view = ssv.UnitsTable(
        columns=columns,
        rows=rows
    )
    return view