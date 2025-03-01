// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";

contract Migrations is Ownable {
    // State variable to track the last completed migration
    uint public lastCompletedMigration;

    // Event to log migration completion
    event MigrationCompleted(uint completed);

    // Function to set the completed migration
    function setCompleted(uint completed) public onlyOwner {
        lastCompletedMigration = completed;
        emit MigrationCompleted(completed); // Emit event on completion
    }

    // Function to get the last completed migration
    function getLastCompletedMigration() public view returns (uint) {
        return lastCompletedMigration;
    }
}
