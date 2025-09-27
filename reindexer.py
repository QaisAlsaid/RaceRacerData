import os
import shutil

train_dir = "train"
val_dir = "val"

train_files = [f for f in os.listdir(train_dir) if f.endswith(".jpg")]
train_numbers = [int(os.path.splitext(f)[0]) for f in train_files]
max_train_num = max(train_numbers) if train_numbers else 0

val_files = [f for f in os.listdir(val_dir) if f.endswith(".jpg")]
for i, f in enumerate(val_files, start=1):
    old_path = os.path.join(val_dir, f)
    new_num = max_train_num + i
    new_name = f"{new_num}.jpg"
    new_path = os.path.join(train_dir, new_name)

    shutil.move(old_path, new_path)

print(f"moved {len(val_files)} images to 'train/', numbering continues from {max_train_num+1}")

