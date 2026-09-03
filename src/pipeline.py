#!/usr/bin/env python3
"""
Main Pipeline: Face Identification & Blockchain Verification
HH Goa 2026 Task 3
Connects: Face Detection & 128-D Encoding -> SerpAPI Reverse Search -> Ethereum Sepolia Blockchain Upload
"""
import os
import sys
import json
from pathlib import Path
from dotenv import load_dotenv

# Ensure project root is in sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.face_detection.detector import FaceDetector
from src.web_search.serpapi_search import SerpAPISearcher
from src.blockchain.ethereum_uploader import BlockchainUploader
from src.utils.helpers import get_file_sha256, create_sample_face_image


class FaceBlockchainPipeline:
    def __init__(self):
        load_dotenv()
        self.face_detector = FaceDetector()
        self.web_searcher = SerpAPISearcher(os.getenv("SERPAPI_API_KEY"))
        self.blockchain_uploader = BlockchainUploader(
            contract_address=os.getenv("CONTRACT_ADDRESS"),
            contract_abi=self.load_contract_abi(),
            rpc_url=os.getenv("SEPOLIA_RPC_URL"),
            private_key=os.getenv("WALLET_PRIVATE_KEY")
        )
        self.results = {}

    def load_contract_abi(self):
        """
        Load smart contract ABI from JSON file.
        """
        abi_path = Path("blockchain/contract_abi.json")
        if abi_path.exists():
            try:
                with open(abi_path, "r") as f:
                    return json.load(f)
            except Exception:
                pass
        return []

    def run(self, image_path):
        """
        Execute full end-to-end pipeline:
        1. Face Detection & 128-D Encoding
        2. Reverse Image Search (SerpAPI) & Social Media Detection
        3. Blockchain Record Upload & Verification
        """
        print("\n" + "=" * 60)
        print("🚀 FACE IDENTIFICATION & BLOCKCHAIN VERIFICATION PIPELINE")
        print("=" * 60)

        # -------------------------------------------------------------
        # STEP 1: Face Detection & Encoding
        # -------------------------------------------------------------
        print("\n📸 STEP 1: Face Detection & Encoding")
        print("-" * 40)

        if not os.path.exists(image_path):
            print(f"❌ Image not found: {image_path}")
            return None

        image, face_locations = self.face_detector.detect_faces(image_path)
        if not face_locations:
            print("❌ No faces detected in image")
            return None

        face_encodings = self.face_detector.encode_faces(image, face_locations)
        primary_encoding = self.face_detector.get_primary_encoding()

        # Save encoding to results
        self.face_detector.save_encoding(primary_encoding, "face_encoding.json")

        self.results["face_detection"] = {
            "faces_found": len(face_locations),
            "encoding_vector_size": len(primary_encoding) if primary_encoding else 0,
            "face_locations": [list(loc) for loc in face_locations],
            "status": "success"
        }

        # -------------------------------------------------------------
        # STEP 2: Reverse Image Search & Social Media Detection
        # -------------------------------------------------------------
        print("\n🔍 STEP 2: Reverse Image Search & Social Media Detection")
        print("-" * 40)

        search_results = self.web_searcher.reverse_image_search(image_path)
        if not search_results or search_results.get("total", 0) == 0:
            print("❌ No matching posts found on web/social media")
            return None

        best_match = self.web_searcher.get_best_social_post()
        if not best_match:
            print("❌ No social media posts found")
            return None

        self.results["web_search"] = {
            "total_matches": search_results.get("total", 0),
            "social_media_posts": len(search_results.get("social_posts", [])),
            "best_match": best_match,
            "person_suggestions": search_results.get("person_suggestions", {}),
            "status": "success"
        }

        print(f"\n🎯 Best Match Found:")
        print(f"  URL:    {best_match.get('url')}")
        print(f"  Source: {best_match.get('source')}")
        print(f"  Title:  {best_match.get('title')}")

        # -------------------------------------------------------------
        # STEP 3: Blockchain Upload & Verification
        # -------------------------------------------------------------
        print("\n⛓ STEP 3: Blockchain Upload & Verification")
        print("-" * 40)

        try:
            image_hash = get_file_sha256(image_path)
            post_hash = best_match.get("url", "https://instagram.com")
            social_url = best_match.get("url", "")

            tx_receipt = self.blockchain_uploader.upload_face_data(
                face_encoding=primary_encoding,
                image_hash=image_hash,
                post_hash=post_hash,
                social_url=social_url
            )

            tx_hash = tx_receipt.get("tx_hash")
            block_num = tx_receipt.get("block_number", tx_receipt.get("block"))
            gas_used = tx_receipt.get("gas_used")
            etherscan_url = tx_receipt.get("etherscan_url", f"https://sepolia.etherscan.io/tx/{tx_hash}")

            self.results["blockchain"] = {
                "tx_hash": tx_hash,
                "block_number": block_num,
                "gas_used": gas_used,
                "status": "success" if tx_receipt.get("status") else "failed",
                "etherscan_url": etherscan_url
            }

            print(f"\n✓ Blockchain Upload Complete:")
            print(f"  TX Hash:   {tx_hash}")
            print(f"  Block:     {block_num}")
            print(f"  Gas Used:  {gas_used}")
            print(f"  Etherscan: {etherscan_url}")

        except Exception as e:
            print(f"❌ Blockchain step failed: {e}")
            self.results["blockchain"] = {"status": "failed", "error": str(e)}

        # -------------------------------------------------------------
        # Save Consolidated Results
        # -------------------------------------------------------------
        self.save_pipeline_results()

        print("\n" + "=" * 60)
        print("✅ PIPELINE EXECUTION COMPLETE")
        print("=" * 60)

        return self.results

    def save_pipeline_results(self, filename="pipeline_results.json"):
        """
        Save complete pipeline results to data/results/pipeline_results.json.
        """
        out_dir = Path("data/results")
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / filename

        with open(out_path, "w") as f:
            json.dump(self.results, f, indent=2)

        print(f"\n📁 Results saved to: {out_path}")
        return str(out_path)


def main():
    if len(sys.argv) < 2:
        print("Usage: python src/pipeline.py <image_path>")
        print("Example: python src/pipeline.py data/input_faces/sample.jpg")
        sample_img = "data/input_faces/sample.jpg"
        if not os.path.exists(sample_img):
            create_sample_face_image(sample_img)
        print(f"Running pipeline on default sample image: {sample_img}\n")
        image_path = sample_img
    else:
        image_path = sys.argv[1]

    pipeline = FaceBlockchainPipeline()
    results = pipeline.run(image_path)

    if results:
        print("\n📊 Consolidated Pipeline Results:")
        print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
