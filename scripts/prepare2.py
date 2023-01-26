import os
import time
import spikeinterface as si
import figneuro.views as vv
from spikeforest.load_spikeforest_recordings.SFRecording import SFRecording
import yaml

from create_autocorrelograms import create_autocorrelograms
from create_units_table import create_units_table
from create_average_waveforms import create_average_waveforms
# from create_cross_correlograms import create_cross_correlograms
from create_spike_amplitudes import create_spike_amplitudes
from create_firing_rates_plot import create_firing_rates_plot

def main():
    for study_name in os.listdir('studies'):
        for fname in os.listdir(f'studies/{study_name}/recordings'):
            p = f'studies/{study_name}/recordings/{fname}'
            with open(p, 'r') as f:
                recording_record = yaml.safe_load(f)
            R: SFRecording = SFRecording(recording_record)
            label = f'{R.study_name}/{R.recording_name}'
            print(label)

            path_figurl_yaml = f'studies/{study_name}/recording_figurls/{R.recording_name}.yaml'
            if not os.path.exists(path_figurl_yaml):
                os.makedirs(os.path.dirname(path_figurl_yaml), exist_ok=True)
                recording: si.BaseRecording = R.get_recording_extractor()
                sorting_true: si.BaseSorting = R.get_sorting_true_extractor()
                url = create_recording_figurl(recording=recording, sorting=sorting_true, label=label)
                print(url)
                with open(path_figurl_yaml, 'w') as f:
                    yaml.safe_dump({
                        'type': 'recording_figurl',
                        'studyName': R.study_name,
                        'recordingName': R.recording_name,
                        'url': url,
                        'timestampCreated': time.time()
                    }, f)

def create_recording_figurl(*, recording: si.BaseRecording, sorting: si.BaseSorting, label: str):
    v_u = create_units_table(recording=recording, sorting=sorting)
    v_ac = create_autocorrelograms(sorting=sorting)
    v_aw = create_average_waveforms(recording=recording, sorting=sorting)
    # v_cc = create_cross_correlograms(sorting=sorting)
    v_sa = create_spike_amplitudes(recording=recording, sorting=sorting)
    v_fr = create_firing_rates_plot(recording=recording, sorting=sorting)

    B = vv.Box(
        direction='vertical',
        items=[
            vv.LayoutItem(v_aw, stretch=1.5),
            vv.LayoutItem(v_ac, stretch=1)
        ]
    )
    C = vv.Box(
        direction='vertical',
        items=[
            vv.LayoutItem(v_sa, stretch=1.5),
            vv.LayoutItem(v_fr, stretch=1)
        ]
    )

    view = vv.Box(
        direction='horizontal',
        items=[
            vv.LayoutItem(
                v_u,
                max_size=200
            ),
            vv.LayoutItem(
                B,
                stretch=1
            ),
            vv.LayoutItem(
                C,
                stretch=2
            )
        ]
    )
    return view.url(label=label)

if __name__ == '__main__':
    main()