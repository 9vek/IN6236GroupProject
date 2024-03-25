// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract CertificationAuthority {
    address public authorityOwner;
    mapping(bytes32 => bool) public certifications; // 文件的认证状态

    event CertificationIssued(bytes32 indexed fileChecksum);
    event CertificationRevoked(bytes32 indexed fileChecksum);

    constructor() {
        authorityOwner = msg.sender;
    }

    modifier onlyAuthorityOwner() {
        require(msg.sender == authorityOwner, "Caller is not the authority owner");
        _;
    }

    // 发行认证
    function issueCertification(bytes32 _fileChecksum) external onlyAuthorityOwner {
        certifications[_fileChecksum] = true;
        emit CertificationIssued(_fileChecksum);
    }

    // 撤销认证
    function revokeCertification(bytes32 _fileChecksum) external onlyAuthorityOwner {
        certifications[_fileChecksum] = false;
        emit CertificationRevoked(_fileChecksum);
    }

    // 检查认证状态
    function isCertified(bytes32 _fileChecksum) public view returns (bool) {
        return certifications[_fileChecksum];
    }
}
