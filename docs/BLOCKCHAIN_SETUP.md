# Smart Contract Deployment & Verification Guide

This guide details how to compile, deploy, and verify the `FaceDataRegistry.sol` smart contract on Ethereum Sepolia Testnet using Remix IDE or web3.

---

## 📄 Smart Contract Overview
- **File**: `blockchain/FaceDataRegistry.sol`
- **Solidity Version**: `^0.8.0`
- **License**: MIT

### Contract Functions:
1. `uploadFaceData(bytes32 _faceEncoding, bytes32 _imageHash, bytes32 _postHash, string memory _socialMediaURL) returns (uint256)`:
   Stores the cryptographic record and emits the `FaceDataUploaded` event.
2. `verifyFaceData(uint256 _recordId) returns (bool)`:
   Validates that the record exists and is non-empty.
3. `getRecord(uint256 _recordId) returns (FaceRecord memory)`:
   Fetches full struct details.

---

## 🚀 Deploying via Remix IDE (Step-by-Step)

1. Open [https://remix.ethereum.org](https://remix.ethereum.org).
2. Under the **File Explorer**, create a new file named `FaceDataRegistry.sol`.
3. Copy and paste the contents of `blockchain/FaceDataRegistry.sol`.
4. Go to the **Solidity Compiler** tab on the left navigation bar:
   - Select compiler version `0.8.20` or any `0.8.x`.
   - Click **Compile FaceDataRegistry.sol**.
5. Switch to the **Deploy & Run Transactions** tab:
   - Environment: Select **Injected Provider - MetaMask**.
   - Make sure your MetaMask network is set to **Sepolia Testnet**.
   - Account: Ensure your wallet address has Sepolia test ETH.
   - Contract: Select `FaceDataRegistry - FaceDataRegistry.sol`.
   - Click the orange **Deploy** button.
6. Confirm the deployment transaction in MetaMask.
7. Once mined, find the deployed contract under **Deployed Contracts**:
   - Click the copy button next to the deployed address.
   - Paste the address into your `.env` file:
     ```ini
     CONTRACT_ADDRESS=0xYourDeployedContractAddress
     ```
8. In the Solidity Compiler tab, click **ABI** (copy icon) and paste into `blockchain/contract_abi.json`.

---

## 🔍 On-Chain Verification
You can inspect every uploaded record, transaction hash, block number, and emitted events directly on Sepolia Etherscan:
- `https://sepolia.etherscan.io/address/<CONTRACT_ADDRESS>`
- `https://sepolia.etherscan.io/tx/<TX_HASH>`
