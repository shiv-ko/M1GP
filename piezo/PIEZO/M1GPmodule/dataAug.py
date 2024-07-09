import os
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
from scipy.ndimage import zoom
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='scipy')

# データ拡張用の関数
def add_white_noise(image, rate=0.1):
    noise = np.random.randn(*image.shape) * rate
    return image + noise

def shift_image(image, rate=0.1):
    return np.roll(image, int(image.shape[0] * rate), axis=0)

def stretch_image(image, rate=1.1):
    return zoom(image, (rate, 1, 1))

# 画像を読み込み、拡張して保存する関数
def augment_image(image_path, output_dir, filename):
    image = load_img(image_path)
    image = img_to_array(image)
    
    # オリジナルの保存
    original_output_path = os.path.join(output_dir, f"{filename}_original.png")
    array_to_img(image).save(original_output_path)

    # ホワイトノイズ追加
    augmented_image = add_white_noise(image)
    noise_output_path = os.path.join(output_dir, f"{filename}_noise.png")
    array_to_img(augmented_image).save(noise_output_path)

    # 画像シフト
    augmented_image = shift_image(image)
    shift_output_path = os.path.join(output_dir, f"{filename}_shift.png")
    array_to_img(augmented_image).save(shift_output_path)

    # 画像伸長
    augmented_image = stretch_image(image)
    stretch_output_path = os.path.join(output_dir, f"{filename}_stretch.png")
    array_to_img(augmented_image).save(stretch_output_path)

# メインの処理
def main():
    root_directory = r"C:\Users\kouki\projects\m1gp\piezo\PIEZO\M1GPmodule\images\annotated"
    
    for label_dir in os.listdir(root_directory):
        label_path = os.path.join(root_directory, label_dir)
        if not os.path.isdir(label_path):
            continue
        
        output_directory = label_path  # 拡張後の画像も同じフォルダに保存する場合

        for filename in os.listdir(label_path):
            if filename.endswith(".png"):
                file_path = os.path.join(label_path, filename)
                augment_image(file_path, output_directory, os.path.splitext(filename)[0])

# 実行
if __name__ == '__main__':
    main()
