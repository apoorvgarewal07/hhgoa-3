import os
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.face_detection.detector import FaceDetector
from src.utils.helpers import create_sample_face_image


def test_face_detection():
    detector = FaceDetector()

    # Ensure test image exists
    test_image = "data/input_faces/test.jpg"
    if not os.path.exists(test_image):
        create_sample_face_image(test_image)

    # Detect faces
    image, locations = detector.detect_faces(test_image)
    assert locations is not None, "No faces detected"
    assert len(locations) > 0, "Location list is empty"

    # Encode faces
    encodings = detector.encode_faces(image, locations)
    assert len(encodings) > 0, "No encodings generated"

    # Primary encoding
    primary = detector.get_primary_encoding()
    assert primary is not None, "No primary encoding"
    assert len(primary) == 128, f"Expected 128 dimensions, got {len(primary)}"

    # Save encoding
    saved_path = detector.save_encoding(primary, "test_face_encoding.json")
    assert os.path.exists(saved_path), "Saved encoding file does not exist"

    # Test comparison
    is_match, dist = detector.compare_faces(primary, primary)
    assert is_match is True, "Self comparison should match"
    assert dist == 0.0 or dist < 1e-5, f"Self distance should be ~0, got {dist}"

    print("✓ All face detection tests passed!")


if __name__ == "__main__":
    test_face_detection()
