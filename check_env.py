"""Setup check. Run with: python check_env.py
Everyone must see ALL OK before writing project code."""
import platform
import re
import sys
import time
from collections import Counter
from pathlib import Path

problems = []

# 1. Python
print(f"Python {sys.version.split()[0]} on {platform.system()} {platform.machine()}")
print(f"Running from: {sys.executable}")
if sys.version_info[:2] != (3, 11):
    problems.append("Python must be 3.11")
if ".venv" not in sys.executable:
    problems.append("the .venv is not active (see README, step 3)")
if platform.system() == "Darwin" and platform.machine() != "arm64":
    problems.append("this Python runs through Rosetta; see Common problems in the README")

# 2. Packages
try:
    import cv2
    import numpy as np
    import sklearn
    print(f"opencv {cv2.__version__}, numpy {np.__version__}, scikit-learn {sklearn.__version__}")
    if cv2.__version__ != "4.10.0":
        problems.append("wrong OpenCV version, run: pip install -r requirements.txt")
except ImportError as e:
    print(f"FAIL: {e}")
    print("Run: pip install -r requirements.txt")
    sys.exit(1)

# 3. Dataset
data = Path(__file__).parent / "Data2"
if not (data / "server").is_dir() or not (data / "client").is_dir():
    print(f"FAIL: Data2 not found at {data}. Run: git pull")
    sys.exit(1)

def images(folder):
    # files end in .JPG (uppercase), so compare in lowercase
    return sorted(p for p in (data / folder).iterdir() if p.suffix.lower() == ".jpg")

server, client = images("server"), images("client")
obj_id = re.compile(r"obj(\d+)_", re.IGNORECASE)
per_object = Counter(int(obj_id.search(p.name).group(1)) for p in server)
print(f"server: {len(server)} images of {len(per_object)} objects, client: {len(client)} images")
if len(per_object) != 50 or len(client) != 50:
    problems.append("expected 50 objects in server and 50 images in client")
unusual = {k: v for k, v in sorted(per_object.items()) if v != 3}
if unusual:
    print(f"note: objects without exactly 3 server images: {unusual} (this is normal)")

# 4. SIFT on one image
sift = cv2.SIFT_create()  # the old cv2.xfeatures2d.SIFT_create() does not work
img = cv2.imread(str(server[0]), cv2.IMREAD_GRAYSCALE)
scale = 1024 / max(img.shape)
img = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
t = time.time()
keypoints, descriptors = sift.detectAndCompute(img, None)
print(f"SIFT on {server[0].name} at {img.shape[1]}x{img.shape[0]}: "
      f"{len(keypoints)} keypoints, descriptors {descriptors.shape}, {time.time() - t:.2f} s")

print()
if problems:
    for p in problems:
        print("FAIL:", p)
else:
    print("ALL OK")
