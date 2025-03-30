import { expect } from "chai";
import { ethers } from "hardhat";
import EthereumService from "../services/EthereumService"; // Adjust the import based on your file structure

describe("EthereumService", function () {
  let ethereumService: EthereumService;
  let owner: any;
  let recipient: any;

  beforeEach(async function () {
    [owner, recipient] = await ethers.getSigners();
    ethereumService = new EthereumService();
  });

  it("should send a transaction successfully", async function () {
    const initialBalance = await ethers.provider.getBalance(recipient.address);
    const txHash = await ethereumService.sendTransaction(recipient.address, ethers.utils.parseEther("0.01"));
    
    // Wait for the transaction to be mined
    await ethers.provider.waitForTransaction(txHash);

    const finalBalance = await ethers.provider.getBalance(recipient.address);
    expect(finalBalance).to.equal(initialBalance.add(ethers.utils.parseEther("0.01")));
  });

  it("should revert when sending insufficient funds", async function () {
    await expect(ethereumService.sendTransaction(recipient.address, ethers.utils.parseEther("100"))).to.be.revertedWith("Insufficient funds");
  });
});
