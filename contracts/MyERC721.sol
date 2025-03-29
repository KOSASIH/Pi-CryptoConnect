// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/Pausable.sol";
import "@openzeppelin/contracts/utils/Strings.sol";

contract MyERC721 is ERC721, Ownable, Pausable {
    using Strings for uint256;

    // Mapping from token ID to token URI
    mapping(uint256 => string) private _tokenURIs;

    constructor(string memory name_, string memory symbol_) ERC721(name_, symbol_) {}

    // Mint a new token
    function mint(address to, uint256 tokenId, string memory tokenURI) public onlyOwner whenNotPaused {
        _mint(to, tokenId);
        _setTokenURI(tokenId, tokenURI);
    }

    // Set the token URI
    function _setTokenURI(uint256 tokenId, string memory tokenURI) internal {
        require(_exists(tokenId), "ERC721Metadata: URI set of nonexistent token");
        _tokenURIs[tokenId] = tokenURI;
    }

    // Retrieve the token URI
    function tokenURI(uint256 tokenId) public view override returns (string memory) {
        require(_exists(tokenId), "ERC721Metadata: URI query for nonexistent token");
        return _tokenURIs[tokenId];
    }

    // Burn a token
    function burn(uint256 tokenId) public {
        require(_isApprovedOrOwner(msg.sender, tokenId), "ERC721: caller is not owner nor approved");
        _burn(tokenId);
        delete _tokenURIs[tokenId]; // Clear the token URI
    }

    // Override transfer function to include pausable functionality
    function transferFrom(address from, address to, uint256 tokenId) public override whenNotPaused {
        _transfer(from, to, tokenId);
    }

    // Safe transfer function
    function safeTransferFrom(address from, address to, uint256 tokenId) public override whenNotPaused {
        super.safeTransferFrom(from, to, tokenId);
    }

    // Safe transfer function with data
    function safeTransferFrom(address from, address to, uint256 tokenId, bytes memory _data) public override whenNotPaused {
        super.safeTransferFrom(from, to, tokenId, _data);
    }

    // Pause the contract
    function pause() public onlyOwner {
        _pause();
    }

    // Unpause the contract
    function unpause() public onlyOwner {
        _unpause();
    }
}
