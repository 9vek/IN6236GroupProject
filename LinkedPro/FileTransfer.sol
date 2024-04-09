// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract FileTransfer {
    mapping(address => string[]) private fileLocations;

    event FileUploaded(address indexed user, string location);
    
    function uploadFileLocation(string memory _location) public {
        fileLocations[msg.sender].push(_location);
        emit FileUploaded(msg.sender, _location);
    }

    function getFileLocations(address _user) public view returns (string[] memory) {
        return fileLocations[_user];
    }
}
