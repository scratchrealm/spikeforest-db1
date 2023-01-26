import os
import spikeforest as sf
import yaml


def main():
    os.makedirs('studies', exist_ok=True)
    X = sf.load_spikeforest_recordings()
    for R in X:
        path_study = f'studies/{R.study_name}'
        path_recording_yaml = f'{path_study}/recordings/{R.recording_name}.yaml'
        os.makedirs(path_study, exist_ok=True)
        os.makedirs(os.path.dirname(path_recording_yaml), exist_ok=True)
        with open(path_recording_yaml, 'w') as f:
            yaml.safe_dump({'type': 'recording', **R._recording_record}, f, sort_keys=False)

if __name__ == '__main__':
    main()