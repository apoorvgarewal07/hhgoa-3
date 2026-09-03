import os
import hashlib
import json
from pathlib import Path
import numpy as np
import cv2


def get_file_sha256(filepath):
    """
    Compute hex sha256 hash of a file.
    """
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return "0x" + h.hexdigest()


def create_sample_face_image(target_path="data/input_faces/sample.jpg"):
    """
    Creates a realistic face mockup image for testing if none exists.
    """
    target = Path(target_path)
    target.parent.mkdir(parents=True, exist_ok=True)

    if target.exists():
        return str(target)

    # Generate a clean stylized portrait image with distinct facial features
    width, height = 400, 400
    img = np.full((height, width, 3), (240, 240, 245), dtype=np.uint8)

    # Face Oval
    center = (200, 200)
    axes = (110, 140)
    cv2.ellipse(img, center, axes, 0, 0, 360, (190, 215, 235), -1) # Skin tone in BGR
    cv2.ellipse(img, center, axes, 0, 0, 360, (140, 160, 180), 2)

    # Hair
    cv2.ellipse(img, (200, 120), (120, 80), 0, 180, 360, (50, 40, 35), -1)

    # Eyes
    cv2.circle(img, (155, 175), 14, (255, 255, 255), -1)
    cv2.circle(img, (245, 175), 14, (255, 255, 255), -1)
    cv2.circle(img, (155, 175), 7, (70, 50, 30), -1)
    cv2.circle(img, (245, 175), 7, (70, 50, 30), -1)
    cv2.circle(img, (157, 173), 2, (255, 255, 255), -1)
    cv2.circle(img, (247, 173), 2, (255, 255, 255), -1)

    # Eyebrows
    cv2.ellipse(img, (155, 155), (25, 8), 0, 180, 360, (40, 30, 25), 3)
    cv2.ellipse(img, (245, 155), (25, 8), 0, 180, 360, (40, 30, 25), 3)

    # Nose
    cv2.line(img, (200, 175), (195, 215), (160, 180, 200), 2)
    cv2.line(img, (195, 215), (205, 215), (160, 180, 200), 2)

    # Mouth / Smile
    cv2.ellipse(img, (200, 250), (35, 18), 0, 0, 180, (80, 80, 180), -1)
    cv2.ellipse(img, (200, 250), (35, 18), 0, 0, 180, (40, 40, 140), 2)

    # Save image
    cv2.imwrite(str(target), img)
    print(f"✓ Created test face image: {target}")
    return str(target)


def format_tx_receipt(receipt):
    """
    Format web3 transaction receipt into JSON-serializable dictionary.
    """
    return {
        "tx_hash": receipt.get("tx_hash", receipt.get("transactionHash", "")),
        "block_number": receipt.get("block_number", receipt.get("blockNumber", 0)),
        "gas_used": receipt.get("gas_used", receipt.get("gasUsed", 0)),
        "status": receipt.get("status", 1) in [1, True, "0x1", "1"]
    }
