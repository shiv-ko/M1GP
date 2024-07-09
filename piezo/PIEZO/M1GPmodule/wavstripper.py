import wave
import struct
import math
import os
import numpy as np

def makewavstrip():
        
    f_names = [r"C:\Users\kouki\projects\m1gp\piezo\PIEZO\M1GPmodule\sounds\minmaxed\sample1",
               r"C:\Users\kouki\projects\m1gp\piezo\PIEZO\M1GPmodule\sounds\minmaxed\sample2",
               r"C:\Users\kouki\projects\m1gp\piezo\PIEZO\M1GPmodule\sounds\minmaxed\sample3",
               r"C:\Users\kouki\projects\m1gp\piezo\PIEZO\M1GPmodule\sounds\minmaxed\sample4",
               r"C:\Users\kouki\projects\m1gp\piezo\PIEZO\M1GPmodule\sounds\minmaxed\sample5",
               r"C:\Users\kouki\projects\m1gp\piezo\PIEZO\M1GPmodule\sounds\minmaxed\sample6",
               r"C:\Users\kouki\projects\m1gp\piezo\PIEZO\M1GPmodule\sounds\minmaxed\sample7",
               r"C:\Users\kouki\projects\m1gp\piezo\PIEZO\M1GPmodule\sounds\minmaxed\sample8"
               ]
    
    # 切り取り時間[sec]
    cut_time = 1
    
    # 保存するフォルダの作成
    output_folder = r"C:\Users\kouki\projects\m1gp\piezo\PIEZO\M1GPmodule\sounds\stripped"
    
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)
    
    def wav_cut(filename, time): 
        # ファイルを読み出し
        wavf = filename + '.wav'
        wr = wave.open(wavf, 'r')
    
        # waveファイルが持つ性質を取得
        ch = wr.getnchannels()
        width = wr.getsampwidth()
        fr = wr.getframerate()
        fn = wr.getnframes()
        total_time = 1.0 * fn / fr
        integer = math.floor(total_time)  # 小数点以下切り捨て
        t = int(time)  # 秒数[sec]
        frames = int(ch * fr * t)
        num_cut = int(integer // t)
    
        # waveの実データを取得し、数値化
        data = wr.readframes(wr.getnframes())
        wr.close()
        X = np.frombuffer(data, dtype=np.int16)
    
        base_name = os.path.basename(filename)
        
        for i in range(num_cut):
            outf = os.path.join(output_folder, f"{base_name}_{str(i).zfill(len(str(num_cut)))}.wav")
            start_cut = i * frames
            end_cut = i * frames + frames
            Y = X[start_cut:end_cut]
            outd = struct.pack("h" * len(Y), *Y)
    
            # 書き出し
            ww = wave.open(outf, 'w')
            ww.setnchannels(ch)
            ww.setsampwidth(width)
            ww.setframerate(fr)
            ww.writeframes(outd)
            ww.close()
    
    for f_name in f_names:
        wav_cut(f_name, cut_time)

makewavstrip()
