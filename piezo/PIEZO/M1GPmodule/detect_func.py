import pyaudio  # 録音機能を使うためのライブラリ
import wave     # wavファイルを扱うためのライブラリ
import keyboard
import wave
import struct
import math
import os
import json
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import librosa
import librosa.display
import soundfile as sf
from scipy import signal
from tensorflow.keras.preprocessing import image
from keras.models import load_model
from keras.applications.vgg16 import preprocess_input
from PIL import Image

def makewavstrip():
    f_names = r"C:\Users\kouki\projects\m1gp\piezo\PIEZO\M1GPmodule\4detect\wav\raw\a"  # 使用するファイル名をリストで指定
    cut_time = 1
    output_folder = r"C:\Users\kouki\projects\m1gp\piezo\PIEZO\M1GPmodule\4detect\wav\stripped"
    
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)
    
    def wav_cut(filename, time): 
        wavf = filename + '.wav'
        wr = wave.open(wavf, 'r')
        ch = wr.getnchannels()
        width = wr.getsampwidth()
        fr = wr.getframerate()
        fn = wr.getnframes()
        total_time = 1.0 * fn / fr
        integer = math.floor(total_time)
        t = int(time)
        frames = int(ch * fr * t)
        num_cut = int(integer // t)
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
            ww = wave.open(outf, 'w')
            ww.setnchannels(ch)
            ww.setsampwidth(width)
            ww.setframerate(fr)
            ww.writeframes(outd)
            ww.close()
    
    for f_name in f_names:
        wav_cut(f_name, cut_time)


def wavminmax():
    directory = r"C:\Users\kouki\projects\m1gp\piezo\PIEZO\M1GPmodule\4detect\wav\raw"
    output_directory = r"C:\Users\kouki\projects\m1gp\piezo\PIEZO\M1GPmodule\4detect\wav\minmaxed"
    target_filename = "a.wav"  # 処理する特定のファイル名

    if not os.path.exists(output_directory):
        os.mkdir(output_directory)

    infilepath = os.path.join(directory, target_filename)
    outfilepath = os.path.join(output_directory, target_filename)
    if os.path.exists(infilepath):
        waveform, sample_rate = librosa.load(infilepath, sr=None)
        normalized_waveform = librosa.util.normalize(waveform)
        sf.write(outfilepath, normalized_waveform, sample_rate)
        print(f"Processed {target_filename}")
    else:
        print(f"{target_filename} not found in {directory}")

def takewavsomeseconds(rubixindex):
    RECORD_SECONDS =0.2
    WAVE_OUTPUT_FILENAME = r"C:\Users\kouki\projects\m1gp\piezo\PIEZO\M1GPmodule\4detect\wav\raw\a.wav"
    iDeviceIndex = rubixindex
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = int(RATE * RECORD_SECONDS)
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        input_device_index=iDeviceIndex,
                        frames_per_buffer=CHUNK)
    print("recording...")
    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
        print(f"Recording: {i * 0.2:.1f} seconds")
    print("finished recording")
    stream.stop_stream()
    stream.close()
    audio.terminate()
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

# Matplotlibのバックエンドを変更
matplotlib.use('Agg')

def makeimage():
    directory = r"C:\Users\kouki\projects\m1gp\piezo\PIEZO\M1GPmodule\4detect\wav\minmaxed"
    output_directory = r"C:\Users\kouki\projects\m1gp\piezo\PIEZO\M1GPmodule\4detect\img"
    target_filename = "a.wav"  # 処理する特定のファイル名

    if not os.path.exists(output_directory):
        os.mkdir(output_directory)

    infilepath = os.path.join(directory, target_filename)
    if os.path.exists(infilepath):
        waveform, sample_rate = librosa.load(infilepath, sr=None)
        mel_spec = librosa.feature.melspectrogram(y=waveform, sr=sample_rate)
        mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)
        output_path = os.path.join(output_directory, f"{target_filename}.png")
        plt.figure(figsize=(3, 3))
        librosa.display.specshow(mel_spec_db, sr=sample_rate, x_axis='off', y_axis='off')
        plt.axis('off')
        plt.ylim(0, 10)
        plt.savefig(output_path, bbox_inches='tight', pad_inches=0)
        plt.close()
        print(f"Processed {target_filename} to image")
    else:
        print(f"{target_filename} not found in {directory}")

def save_status_to_file(status):
    file_path = r'C:\Users\kouki\projects\m1gp\public\status.json'
    data = {'status': status}
    with open(file_path, 'w') as f:
        json.dump(data, f)

def detectVib(model, image_path):
    image_resize_width = 232
    image_resize_height = 231

    img = image.load_img(image_path, target_size=(image_resize_width, image_resize_height))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    preds = model.predict(preprocess_input(x))

    shake_prob = preds[0][0]
    no_shake_prob = preds[0][1]

    print("No shake probability:", no_shake_prob)
    print("Shake probability:", shake_prob)

    if no_shake_prob > shake_prob:
        print("noshake")
        save_status_to_file("noshake")
        return 0
    else:
        print("shake")
        save_status_to_file("shake")
        return 1
