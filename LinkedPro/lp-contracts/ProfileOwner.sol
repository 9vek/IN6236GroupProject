// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./Credential.sol";

contract ProfileOwner {

    // profile owner
    address public owner;

    // other info


    // credential list
    mapping(bytes32 => Credential) private credentials;

    // events
    event CredentialAdded(
        bytes32 indexed credentialId,
        address issuer,
        string dataLocation
    );
    event CredentialSigned(bytes32 indexed credentialId, address issuer);
    event CredentialRevoked(bytes32 indexed credentialId, address issuer);
    event CredentialRemoved(bytes32 indexed credentialId);

    event CredentialStatusRequested(bytes32 indexed credentialId);
    event CredentialStatusUpdated(bytes32 indexed credentialId, bool isCertified);
    event CredentialSignatureUpdated(bytes32 indexed credentialId, bytes signature);

    // constructor
    constructor() {
        owner = msg.sender;
    }

    // modifiers
    modifier onlyOwner() {
        require(msg.sender == owner, "Caller is not the owner");
        _;
    }

    modifier onlyIssuer(bytes32 _credentialId) {
        require(
            credentials[_credentialId].issuer == msg.sender,
            "Only issuer can sign the credential"
        );
        _;
    }

    // only profile owner can call to add a credential
    function addCredential(
        address _issuer,
        bytes calldata _checksum,
        string calldata _dataLocation
    ) external onlyOwner returns (bytes32 credentialId) {

        // require(credentialId.length <= 32, "Text too long");

        credentialId = keccak256(abi.encodePacked(_issuer, _checksum));
        Credential memory newCredential = Credential({
            issuer: _issuer,
            signature: "",
            checksum: _checksum,
            dataLocation: _dataLocation
        });
        credentials[credentialId] = newCredential;
        // emit ClaimAdded
        emit CredentialAdded(credentialId, _issuer, _dataLocation);
        return credentialId;
    }

    // issuers can sign related credentials by calling his
    function signCredential(bytes32 _credentialId, bytes calldata _signature)
        external
        onlyIssuer(_credentialId)
        returns (bool isSuccessful) {
        Credential storage credential = credentials[_credentialId];
        credential.signature = _signature;
        emit CredentialSigned(_credentialId, msg.sender);
        return true;
    }

    // issuers can revoke related credentials by calling his
    function revokeCredential(bytes32 _credentialId)
        external
        onlyIssuer(_credentialId)
        returns (bool isSuccessful) {
        Credential storage credential = credentials[_credentialId];
        credential.signature = "";
        emit CredentialRevoked(_credentialId, msg.sender);
        return true;
    }

    // only profile owner can call to remove a credential
    function removeCredential(bytes32 _credentialId)
        external
        onlyOwner
        returns (bool isSuccessful) {
        delete credentials[_credentialId];
        emit CredentialRemoved(_credentialId);
        return true;
    }

    // 请求更新凭证状态（链下服务监听当前事件，并通过外部系统更新状态）
    function requestCredentialStatus(bytes32 _credentialId) external onlyOwner {
        require(credentials[_credentialId].issuer != address(0), "Credential does not exist");

        // 触发事件，链下服务监听后可进行进一步的处理
        emit CredentialStatusRequested(_credentialId);
    }

    // 更新凭证签名（模拟外部认证机构签名操作的结果）
    function updateCredentialSignature(bytes32 _credentialId, bytes calldata _signature) external onlyOwner {
        Credential storage credential = credentials[_credentialId];
        credential.signature = _signature;
        emit CredentialSignatureUpdated(_credentialId, _signature);
    }

}
