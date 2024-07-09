import pyaudio  # 録音機能を使うためのライブラリ
import wave     # wavファイルを扱うためのライブラリ
import keyboard

def getmicindex():
    # オーディオデバイスの情報を取得、マイクのインデックス番号を入手する。
    iAudio = pyaudio.PyAudio()
    for x in range(0, iAudio.get_device_count()): 
        print(iAudio.get_device_info_by_index(x))

def takewavsomeseconds(rubixindex):
    RECORD_SECONDS = 10 # 録音する時間の長さ（秒）
    WAVE_OUTPUT_FILENAME = r"C:\Users\kouki\projects\m1gp\piezo\PIEZO\M1GPmodule\sounds\taken-sound\sample.wav" # 音声を保存するファイル名
    iDeviceIndex = rubixindex # 録音デバイスのインデックス番号
    # 基本情報の設定
    FORMAT = pyaudio.paInt16 # 音声のフォーマット
    CHANNELS = 1             # モノラル
    RATE = 44100             # サンプルレート
    CHUNK = int(RATE * 0.2)  # データ点数（0.2秒区切り）
    audio = pyaudio.PyAudio() # pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS,
            rate=RATE, input=True,
            input_device_index = iDeviceIndex, # 録音デバイスのインデックス番号
            frames_per_buffer=CHUNK)
    #--------------録音開始---------------
    print("recording...")
    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
        print(f"Recording: {i * 0.2:.1f} seconds")
    print("finished recording")
    #--------------録音終了---------------
    stream.stop_stream()
    stream.close()
    audio.terminate()
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

def takewavroop(rubixindex):
    print("10秒間 q を押すとストップ")
    while(True):
        if keyboard.is_pressed("q"):
            break
        takewavsomeseconds(rubixindex)


print(getmicindex())

takewavsomeseconds(getmicindex())