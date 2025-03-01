// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract DAppContract {
    // State variables
    string public name;
    string public description;
    address public owner;

    // Event to log changes
    event DAppUpdated(string name, string description);

    // Modifier to restrict access to the owner
    modifier onlyOwner() {
        require(msg.sender == owner, "You are not the owner");
        _;
    }

    // Constructor to initialize the contract
    constructor(string memory _name, string memory _description) {
        name = _name;
        description = _description;
        owner = msg.sender; // Set the contract creator as the owner
    }

    // Function to update the DApp's name and description
    function updateDApp(string memory _name, string memory _description) public onlyOwner {
        name = _name;
        description = _description;
        emit DAppUpdated(_name, _description); // Emit event on update
    }

    // Function to get the DApp's details
    function getDAppDetails() public view returns (string memory, string memory) {
        return (name, description);
    }
}
