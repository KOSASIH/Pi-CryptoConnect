const PiNetwork = require('pinetwork-js');
const dotenv = require('dotenv');
const readline = require('readline');

// Load environment variables from .env file
dotenv.config();

// If you want to use the mainnet, set Chain ID to 1.
const chainId = process.env.CHAIN_ID || 0; // Testnet
const pinetwork = new PiNetwork(process.env.API_URL || 'https://mainnet-api.ainetwork.ai', chainId);

// Set your private key from environment variable
const privateKey = process.env.PRIVATE_KEY;
if (!privateKey) {
    console.error("Private key is not set. Please set it in the .env file.");
    process.exit(1);
}

const account = pinetwork.wallet.addAndSetDefaultAccount(privateKey);

// Set your app name
const appName = 'my_bot';

// Set the app path
const appPath = `/apps/${appName}`;

// Function to send a message
async function sendMessage(userAddress, message) {
    const timestamp = Date.now();
    const valuePath = `${appPath}/messages/${account.address}/${timestamp}/user`;
    
    try {
        await pinetwork.database.set(valuePath, { message, userAddress });
        console.log(`Message sent to ${userAddress}: ${message}`);
    } catch (error) {
        console.error("Error sending message:", error);
    }
}

// Function to listen for incoming messages
async function listenForMessages() {
    const functionPath = `${appPath}/messages/$user_addr/$timestamp/user`;
    
    try {
        pinetwork.database.on(functionPath, (data) => {
            console.log(`Received message from ${data.userAddress}: ${data.message}`);
        });
    } catch (error) {
        console.error("Error listening for messages:", error);
    }
}

// Function to start the bot
async function startBot() {
    console.log("Bot is starting...");
    await listenForMessages();
    
    const rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout
    });

    rl.on('line', async (input) => {
        const [userAddress, ...messageParts] = input.split(' ');
        const message = messageParts.join(' ');
        await sendMessage(userAddress, message);
    });
}

// Start the bot
startBot();
