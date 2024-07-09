import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# PyAudioの設定
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
DEVICE_INDEX = 1  # オーディオインターフェースのインデックス

# PyAudioオブジェクトの作成
audio = pyaudio.PyAudio()

# オーディオストリームの開始
stream = audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK,
                    input_device_index=DEVICE_INDEX)

# リアルタイムプロットの設定
fig, ax = plt.subplots()
x = np.arange(0, 2 * CHUNK, 2)
line, = ax.plot(x, np.random.rand(CHUNK))
ax.set_ylim(-2**15, 2**15)

def update(frame):
    data = np.frombuffer(stream.read(CHUNK), dtype=np.int16)
    line.set_ydata(data)
    return line,

# アニメーションの設定
ani = animation.FuncAnimation(fig, update, interval=50)

plt.show()

# ストリームの停止とクローズ
stream.stop_stream()
stream.close()
audio.terminate()
