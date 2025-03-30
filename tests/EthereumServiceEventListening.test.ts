import { expect } from "chai";
import { ethers } from "hardhat";
import EthereumService from "../services/EthereumService"; // Adjust the import based on your file structure
import { Contract } from "ethers";

describe("EthereumService Event Listening", function () {
  let ethereumService: EthereumService;
  let testContract: Contract;
  let owner: any;

  beforeEach(async function () {
    [owner] = await ethers.getSigners();
    const TestContract = await ethers.getContractFactory("TestContract"); // Replace with your contract
    testContract = await TestContract.deploy();
    await testContract.deployed();
    ethereumService = new EthereumService();
  });

  it("should listen for Transfer events", async function () {
    const eventPromise = new Promise((resolve) => {
      testContract.on("Transfer", (from, to, value) => {
        resolve({ from, to, value });
      });
    });

    await testContract.transfer(owner.address, ethers.utils.parseEther("1")); // Trigger the event

    const eventData = await eventPromise;
    expect(eventData.from).to.equal(owner.address);
    expect(eventData.to).to.equal(owner.address);
    expect(eventData.value.toString()).to.equal(ethers.utils.parseEther("1").toString());
  });
});
