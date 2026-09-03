# HH Goa Task 3: Step-by-Step Execution Guide for Coding Agent

**This guide is structured for easy handoff to a coding agent. Follow sequentially.**

\---

## 🎯 Mission

Build a pipeline: **Face Image → Find on Social Media → Upload to Blockchain**

**Deadline:** September 7, 2026, 11:59 PM

\---

## 📋 STEP 1: Project Setup (Do First)

### 1.1

<br/>\# Create folder structure  
mkdir -p src/{face_detection,web_search,blockchain,utils}  
mkdir -p blockchain  
mkdir -p data/{input_faces,results,logs}  
mkdir -p tests  
mkdir -p docs

### 1.2 Create requirements.txt

**File:** requirements.txt

face-recognition==1.4.0  
face_recognition_models==0.4.0  
opencv-python==4.8.0.76  
Pillow==10.0.0  
requests==2.31.0  
web3==6.11.0  
serpapi==0.1.0  
python-dotenv==1.0.0  
flask==3.0.0  
pytest==7.4.0

### 1.3 Install Dependencies

pip install -r requirements.txt

### 1.4 Create .env File

**File:** .env

\# Get these from services below  
SERPAPI_API_KEY=paste_your_key_here  
INFURA_API_KEY=paste_your_key_here  
CONTRACT_ADDRESS=0x0000000000000000000000000000000000000000  
WALLET_ADDRESS=0x0000000000000000000000000000000000000000  
WALLET_PRIVATE_KEY=0x0000000000000000000000000000000000000000  
SEPOLIA_RPC_URL=<https://sepolia.infura.io/v3/PASTE_YOUR_INFURA_KEY>

### 1.5 Create .gitignore

**File:** .gitignore

.env  
\__pycache_\_/  
\*.pyc  
.pytest_cache/  
\*.egg-info/  
venv/  
.DS_Store  
.vscode/  
\*.json (optional, for private results)

### 1.6 Push to GitHub

git add .  
git commit -m "Initial project setup"  
git remote add origin <https://github.com/YOUR_USERNAME/hh-goa-task3-face-blockchain.git>  
git branch -M main  
git push -u origin main

\---

## 🔐 STEP 2: Get API Keys & Credentials (15 minutes)

### 2.1 SerpAPI Key (Web Search)

**URL:** <https://serpapi.com>

**Instructions:**

1. Click "Try for free" or "Sign up"
2. Complete signup
3. Dashboard shows API key
4. Copy key
5. Paste in \`.env\`: \`SERPAPI_API_KEY=9c42e085367cb344cd72c5e6deb453d96001c41ddeae8b92cff2e4c4ff84b231\`
6. Test: 100 free searches/month ✓

\---

### 2.2 Infura Account (Blockchain Access)

**URL:** <https://infura.io>

**Instructions:**

1. Sign up (use email)
2. Create new project → "Ethereum"
3. Go to Settings
4. Copy "Sepolia" RPC URL (looks like: \`<https://sepolia.infura.io/v3/abc123...\`>)
5. Paste in \`.env\` as \`SEPOLIA_RPC_URL= <https://sepolia.infura.io/v3/9da0131d41534fdeadf21036ec689b1c> \`
6. Also get Project ID and paste as \`INFURA_API_KEY= 9da0131d41534fdeadf21036ec689b1c\`

## 💻 STEP 3: Build Module 1 - Face Detection

### 3.1 Create Face Detector Class

**File:** src/face_detection/detector.py

import face_recognition  
import cv2  
import numpy as np  
from PIL import Image  
import json  
from pathlib import Path  
<br/>class FaceDetector:  
def \__init_\_(self):  
self.face_encodings = \[\]  
self.face_locations = \[\]  
<br/>def load_image(self, image_path):  
"""Load image file"""  
image = face_recognition.load_image_file(image_path)  
return image  
<br/>def detect_faces(self, image_path):  
"""Find faces in image"""  
image = self.load_image(image_path)  
face_locations = face_recognition.face_locations(image)  
<br/>if not face_locations:  
print("❌ No faces found")  
return None, None  
<br/>self.face_locations = face_locations  
print(f"✓ Found {len(face_locations)} face(s)")  
return image, face_locations  
<br/>def encode_faces(self, image, face_locations):  
"""Generate face encodings (vectors)"""  
face_encodings = face_recognition.face_encodings(image, face_locations)  
self.face_encodings = face_encodings  
print(f"✓ Generated {len(face_encodings)} encoding(s)")  
return face_encodings  
<br/>def get_primary_encoding(self):  
"""Get main face encoding"""  
if self.face_encodings:  
return self.face_encodings\[0\].tolist()  
return None  
<br/>def save_encoding(self, encoding, filename="face_encoding.json"):  
"""Save encoding to file"""  
Path("data/results").mkdir(parents=True, exist_ok=True)  
with open(f"data/results/{filename}", "w") as f:  
json.dump({"encoding": encoding, "vector_size": 128}, f)  
print(f"✓ Saved to {filename}")

### 3.2 Create \__init_\_.py files

**File:** src/\__init_\_.py (empty)

**File:** src/face_detection/\__init_\_.py (empty)

### 3.3 Test Face Detection

**File:** tests/test_face_detection.py

import os  
from src.face_detection.detector import FaceDetector  
<br/>def test_face_detection():  
detector = FaceDetector()  
<br/>\# Create test image path  
test_image = "data/input_faces/test.jpg"  
<br/>if not os.path.exists(test_image):  
print(f"⚠️ Add test image to {test_image}")  
return False  
<br/>\# Test detection  
image, locations = detector.detect_faces(test_image)  
if locations is None:  
print("❌ Detection failed")  
return False  
<br/>\# Test encoding  
encodings = detector.encode_faces(image, locations)  
if not encodings:  
print("❌ Encoding failed")  
return False  
<br/>print("✓ Face detection works!")  
return True  
<br/>if \__name__== "\__main_\_":  
test_face_detection()

### 3.4 Run Test

\# First, add a test image to: data/input_faces/test.jpg  
\# Then run:  
python tests/test_face_detection.py

**Expected output:**

✓ Found 1 face(s)  
✓ Generated 1 encoding(s)  
✓ Face detection works!

\---

## 🔍 STEP 4: Build Module 2 - Web Search (SerpAPI)

### 4.1 Create SerpAPI Searcher

**File:** src/web_search/serpapi_search.py

import serpapi  
import json  
from pathlib import Path  
import os  
<br/>class SerpAPISearcher:  
def \__init_\_(self, api_key):  
self.api_key = api_key  
self.results = \[\]  
<br/>def reverse_image_search(self, image_path):  
"""Search web for matching images"""  
print(f"🔍 Searching for: {image_path}")  
<br/>try:  
\# Read image and encode  
import base64  
with open(image_path, "rb") as f:  
image_b64 = base64.b64encode(f.read()).decode()  
<br/>\# SerpAPI call  
params = {  
"api_key": self.api_key,  
"engine": "google_reverse_image",  
"image": image_b64,  
"tbm": "isch"  
}  
<br/>search = serpapi.search(params)  
self.results = search  
<br/>return self.\_parse_results(search)  
<br/>except Exception as e:  
print(f"❌ Search failed: {e}")  
return None  
<br/>def \_parse_results(self, search_data):  
"""Extract relevant data"""  
results = {  
"total": 0,  
"matches": \[\],  
"social_posts": \[\]  
}  
<br/>\# Parse matches  
if "inline_images" in search_data:  
for img in search_data\["inline_images"\]\[:10\]: # Top 10  
match = {  
"url": img.get("link", ""),  
"source": img.get("source", ""),  
"title": img.get("title", ""),  
}  
results\["matches"\].append(match)  
results\["total"\] += 1  
<br/>\# Check if social media  
social_domains = \["instagram.com", "twitter.com", "facebook.com",  
"tiktok.com", "linkedin.com", "reddit.com"\]  
if any(d in match\["source"\] for d in social_domains):  
results\["social_posts"\].append(match)  
<br/>print(f"✓ Found {results\['total'\]} matches, {len(results\['social_posts'\])} from social media")  
return results  
<br/>def get_best_social_post(self):  
"""Get best social media match"""  
if not self.results or "inline_images" not in self.results:  
return None  
<br/>\# Priority: Instagram > Twitter > Facebook > Others  
for domain in \["instagram.com", "twitter.com", "facebook.com"\]:  
for img in self.results\["inline_images"\]:  
if domain in img.get("source", ""):  
return {  
"url": img.get("link", ""),  
"title": img.get("title", ""),  
"source": img.get("source", "")  
}  
<br/>\# Default to first  
if self.results.get("inline_images"):  
first = self.results\["inline_images"\]\[0\]  
return {  
"url": first.get("link", ""),  
"title": first.get("title", ""),  
"source": first.get("source", "")  
}  
<br/>return None  
<br/>def save_results(self, filename="search_results.json"):  
"""Save results"""  
Path("data/results").mkdir(parents=True, exist_ok=True)  
with open(f"data/results/{filename}", "w") as f:  
json.dump(self.results, f, indent=2)  
print(f"✓ Results saved")

### 4.2 Create \__init_\_.py

**File:** src/web_search/\__init_\_.py (empty)

### 4.3 Test Web Search

**File:** tests/test_web_search.py

import os  
from dotenv import load_dotenv  
from src.web_search.serpapi_search import SerpAPISearcher  
<br/>def test_web_search():  
load_dotenv()  
api_key = os.getenv("SERPAPI_API_KEY")  
<br/>searcher = SerpAPISearcher(api_key)  
<br/>test_image = "data/input_faces/test.jpg"  
if not os.path.exists(test_image):  
print("⚠️ Add test image first")  
return False  
<br/>results = searcher.reverse_image_search(test_image)  
<br/>if not results or results\["total"\] == 0:  
print("❌ No results found")  
return False  
<br/>best = searcher.get_best_social_post()  
if not best:  
print("❌ No social posts found")  
return False  
<br/>print(f"✓ Web search works!")  
print(f" URL: {best\['url'\]}")  
print(f" Source: {best\['source'\]}")  
<br/>return True  
<br/>if \__name__ == "\__main_\_":  
test_web_search()

### 4.4 Run Test

python tests/test_web_search.py

**Expected output:**

✓ Found X matches, Y from social media  
✓ Web search works!  
URL: https://...  
Source: instagram.com

\---

## ⛓️ STEP 5: Build Module 3 - Blockchain Upload

### 5.1 Deploy Smart Contract

**Go to:** <https://remix.ethereum.org>

**Steps:**

1. Create new file: \`FaceDataRegistry.sol\`
2. Paste this code:

// SPDX-License-Identifier: MIT  
pragma solidity ^0.8.0;  
<br/>contract FaceDataRegistry {  
<br/>struct FaceRecord {  
bytes32 faceEncoding;  
bytes32 imageHash;  
bytes32 postHash;  
string socialMediaURL;  
uint256 timestamp;  
address uploadedBy;  
}  
<br/>mapping(uint256 => FaceRecord) public records;  
uint256 public recordCount = 0;  
<br/>event FaceDataUploaded(  
uint256 indexed recordId,  
bytes32 faceEncoding,  
string socialMediaURL,  
uint256 timestamp  
);  
<br/>function uploadFaceData(  
bytes32 \_faceEncoding,  
bytes32 \_imageHash,  
bytes32 \_postHash,  
string memory \_socialMediaURL  
) public returns (uint256) {  
<br/>uint256 recordId = recordCount;  
<br/>records\[recordId\] = FaceRecord({  
faceEncoding: \_faceEncoding,  
imageHash: \_imageHash,  
postHash: \_postHash,  
socialMediaURL: \_socialMediaURL,  
timestamp: block.timestamp,  
uploadedBy: msg.sender  
});  
<br/>emit FaceDataUploaded(  
recordId,  
\_faceEncoding,  
\_socialMediaURL,  
block.timestamp  
);  
<br/>recordCount++;  
return recordId;  
}  
<br/>function verifyFaceData(uint256 \_recordId) public view returns (bool) {  
require(\_recordId < recordCount, "Record does not exist");  
return records\[\_recordId\].faceEncoding != bytes32(0);  
}  
<br/>function getRecord(uint256 \_recordId) public view returns (FaceRecord memory) {  
require(\_recordId < recordCount, "Record does not exist");  
return records\[\_recordId\];  
}  
}

1. Click "Solidity Compiler" tab
2. Select version "0.8.0" or higher
3. Click "Compile"
4. Go to "Deploy & Run Transactions"
5. Select "Injected Provider - MetaMask"
6. Connect MetaMask if asked
7. Make sure MetaMask is on \*\*Sepolia testnet\*\*
8. Click "Deploy"
9. Confirm in MetaMask
10. \*\*Copy contract address\*\* from Remix output
11. Add to \`.env\`: \`CONTRACT_ADDRESS=0x...\`

### 5.2 Get Contract ABI

**In Remix:**

1. Go to Solidity Compiler
2. Click the copy icon (ABI)
3. Create file: \`blockchain/contract_abi.json\`
4. Paste the ABI as-is

### 5.3 Create Python Blockchain Module

**File:** src/blockchain/ethereum_uploader.py

from web3 import Web3  
import json  
import hashlib  
import os  
from pathlib import Path  
<br/>class BlockchainUploader:  
def \__init_\_(self, contract_address, contract_abi, rpc_url, private_key):  
"""Initialize blockchain connection"""  
self.w3 = Web3(Web3.HTTPProvider(rpc_url))  
<br/>if not self.w3.is_connected():  
print("❌ Not connected to blockchain")  
raise Exception("Blockchain connection failed")  
<br/>print(f"✓ Connected to blockchain (Chain ID: {self.w3.eth.chain_id})")  
<br/>self.contract = self.w3.eth.contract(  
address=Web3.to_checksum_address(contract_address),  
abi=contract_abi  
)  
<br/>self.account = self.w3.eth.account.from_key(private_key)  
print(f"✓ Account: {self.account.address}")  
<br/>def hash_data(self, data):  
"""Create hash of data"""  
if isinstance(data, str):  
data = data.encode()  
return "0x" + hashlib.sha256(data).hexdigest()  
<br/>def upload_face_data(self, face_encoding, image_hash, post_hash, social_url):  
"""Upload data to blockchain"""  
print(f"⛓️ Uploading to blockchain...")  
<br/>try:  
\# Convert to string and hash  
if isinstance(face_encoding, list):  
encoding_str = json.dumps(face_encoding)  
else:  
encoding_str = str(face_encoding)  
<br/>face_hash = self.hash_data(encoding_str)  
<br/>\# Build transaction  
tx = self.contract.functions.uploadFaceData(  
face_hash,  
self.hash_data(str(image_hash)),  
self.hash_data(str(post_hash)),  
social_url  
).build_transaction({  
"from": self.account.address,  
"nonce": self.w3.eth.get_transaction_count(self.account.address),  
"gas": 300000,  
"gasPrice": self.w3.eth.gas_price,  
"chainId": self.w3.eth.chain_id  
})  
<br/>\# Sign and send  
signed_tx = self.w3.eth.account.sign_transaction(tx, self.account.key)  
tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)  
print(f"✓ Transaction: {tx_hash.hex()}")  
<br/>\# Wait for confirmation  
print(f"⏳ Waiting for confirmation...")  
receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)  
<br/>print(f"✓ Confirmed in block {receipt\['blockNumber'\]}")  
<br/>return {  
"tx_hash": tx_hash.hex(),  
"block": receipt\['blockNumber'\],  
"gas_used": receipt\['gasUsed'\],  
"status": receipt\['status'\] == 1  
}  
<br/>except Exception as e:  
print(f"❌ Upload failed: {e}")  
raise  
<br/>def verify(self, record_id):  
"""Check if record exists"""  
result = self.contract.functions.verifyFaceData(record_id).call()  
return result

### 5.4 Create \__init_\_.py

**File:** src/blockchain/\__init_\_.py (empty)

\---

## 🚀 STEP 6: Build Main Pipeline

### 6.1 Create Main Pipeline

**File:** src/pipeline.py

# !/usr/bin/env python3

import os  
import sys  
import json  
from pathlib import Path  
from dotenv import load_dotenv  
<br/>from src.face_detection.detector import FaceDetector  
from src.web_search.serpapi_search import SerpAPISearcher  
from src.blockchain.ethereum_uploader import BlockchainUploader  
<br/>class FaceBlockchainPipeline:  
def \__init_\_(self):  
load_dotenv()  
<br/>self.face_detector = FaceDetector()  
self.web_searcher = SerpAPISearcher(os.getenv("SERPAPI_API_KEY"))  
<br/>\# Blockchain (optional if contract not deployed yet)  
contract_addr = os.getenv("CONTRACT_ADDRESS")  
if contract_addr and contract_addr != "0x0000000000000000000000000000000000000000":  
try:  
with open("blockchain/contract_abi.json") as f:  
abi = json.load(f)  
<br/>self.blockchain_uploader = BlockchainUploader(  
contract_address=contract_addr,  
contract_abi=abi,  
rpc_url=os.getenv("SEPOLIA_RPC_URL"),  
private_key=os.getenv("WALLET_PRIVATE_KEY")  
)  
except:  
print("⚠️ Blockchain not configured")  
self.blockchain_uploader = None  
else:  
self.blockchain_uploader = None  
<br/>self.results = {}  
<br/>def run(self, image_path):  
"""Run complete pipeline"""  
<br/>print("\\n" + "="\*60)  
print("🚀 FACE IDENTIFICATION & BLOCKCHAIN VERIFICATION")  
print("="\*60)  
<br/>\# Step 1: Face Detection  
print("\\n📸 STEP 1: Face Detection")  
print("-"\*40)  
<br/>if not os.path.exists(image_path):  
print(f"❌ Image not found: {image_path}")  
return None  
<br/>image, faces = self.face_detector.detect_faces(image_path)  
if not faces:  
print("❌ No faces detected")  
return None  
<br/>encodings = self.face_detector.encode_faces(image, faces)  
encoding = self.face_detector.get_primary_encoding()  
<br/>self.results\["face_detection"\] = {  
"faces": len(faces),  
"encoding_size": len(encoding) if encoding else 0,  
"status": "success"  
}  
<br/>\# Step 2: Web Search  
print("\\n🔍 STEP 2: Web Search")  
print("-"\*40)  
<br/>search_results = self.web_searcher.reverse_image_search(image_path)  
if not search_results or search_results\["total"\] == 0:  
print("❌ No results found")  
return None  
<br/>best_match = self.web_searcher.get_best_social_post()  
if not best_match:  
print("❌ No social posts found")  
return None  
<br/>print(f"✓ Found: {best_match\['url'\]}")  
print(f" Source: {best_match\['source'\]}")  
<br/>self.results\["web_search"\] = {  
"total_matches": search_results\["total"\],  
"social_posts": len(search_results\["social_posts"\]),  
"best_match": best_match,  
"status": "success"  
}  
<br/>\# Step 3: Blockchain Upload  
if self.blockchain_uploader:  
print("\\n⛓️ STEP 3: Blockchain Upload")  
print("-"\*40)  
<br/>try:  
receipt = self.blockchain_uploader.upload_face_data(  
face_encoding=encoding,  
image_hash=image_path,  
post_hash=best_match\["url"\],  
social_url=best_match\["url"\]  
)  
<br/>self.results\["blockchain"\] = {  
"tx_hash": receipt\["tx_hash"\],  
"block": receipt\["block"\],  
"status": "success"  
}  
<br/>print(f"\\n✓ Etherscan: <https://sepolia.etherscan.io/tx/{receipt\['tx_hash'\]}>")  
<br/>except Exception as e:  
print(f"❌ Blockchain failed: {e}")  
self.results\["blockchain"\] = {"status": "failed"}  
else:  
print("\\n⚠️ Blockchain not configured (skip)")  
<br/>\# Save results  
Path("data/results").mkdir(parents=True, exist_ok=True)  
with open("data/results/pipeline_results.json", "w") as f:  
json.dump(self.results, f, indent=2)  
<br/>print("\\n" + "="\*60)  
print("✅ PIPELINE COMPLETE")  
print("="\*60)  
<br/>return self.results  
<br/>if \__name__== "\__main_\_":  
if len(sys.argv) < 2:  
print("Usage: python src/pipeline.py &lt;image_path&gt;")  
sys.exit(1)  
<br/>pipeline = FaceBlockchainPipeline()  
results = pipeline.run(sys.argv\[1\])  
<br/>if results:  
print("\\n📊 Results:")  
print(json.dumps(results, indent=2))

### 6.2 Run Pipeline

\# Add your test image to: data/input_faces/sample.jpg  
\# Then run:  
python src/pipeline.py data/input_faces/sample.jpg

**Expected output:**

\============================================================  
🚀 FACE IDENTIFICATION & BLOCKCHAIN VERIFICATION  
\============================================================  
<br/>📸 STEP 1: Face Detection  
\----------------------------------------  
✓ Found 1 face(s)  
✓ Generated 1 encoding(s)  
<br/>🔍 STEP 2: Web Search  
\----------------------------------------  
✓ Found X matches, Y from social media  
✓ Found: <https://instagram.com/p/ABC123/>  
Source: instagram.com  
<br/>⛓️ STEP 3: Blockchain Upload  
\----------------------------------------  
✓ Transaction: 0xabc123...  
✓ Confirmed in block 5678  
<br/>✓ Etherscan: <https://sepolia.etherscan.io/tx/0xabc123>...  
<br/>\============================================================  
✅ PIPELINE COMPLETE  
\============================================================

\-

## 📝 STEP 8: GitHub & Documentation

### 8.1 Write README.md

**File:** README.md

\# Face Identification & Blockchain Verification Pipeline  
<br/>\## What It Does  
1\. Detects faces in images  
2\. Finds matching social media posts  
3\. Uploads data to blockchain  
<br/>\## Quick Start

pip install -r requirements.txt

cp .env.example .env

# Edit .env with API keys

python src/pipeline.py data/input_faces/sample.jpg

\## Technologies  
\- face_recognition (face detection)  
\- SerpAPI (web search)  
\- web3.py (blockchain)  
\- Ethereum Sepolia testnet  
<br/>\## Setup Instructions  
See \`docs/SETUP.md\`  
<br/>\## Screen Recording  
\[Link to your recording\]  
<br/>\## Blockchain Verification  
View transactions: <https://sepolia.etherscan.io>

### 8.2 Commit Everything

git add -A  
git commit -m "Complete face identification and blockchain pipeline"  
git push origin main

\--

\---

\---

## 🎉 You're Done

Good luck! 🚀