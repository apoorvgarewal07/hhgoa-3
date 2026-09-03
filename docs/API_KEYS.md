# API Keys & Credentials Guide

This guide walks you through acquiring all required free API keys and testnet resources in under 10 minutes.

---

## 1. SerpAPI (Google Reverse Image Search)
- **Website**: [https://serpapi.com](https://serpapi.com)
- **Free Tier**: 100 free searches per month (no credit card required).

### Steps to Acquire:
1. Visit [https://serpapi.com](https://serpapi.com) and click **Sign Up** / **Register**.
2. Complete signup and verify your email.
3. Access your **Dashboard** at `https://serpapi.com/dashboard`.
4. Copy your private API key from the **API Key** section.
5. Paste it into your `.env` file:
   ```ini
   SERPAPI_API_KEY=your_copied_serpapi_key
   ```

---

## 2. Infura (Ethereum Sepolia RPC Endpoint)
- **Website**: [https://infura.io](https://infura.io)
- **Free Tier**: Free access to Ethereum Sepolia Testnet.

### Steps to Acquire:
1. Go to [https://infura.io](https://infura.io) and create a free developer account.
2. Click **Create New Key** / **New API Key**.
3. Select Network: **Web3 API (formerly Ethereum)** and enter a project name (e.g. `HH-Goa-Task3`).
4. In the **Endpoints** tab, find **Sepolia Testnet**.
5. Copy the Sepolia RPC URL (format: `https://sepolia.infura.io/v3/YOUR_PROJECT_ID`).
6. Set the values in your `.env` file:
   ```ini
   INFURA_API_KEY=your_project_id
   SEPOLIA_RPC_URL=https://sepolia.infura.io/v3/your_project_id
   ```

---

## 3. Sepolia Testnet ETH (Free Faucets)
To broadcast on-chain transactions, your wallet needs Sepolia test ETH.

### Free Faucets:
- **Google Cloud Web3 Sepolia Faucet**: [https://cloud.google.com/application/web3/faucet/ethereum/sepolia](https://cloud.google.com/application/web3/faucet/ethereum/sepolia)
- **Sepolia PoW Faucet**: [https://sepolia-faucet.pk910.de](https://sepolia-faucet.pk910.de)
- **Alchemy Sepolia Faucet**: [https://www.sepoliafaucet.com](https://www.sepoliafaucet.com)
- **Infura Faucet**: [https://infura.io/faucet/sepolia](https://infura.io/faucet/sepolia)

---

## 4. Wallet Private Key Setup
1. Open your MetaMask or Ethereum wallet.
2. Ensure network is switched to **Sepolia**.
3. Export your account private key (**Never share or commit this to public repositories**).
4. Add your wallet address and private key to `.env`:
   ```ini
   WALLET_ADDRESS=0xYourWalletAddress
   WALLET_PRIVATE_KEY=your_private_key_hex
   ```
