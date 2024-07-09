import os
import glob

def clear_image_folders(base_dir):
    # base_dir内のすべてのサブディレクトリを取得
    sub_dirs = [os.path.join(base_dir, d) for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]
    
    # 各サブディレクトリ内の画像ファイルを削除
    for sub_dir in sub_dirs:
        images = glob.glob(os.path.join(sub_dir, '*.png'))
        for image in images:
            os.remove(image)
            print(f"Deleted {image}")

# 使用例
base_directory = r"C:\Users\kouki\projects\m1gp\piezo\PIEZO\M1GPmodule\images\stripped_nonminmax"
clear_image_folders(base_directory)
