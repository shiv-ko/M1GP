import detect_func
import threading
import keyboard
from keras.models import load_model
import os
import shutil
import json

model = load_model(r'C:\Users\kouki\projects\m1gp\piezo\PIEZO\M1GPmodule\vib_cnn_model2.h5')
Rubix44index = 1  # Rubix44のサウンドインデックスを指定

recording_complete = threading.Event()

def clean_directory(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)  # ディレクトリをいったん削除
    os.mkdir(directory)  # ディレクトリ復活・中身を綺麗に

def takesound():
    global recording_complete
    detect_func.takewavsomeseconds(Rubix44index)  # Rubix44 10秒録音テスト
    recording_complete.set()  # 録音が完了したことを通知




def predictnotice():
    global recording_complete
    recording_complete.wait()  # 録音が完了するまで待機
    recording_complete.clear()  # フラグをクリア

    # work_directory = r"C:\Users\kouki\projects\m1gp\piezo\PIEZO\M1GPmodule\4detect\wav\stripped"
    # clean_directory(work_directory)
    # detect_func.makewavstrip()  # 録音した10秒のデータを1秒ごとに切り取る
    
    work_directory = r"C:\Users\kouki\projects\m1gp\piezo\PIEZO\M1GPmodule\4detect\wav\minmaxed"
    clean_directory(work_directory)
    detect_func.wavminmax()  # 録音した音声を正規化
    
    work_directory = r"C:\Users\kouki\projects\m1gp\piezo\PIEZO\M1GPmodule\4detect\img"
    clean_directory(work_directory)
    detect_func.makeimage()  # 正規化した音声を画像化

    image_path = os.path.join(work_directory, "a.wav.png")
    isTapped = detect_func.detectVib(model, image_path)
    
    print(isTapped)

while True:
    if keyboard.is_pressed("q"):
        break
    thread1 = threading.Thread(target=takesound)
    thread2 = threading.Thread(target=predictnotice)
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()

print("システム終了")
#cd .\piezo\PIEZO\M1GPmodule\