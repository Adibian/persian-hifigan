import pandas as pd
from pydub import AudioSegment
import os
from scipy.io import wavfile
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_path', required=True, default='data')
    data_path = args.data_path
    all_info = pd.read_csv(main_path + 'all_info.csv', dtype = str)
    grouped = all_info.groupby('file_id')
    os.makedirs('../raw_data/', exist_ok=True)
    uttr_num = {}
    for name, group in grouped:
        audio = AudioSegment.from_wav(main_path + 'wav/' + name + '.wav')
        for index, row in group.iterrows():
            t1, t2 = float(row['start_time'])*1000, float(row['end_time'])*1000
            new_audio = audio[t1:t2]
            speaker_id = str(int(row['speaker_id']))
            if speaker_id in uttr_num.keys():
                uttr_num[speaker_id] += 1
            else:
                uttr_num[speaker_id] = 1
            path = '../raw_data/spk_' + speaker_id
            os.makedirs(path, exist_ok=True)
            new_audio.export(path + '/uttr' + str(uttr_num[speaker_id]) + '.wav', format="wav")
            
if __name__ == "__main__":
    main()
