import os
import csv
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import shutil

# ディレクトリパスと出力先ディレクトリを指定

def makeimage():
        #C:\Users\kouki\projects\m1gp\piezo\PIEZO\M1GPmodule\sounds\stripped_nonminmax
    directory = r"C:\Users\kouki\projects\m1gp\piezo\PIEZO\M1GPmodule\sounds\annotated\tapped"
    output_directory = r"C:\Users\kouki\projects\m1gp\piezo\PIEZO\M1GPmodule\sounds\annotated\tapped"

    # ディレクトリ内のすべての.wavファイルを処理
    for filename in os.listdir(directory):
        if filename.endswith(".wav"):
            waveform, sample_rate = librosa.load(directory + "\\" + filename)
            feature_melspec = librosa.feature.melspectrogram(y=waveform, sr=sample_rate)
            # print(filename)
            # plt.figure(figsize=(15,5))

            # # librosa.feature.melspectrogramをそのまま可視化した場合
            # plt.subplot(1,2,1)
            # plt.title("mel spectrogram")
            # librosa.display.specshow(feature_melspec, sr=sample_rate, x_axis='time', y_axis='hz')
            # plt.colorbar()

            # # デシベルスケールに変換した場合
            # plt.subplot(1,2,2)
            # plt.title("db scale mel spectrogram")
            # feature_melspec_db = librosa.power_to_db(feature_melspec, ref=np.max)
            # librosa.display.specshow(feature_melspec_db, sr=sample_rate, x_axis='time', y_axis='hz')
            
            # plt.colorbar(format='%+2.0f dB')

            # plt.tight_layout()
            # plt.show()

            file_path = os.path.join(directory, filename)
            # 音声データを読み込み
            audio, sr = librosa.load(file_path, sr=None)
            # メルスペクトログラムを計算
            mel_spec = librosa.feature.melspectrogram(y=audio, sr=sr)
            # メルスペクトログラムをデシベルに変換
            mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)        
            # 出力先ファイルパスを作成
            output_path = os.path.join(output_directory, f"{filename}.png")
            # メルスペクトログラムを画像として保存
            plt.figure(figsize=(3, 3))
            librosa.display.specshow(mel_spec_db, sr=sr, x_axis='off', y_axis='off')
            plt.axis('off')
            plt.ylim(0,10)
            # plt.show()
            plt.savefig(output_path, bbox_inches='tight', pad_inches=0)
            plt.close()
def makeimage2():
    directory = r"C:\Users\kouki\projects\m1gp\piezo\PIEZO\M1GPmodule\sounds\stripped"
    output_directory = r"C:\Users\kouki\projects\m1gp\piezo\PIEZO\M1GPmodule\sounds\annotated"
    annotation_file = r"C:\Users\kouki\projects\m1gp\piezo\PIEZO\M1GPmodule\annotations.csv"

    # ラベル情報を読み込み
    annotations = {}
    with open(annotation_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            filename = 'sample1'+row['filename']
            label = row['label']
            annotations[filename] = label

    # ディレクトリ内のすべての.wavファイルを処理
    for filename in os.listdir(directory):
        if filename.endswith(".wav"):
            base_filename = os.path.splitext(filename)[0].split('_')[-1] + '.wav'  # example: 0.wav, 1.wav, etc.
            label = annotations.get(base_filename, "unknown")

            label_dir = os.path.join(output_directory, label)
            if not os.path.exists(label_dir):
                os.makedirs(label_dir)

            src_path = os.path.join(directory, filename)
            dst_path = os.path.join(label_dir, filename)

            shutil.move(src_path, dst_path)

makeimage()