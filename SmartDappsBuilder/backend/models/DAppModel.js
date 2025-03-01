const mongoose = require('mongoose');

// Define the DApp schema
const dAppSchema = new mongoose.Schema({
    name: {
        type: String,
        required: true,
        trim: true, // Remove whitespace from both ends
        minlength: 3, // Minimum length for the name
        maxlength: 100 // Maximum length for the name
    },
    description: {
        type: String,
        required: true,
        trim: true,
        minlength: 10, // Minimum length for the description
        maxlength: 500 // Maximum length for the description
    },
    creator: {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'User ', // Reference to the User model
        required: true
    },
    createdAt: {
        type: Date,
        default: Date.now // Automatically set the creation date
    },
    updatedAt: {
        type: Date,
        default: Date.now // Automatically set the update date
    },
    metadata: {
        type: Object, // Can store additional metadata as an object
        default: {}
    }
});

// Middleware to update the updatedAt field before saving
dAppSchema.pre('save', function(next) {
    this.updatedAt = Date.now();
    next();
});

// Create the DApp model
const DApp = mongoose.model('DApp', dAppSchema);

module.exports = DApp;
