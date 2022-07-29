import pandas as pd
from pydub import AudioSegment
import os
from scipy.io import wavfile
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_path', required=True, default='data')
    args = parser.parse_args()
    data_path = args.data_path
    file_info_path = os.path.join(data_path, 'all_info.csv')
    all_info = pd.read_csv(file_info_path , dtype = str)

    grouped = all_info.groupby('file_id')
    os.makedirs('../raw_data/', exist_ok=True)
    uttr_num = {}
    for name, group in grouped:
        wav_path = os.path.join(data_path, 'wav', name + '.wav')
        audio = AudioSegment.from_wav(wav_path)
        for index, row in group.iterrows():
            t1, t2 = float(row['start_time'])*1000, float(row['end_time'])*1000
            new_audio = audio[t1:t2]
            if 'speaker_id' in row:
                speaker_id = str(int(row['speaker_id']))
            else:
                speaker_id = '0'
            if speaker_id in uttr_num.keys():
                uttr_num[speaker_id] += 1
            else:
                uttr_num[speaker_id] = 1
            path = '../raw_data/spk_' + speaker_id
            os.makedirs(path, exist_ok=True)
            new_audio.export(path + '/uttr' + str(uttr_num[speaker_id]) + '.wav', format="wav")

if __name__ == "__main__":
    main()

