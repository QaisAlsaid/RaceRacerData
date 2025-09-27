import os
import shutil
import pandas as pd

train_dir = "train"
val_dir = "val"
train_csv = "train.csv"
val_csv = "val.csv"
merged_csv = "train_merged.csv"


train_df = pd.read_csv(train_csv)
val_df = pd.read_csv(val_csv)

train_max = train_df["file"].apply(
    lambda x: int(os.path.splitext(os.path.basename(x))[0])
).max()

old_val_files = val_df["file"].copy()
val_df["file"] = val_df["file"].apply(
    lambda x: f"train/{int(os.path.splitext(os.path.basename(x))[0]) + train_max}.jpg"
)

merged_df = pd.concat([train_df, val_df], ignore_index=True)
merged_df.to_csv(merged_csv, index=False)

for old, new in zip(old_val_files, val_df["file"]):
    old_path = os.path.join(val_dir, os.path.basename(old))
    new_path = os.path.join(train_dir, os.path.basename(new))
    shutil.move(old_path, new_path)

print(f"merged csv saved as {merged_csv}")
print(f"moved {len(val_df)} images to {train_dir}")

