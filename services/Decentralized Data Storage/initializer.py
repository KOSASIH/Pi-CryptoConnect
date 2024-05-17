const PiNetwork = require('pinetwork-js');

// If you want to use the mainnet, set Chain ID to 1.
const chainId = 0; // Testnet
const pinetwork = new PiNetwork(`https://mainnet-api.ainetwork.ai`, chainId);

// Set your private key
const privateKey = 'your_private_key_here';
const account = pinetwork.wallet.addAndSetDefaultAccount(privateKey);

// Set your app name
const appName = 'my_bot';

// Set the app path
const appPath = `/apps/${appName}`;

// Set the value path
const valuePath = `${appPath}/messages/${account.address}/${Date.now()}/user`;

// Set the function path
const functionPath = `${appPath}/messages/$user_addr/$timestamp/user`;

// Set the rule path
const rulePath = `${appPath}/messages/$user_address/$timestamp/echo-bot`;
