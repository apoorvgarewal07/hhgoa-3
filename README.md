# Face Identification & Blockchain Verification Pipeline

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Ethereum Sepolia](https://img.shields.io/badge/Ethereum-Sepolia%20Testnet-627EEA.svg)](https://sepolia.etherscan.io)
[![SerpAPI](https://img.shields.io/badge/SerpAPI-Google%20Reverse%20Image-green.svg)](https://serpapi.com)

**HH Goa 2026 Task 3: End-to-End Face Identification & Blockchain Verification Pipeline**

---

## 🎯 Overview
This project implements an autonomous end-to-end pipeline that:
1. **Face Detection & 128-D Encoding**: Detects human faces in an input image and extracts standardized 128-dimensional facial embedding vectors.
2. **Reverse Image Web Search**: Leverages SerpAPI Google Reverse Image engine to locate where the face appears online across social media networks (Instagram, Twitter/X, LinkedIn, Facebook, etc.) and extracts knowledge panel insights.
3. **Blockchain Record & On-Chain Verification**: Computes SHA-256 cryptographic hashes of the face vector, original image, and discovered social media post, and uploads the immutable record to an Ethereum smart contract on the Sepolia testnet.

---

## 🏗 Architecture Workflow

```
[ Input Face Image ]
         │
         ▼
[ Step 1: Face Detection & 128-D Vector Encoding ] ──► Saves: data/results/face_encoding.json
         │
         ▼
[ Step 2: SerpAPI Reverse Image Search ] ────────────► Saves: data/results/search_results.json
         │ (Filters Instagram, X, LinkedIn, FB)
         ▼
[ Step 3: Ethereum Smart Contract Upload ] ──────────► Saves: data/results/blockchain_receipt.json
         │ (Stores cryptographic digests on-chain)
         ▼
[ On-Chain Verification & Etherscan Receipt ] ───────► Saves: data/results/pipeline_results.json
```

---

## 🛠 Tech Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Face Detection** | `OpenCV` / `face_recognition` | Accurate facial landmark and bounding box detection |
| **Face Encoding** | 128-D Facial Vector Extraction | Standard 128-dimensional embedding representations |
| **Web Reverse Search** | `SerpAPI` Google Reverse Image | Reverse image indexing across social media & web |
| **Blockchain** | Ethereum Sepolia Testnet | Decentralized public test network |
| **Smart Contract** | Solidity (`FaceDataRegistry.sol`) | Immutable registry with event logging |
| **Web3 Connection** | `web3.py` (v6.x / v8.x) | Transaction signing, broadcasting & ABI interaction |
| **Testing** | `pytest` | Complete unit and integration test suite |

---

## 🚀 Quick Start

### 1. Installation
```bash
# Clone repository
git clone <repo-url>
cd hh-goa-task3-face-blockchain

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
cp .env.example .env
```
Edit `.env` with your API keys (see [docs/API_KEYS.md](docs/API_KEYS.md) for details):
```ini
SERPAPI_API_KEY=your_serpapi_key_here
INFURA_API_KEY=your_infura_key_here
SEPOLIA_RPC_URL=https://sepolia.infura.io/v3/your_infura_key_here
CONTRACT_ADDRESS=0xYourDeployedContractAddress
WALLET_ADDRESS=0xYourWalletAddress
WALLET_PRIVATE_KEY=your_private_key_here
```

### 3. Run the Pipeline
```bash
python src/pipeline.py data/input_faces/sample.jpg
```

---

## 📂 Project Structure

```
hh-goa-task3-face-blockchain/
├── src/
│   ├── __init__.py
│   ├── pipeline.py                 # Main CLI Orchestrator (RUN THIS)
│   ├── face_detection/
│   │   ├── __init__.py
│   │   └── detector.py             # Face detection & 128-D embedding module
│   ├── web_search/
│   │   ├── __init__.py
│   │   └── serpapi_search.py       # SerpAPI reverse image search module
│   ├── blockchain/
│   │   ├── __init__.py
│   │   └── ethereum_uploader.py    # web3.py smart contract interaction
│   └── utils/
│       ├── __init__.py
│       └── helpers.py              # Cryptographic hashing & sample helpers
├── blockchain/
│   ├── FaceDataRegistry.sol        # Solidity smart contract
│   └── contract_abi.json           # Smart contract ABI definition
├── data/
│   ├── input_faces/                # Input portrait photos
│   └── results/                    # Generated JSON outputs & receipts
├── tests/
│   ├── __init__.py
│   ├── test_face_detection.py      # Face detection unit tests
│   ├── test_web_search.py          # Reverse image search tests
│   └── test_full_pipeline.py       # End-to-end integration test
├── docs/
│   ├── SETUP.md                    # Setup and installation walkthrough
│   ├── API_KEYS.md                 # API key acquisition guide
│   └── BLOCKCHAIN_SETUP.md         # Smart contract deployment guide
├── .env.example                    # Sample environment template
├── requirements.txt                # Python dependencies
├── run.sh                          # Bash run script
├── run.bat                         # Windows batch run script
└── README.md
```

---

## 🧪 Testing Suite

Execute the full automated test suite using `pytest`:
```bash
pytest tests/ -v
```

All test cases validate:
- Facial detection and 128-D vector generation.
- SerpAPI reverse search responses and social media link filtering.
- Ethereum transaction signing, hashing, and blockchain receipt creation.

---

## 📊 Output Artifacts

The pipeline generates JSON reports inside `data/results/`:
- `face_encoding.json`: 128-D facial vector data.
- `search_results.json`: Online match results and social profile links.
- `blockchain_receipt.json`: Transaction hash, mined block, gas used, and Etherscan URL.
- `pipeline_results.json`: Consolidated end-to-end pipeline report.

---

## 🔗 Blockchain Verification
Transactions can be verified on the Ethereum Sepolia block explorer:
```
https://sepolia.etherscan.io/tx/{TX_HASH}
```

---

## 📝 License
This project is licensed under the MIT License.
