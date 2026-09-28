"""Section 2: SIFT feature extraction.

Run:    python extract.py

Output: features/server.npz and features/client.npz
"""

import re
import time
from pathlib import Path

import cv2
import numpy as np

ROOT = Path(__file__).parent
DATA = ROOT / "Data2"
OUT = ROOT / "features"

MAX_SIDE = 1024  # downscale so each image gives a few thousand features, see README
OBJ_ID = re.compile(r"obj(\d+)_", re.IGNORECASE)


def list_images(split):
    """All .JPG files in Data2/<split>, sorted by object id, then name."""
    files = [p for p in (DATA / split).iterdir() if p.suffix.lower() == ".jpg"]
    return sorted(files, key=lambda p: (object_id(p), p.name))


def object_id(path):
    return int(OBJ_ID.search(path.name).group(1))


def load_gray(path):
    img = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
    scale = MAX_SIDE / max(img.shape)
    if scale < 1:
        img = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
    return img


def sift_features(img, sift):
    keypoints, desc = sift.detectAndCompute(img, None)
    if desc is None:
        return keypoints, np.zeros((0, 128), np.uint8)
    return keypoints, desc.astype(np.uint8)


def extract(split):
    sift = cv2.SIFT_create()  # default parameters
    images = list_images(split)
    all_desc, all_obj, all_img = [], [], []
    t = time.time()
    for i, path in enumerate(images):
        _, desc = sift_features(load_gray(path), sift)
        all_desc.append(desc)
        all_obj.append(np.full(len(desc), object_id(path), np.int16))
        all_img.append(np.full(len(desc), i, np.int16))
        print(f"\r{split}: {i + 1}/{len(images)} {path.name:<14} {len(desc):5d} features", end="")
    print(f"  ({time.time() - t:.0f} s)")

    OUT.mkdir(exist_ok=True)
    np.savez(
        OUT / f"{split}.npz",
        desc=np.concatenate(all_desc),
        obj=np.concatenate(all_obj),
        img=np.concatenate(all_img),         # index into image_names
        image_names=np.array([p.name for p in images]),
    )
    return load_features(split)


def load_features(split):
    with np.load(OUT / f"{split}.npz") as f:
        return {k: f[k] for k in f.files}


def summary(split, feats):

    per_image = np.bincount(feats["img"])
    ids, per_object = np.unique(feats["obj"], return_counts=True)
    print(f"{split}: {len(feats['image_names'])} images, {len(ids)} objects, "
          f"{len(feats['desc'])} features in total")
    print(f"  per image : mean {per_image.mean():.0f}, min {per_image.min()}, max {per_image.max()}")
    print(f"  per object: mean {per_object.mean():.0f}, min {per_object.min()}, max {per_object.max()}")


if __name__ == "__main__":
    for split in ("server", "client"):
        summary(split, extract(split))
