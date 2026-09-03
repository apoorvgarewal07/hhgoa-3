// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title FaceDataRegistry
 * @dev Immutable on-chain registry for verified facial encodings and reverse image search matches.
 * HH Goa 2026 - Task 3
 */
contract FaceDataRegistry {

    struct FaceRecord {
        bytes32 faceEncoding;   // Hash of face encoding vector
        bytes32 imageHash;      // Hash of original image
        bytes32 postHash;       // Hash of discovered social media post
        string socialMediaURL;  // Discovered source post URL
        uint256 timestamp;      // Block timestamp
        address uploadedBy;     // Sender wallet address
    }

    mapping(uint256 => FaceRecord) public records;
    uint256 public recordCount = 0;

    event FaceDataUploaded(
        uint256 indexed recordId,
        bytes32 faceEncoding,
        string socialMediaURL,
        uint256 timestamp
    );

    /**
     * @notice Uploads a verified face identification record to the blockchain.
     * @param _faceEncoding Cryptographic hash of the 128-D facial vector
     * @param _imageHash Cryptographic hash of the raw image
     * @param _postHash Cryptographic hash of the discovered match post
     * @param _socialMediaURL Public URL where the image appears online
     * @return recordId The unique index of the created on-chain record
     */
    function uploadFaceData(
        bytes32 _faceEncoding,
        bytes32 _imageHash,
        bytes32 _postHash,
        string memory _socialMediaURL
    ) public returns (uint256) {
        uint256 recordId = recordCount;

        records[recordId] = FaceRecord({
            faceEncoding: _faceEncoding,
            imageHash: _imageHash,
            postHash: _postHash,
            socialMediaURL: _socialMediaURL,
            timestamp: block.timestamp,
            uploadedBy: msg.sender
        });

        emit FaceDataUploaded(
            recordId,
            _faceEncoding,
            _socialMediaURL,
            block.timestamp
        );

        recordCount++;
        return recordId;
    }

    /**
     * @notice Verifies if a valid non-empty face record exists at the given record ID.
     * @param _recordId Index of the record
     * @return bool True if record exists and contains valid encoding hash
     */
    function verifyFaceData(uint256 _recordId) public view returns (bool) {
        require(_recordId < recordCount, "Record does not exist");
        FaceRecord memory record = records[_recordId];
        return record.faceEncoding != bytes32(0);
    }

    /**
     * @notice Retrieves full record details.
     * @param _recordId Index of the record
     */
    function getRecord(uint256 _recordId) public view returns (FaceRecord memory) {
        require(_recordId < recordCount, "Record does not exist");
        return records[_recordId];
    }
}
