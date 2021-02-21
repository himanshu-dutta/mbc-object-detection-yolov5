import os
import random
import shutil


def generate_datset(root_dir, target_dir, val_pct=0.2):
    """
    This function takes a folder with subfolders for different labels,
    and samples the data into train and val splits, with the label as prefix of each image.
    Target directory structure:
    data/
        |
        |_train/
        |
        |_val/
    """
    labels = os.listdir(root_dir)

    if not os.path.exists(target_dir):
        os.mkdir(target_dir)

    to_dir = os.path.join(target_dir, "images")
    if not os.path.exists(to_dir):
        os.mkdir(to_dir)

    to_dir_train = os.path.join(to_dir, "train")
    to_dir_val = os.path.join(to_dir, "val")
    if not os.path.exists(to_dir_train):
        os.mkdir(to_dir_train)
    if not os.path.exists(to_dir_val):
        os.mkdir(to_dir_val)

    print("Labels: ", labels)
    for label in labels:
        label_dir = os.path.join(root_dir, label)

        images = [
            img
            for img in os.listdir(label_dir)
            if img.endswith(".png") or img.endswith(".jpg") or img.endswith(".jpeg")
        ]
        random.shuffle(images)

        val_size = int(len(images) * val_pct)
        images_val = images[:val_size]
        images_train = images[val_size:]

        for img in images_train:
            frm = os.path.join(label_dir, img)
            to = os.path.join(to_dir_train, f"{label}_" + img)
            shutil.copy(frm, to)

        for img in images_val:
            frm = os.path.join(label_dir, img)
            to = os.path.join(to_dir_val, f"{label}_" + img)
            shutil.copy(frm, to)


if __name__ == "__main__":
    generate_datset("indian-food-ingredients/top_10", "data")
