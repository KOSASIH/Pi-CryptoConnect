// Set the identity verification data
const identityData = {
  name: 'John Doe',
  email: 'john.doe@example.com',
  address: account.address,
  timestamp: Date.now()
};

// Set the identity verification value path
const identityValuePath = `${appPath}/identity/${account.address}`;

// Set the identity verification rule path
const identityRulePath = `${appPath}/identity`;

// Set the identity verification rule
const identityRule = {
  value: {
    '.rule': {
      'write': true,
    },
  },
  nonce: -1,
};

// Set the identity verification value
const identityValue = {
  value: identityData,
  nonce: -1,
};

// Set the identity verification rule
const identityRule = {
  value: {
    '.write': 'auth.addr === account.address',
  },
  nonce: -1,
};

// Set the identity verification rule
pinetwork.db.ref(identityRulePath).set(identityRule)
  .then(() => {
    console.log('Identity rule set successfully');
  })
  .catch((error) => {
    console.error('Error setting identity rule:', error);
  });

// Set the identity verification value
pinetwork.db.ref(identityValuePath).set(identityValue)
  .then(() => {
    console.log('Identity value set successfully');
  })
  .catch((error) => {
    console.error('Error setting identity value:', error);
  });
