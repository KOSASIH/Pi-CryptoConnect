// contracts/erc721.sol

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";

contract MyERC721 is ERC721 {
    constructor(string memory name_, string memory symbol_) ERC721(name_, symbol_) {}

    function mint(address to, uint256 tokenId) public {
        _mint(to, tokenId);
    }

    function transferFrom(address from, address to, uint256 tokenId) public override {
        _transfer(from, to, tokenId);
    }
}
