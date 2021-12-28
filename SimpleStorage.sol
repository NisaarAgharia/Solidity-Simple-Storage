// SPDX-License-Identifier: GPL-3.0

pragma solidity ^0.8.0;

/**
 * @title Storage
 * @dev Store & retrieve value in a variable
 */
contract Storage {
    uint256 number;
    string messageData;

    /**
     * @dev Store value in variable
     * @param num value to store
     */
    function store(uint256 num) public returns (uint256) {
        number = num;
        // messageData = msg.data;
        return number;
    }

    function fund(uint256 amount) public payable {
        number = number + amount;
    }

    /**
     * @dev Return value
     * @return value of 'number'
     */
    function retrieve() public view returns (uint256) {
        return number;
    }

    function getMessageData() public pure returns (string memory) {
        return string(msg.data);
    }
}
