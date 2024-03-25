// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

// credential type
struct Credential {
    address issuer;
    bytes signature;
    bytes checksum;
    string dataLocation;
}