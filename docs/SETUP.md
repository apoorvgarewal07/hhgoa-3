# Comprehensive Setup & Installation Guide

## 📌 Project Overview
**HH Goa 2026 Task 3: Face Identification & Blockchain Verification** implements an automated pipeline to:
1. Extract facial boundaries and compute 128-dimensional facial embedding vectors.
2. Query Google Reverse Image Search via SerpAPI to discover online appearances and social media posts.
3. Compute cryptographic digests (SHA-256 / Keccak-256) and upload the verified record to the Ethereum Sepolia blockchain for immutable auditability.

---

## 💻 System Prerequisites
- **Python**: Version 3.10 or higher (Tested on Python 3.10, 3.11, 3.12, 3.13)
- **Git**: For version control
- **Web3 Wallet**: MetaMask or similar (for Sepolia testnet transactions)

---

## 🚀 Quick Installation

### 1. Clone the Repository
```bash
git clone <your-repository-url>
cd hh-goa-task3-face-blockchain
```

### 2. Set Up Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🔑 Configuration & Environment Variables

Copy the sample environment file:
```bash
cp .env.example .env
```

Edit `.env` with your API keys and credentials:
```ini
# SerpAPI Configuration (Google Reverse Image Search)
SERPAPI_API_KEY=your_serpapi_key_here

# Infura Ethereum Sepolia RPC Configuration
INFURA_API_KEY=your_infura_key_here
SEPOLIA_RPC_URL=https://sepolia.infura.io/v3/your_infura_key_here

# Smart Contract Details (Deployed on Sepolia Testnet)
CONTRACT_ADDRESS=0xYourDeployedContractAddress

# Wallet Details (Sepolia Testnet with test ETH)
WALLET_ADDRESS=0xYourWalletAddress
WALLET_PRIVATE_KEY=your_wallet_private_key_without_quotes
```

---

## 🧪 Running the Pipeline

### Run on a Sample Image
```bash
python src/pipeline.py data/input_faces/sample.jpg
```

### Run on Your Own Custom Face Image
```bash
python src/pipeline.py path/to/your/face_image.jpg
```

---

## 📂 Output Artifacts

All execution results are saved in `data/results/`:
- `face_encoding.json`: Extracted 128-D embedding vector.
- `search_results.json`: Reverse image search query results and social media matches.
- `blockchain_receipt.json`: Transaction hash, block number, gas used, and Etherscan URL.
- `pipeline_results.json`: Complete consolidated JSON output.

---

## 🧪 Running Tests
```bash
pytest tests/ -v
```
