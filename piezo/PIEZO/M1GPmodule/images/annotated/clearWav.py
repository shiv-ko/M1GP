import os

def delete_wav_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".wav"):
            file_path = os.path.join(directory, filename)
            try:
                os.remove(file_path)
                print(f"Deleted {file_path}")
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")

# 指定するディレクトリを入力してください
directory = r"C:\Users\kouki\projects\m1gp\piezo\PIEZO\M1GPmodule\sounds\annotated\none"

delete_wav_files(directory)
