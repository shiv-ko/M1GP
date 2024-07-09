import matwavlib as mw
import os
import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display
import soundfile as sf
from scipy import signal
 
def wavminmax():
        
    # ディレクトリパスと出力先ディレクトリを指定
    directory = r"C:\Users\kouki\projects\m1gp\piezo\PIEZO\M1GPmodule\sounds\taken-sound"
    output_directory = r"C:\Users\kouki\projects\m1gp\piezo\PIEZO\M1GPmodule\sounds\minmaxed"
    data_norm = librosa.util.normalize

    # ディレクトリ内のすべての.wavファイルを処理
    for filename in os.listdir(directory):
        if filename.endswith(".wav"):
            
            infilepath = directory + "\\" + filename
            outfilepath = output_directory + "\\" + filename
            # y, fs = mw.wavread(infilepath)
            # mw.wavwrite(outfilepath, y, fs)
            # print("input Datatype:", y.dtype)
            waveform, sample_rate = librosa.load(infilepath, sr=None)

            # 正規化
            normalized_waveform = librosa.util.normalize(waveform)


        
            # 正規化されたwavファイルの出力
            sf.write(outfilepath, normalized_waveform, sample_rate)

# waveform, sample_rate = librosa.load("C:\\Users\\kouki\\FPGA\\myenv\\PIEZO\\M1GPmodule\\sounds\\sample.wav", sr=None)

# # 正規化
# normalized_waveform = librosa.util.normalize(waveform)

# # 正規化されたwavファイルの出力
# sf.write("C:\\Users\\kouki\\FPGA\\myenv\\PIEZO\\M1GPmodule\\sounds\\sample-norm.wav", normalized_waveform, sample_rate)


wavminmax()