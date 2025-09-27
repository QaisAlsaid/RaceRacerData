import os
import shutil
import pandas as pd

train_dir = "train"
val_dir = "val"
output_dir = "images"

train_csv = "train.csv"
val_csv = "val.csv"
merged_csv = "images.csv"
merged_json = "images.json"

os.makedirs(output_dir, exist_ok=True)

train_df = pd.read_csv(train_csv)
val_df = pd.read_csv(val_csv)

train_max = train_df["file"].apply(
    lambda x: int(os.path.splitext(os.path.basename(x))[0])
).max()

old_val_files = val_df["file"].copy()

val_df["file"] = val_df["file"].apply(
    lambda x: f"images/{int(os.path.splitext(os.path.basename(x))[0]) + train_max}.jpg"
)

train_df["file"] = train_df["file"].apply(
    lambda x: f"images/{os.path.basename(x)}"
)

merged_df = pd.concat([train_df, val_df], ignore_index=True)
merged_df.to_csv(merged_csv, index=False)

for f in train_df["file"]:
    old_path = os.path.join(train_dir, os.path.basename(f))
    new_path = os.path.join(output_dir, os.path.basename(f))
    if os.path.exists(old_path):
        shutil.move(old_path, new_path)

for old, new in zip(old_val_files, val_df["file"]):
    old_path = os.path.join(val_dir, os.path.basename(old))
    new_path = os.path.join(output_dir, os.path.basename(new))
    if os.path.exists(old_path):
        shutil.move(old_path, new_path)

if merged_df["service_test"].dtype == object:
    merged_df["service_test"] = merged_df["service_test"].map(
        lambda x: True if str(x).lower() == "true" else False
    )

merged_df.to_json(merged_json, orient="records", indent=2, force_ascii=False)

print(f"merged csv saved as {merged_csv}")
print(f"merged json saved as {merged_json}")
print(f"all images moved into {output_dir}/")

