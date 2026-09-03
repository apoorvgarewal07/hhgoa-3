import os
import sys
import json
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.pipeline import FaceBlockchainPipeline
from src.utils.helpers import create_sample_face_image


def test_full_pipeline():
    """
    Test the full end-to-end Face Identification and Blockchain Verification pipeline.
    """
    test_image = "data/input_faces/test.jpg"
    if not os.path.exists(test_image):
        create_sample_face_image(test_image)

    pipeline = FaceBlockchainPipeline()
    results = pipeline.run(test_image)

    assert results is not None, "Pipeline execution returned None"
    assert "face_detection" in results, "Face detection stage missing from output"
    assert results["face_detection"]["status"] == "success", "Face detection failed"
    assert results["face_detection"]["faces_found"] > 0, "No faces detected in test image"
    assert results["face_detection"]["encoding_vector_size"] == 128, "Encoding vector size must be 128"

    assert "web_search" in results, "Web search stage missing from output"
    assert results["web_search"]["status"] == "success", "Web search failed"
    assert results["web_search"]["best_match"] is not None, "Best match is None"

    assert "blockchain" in results, "Blockchain stage missing from output"
    assert results["blockchain"]["status"] == "success", "Blockchain upload failed"
    assert results["blockchain"]["tx_hash"].startswith("0x"), "Invalid TX hash format"

    # Verify generated output files exist
    assert os.path.exists("data/results/face_encoding.json"), "face_encoding.json not found"
    assert os.path.exists("data/results/search_results.json"), "search_results.json not found"
    assert os.path.exists("data/results/blockchain_receipt.json"), "blockchain_receipt.json not found"
    assert os.path.exists("data/results/pipeline_results.json"), "pipeline_results.json not found"

    print("\n✓ Full end-to-end pipeline test passed successfully!")


if __name__ == "__main__":
    test_full_pipeline()
