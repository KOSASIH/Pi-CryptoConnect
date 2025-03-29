// model.js

class DAppModel {
    constructor() {
        // Predefined dataset for training (mock data)
        this.dataset = [
            { keywords: ["voting", "election", "poll"], idea: "Decentralized Voting System" },
            { keywords: ["supply chain", "logistics", "tracking"], idea: "Blockchain-based Supply Chain Management" },
            { keywords: ["social media", "network", "community"], idea: "Decentralized Social Media Network" },
            { keywords: ["NFT", "art", "digital"], idea: "NFT Marketplace for Digital Art" },
            { keywords: ["finance", "lending", "loans"], idea: "Decentralized Finance (DeFi) Lending Platform" },
            { keywords: ["crowdfunding", "fundraising", "projects"], idea: "Crowdfunding Platform using Smart Contracts" },
            { keywords: ["identity", "verification", "authentication"], idea: "Decentralized Identity Verification System" },
            { keywords: ["real estate", "property", "investment"], idea: "Real Estate Tokenization Platform" },
            { keywords: ["loyalty", "rewards", "points"], idea: "Blockchain-based Loyalty Rewards Program" },
            { keywords: ["energy", "trading", "peer-to-peer"], idea: "Peer-to-Peer Energy Trading Platform" }
        ];
    }

    // Method to predict DApp idea based on user input
    predictDAppIdea(userInput) {
        const lowerInput = userInput.toLowerCase();
        const matchedIdeas = [];

        // Check for keyword matches in the dataset
        for (const data of this.dataset) {
            for (const keyword of data.keywords) {
                if (lowerInput.includes(keyword)) {
                    matchedIdeas.push(data.idea);
                    break; // Stop checking other keywords for this idea
                }
            }
        }

        // Return matched ideas or a default message
        return matchedIdeas.length > 0 
            ? matchedIdeas 
            : ["No specific DApp idea found. Please try different keywords."];
    }

    // Method to train the model (mock implementation)
    trainModel() {
        // In a real implementation, you would train your model here
        console.log("Training model with dataset:", this.dataset);
        // Simulate training process
        return true;
    }
}

// Export an instance of the DApp model
const dAppModel = new DAppModel();
module.exports = dAppModel;
