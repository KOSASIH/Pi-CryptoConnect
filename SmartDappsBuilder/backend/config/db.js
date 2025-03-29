const mongoose = require('mongoose');

// MongoDB connection URI
const mongoURI = process.env.MONGO_URI || 'mongodb://localhost:27017/smart_dapps_builder'; // Default to local MongoDB

// Function to connect to the database
const connectDB = async () => {
    try {
        await mongoose.connect(mongoURI, {
            useNewUrlParser: true,
            useUnifiedTopology: true,
            useCreateIndex: true, // Use createIndex for unique indexes
            useFindAndModify: false // Disable findAndModify to use native findOneAndUpdate
        });
        console.log('MongoDB connected successfully');
    } catch (error) {
        console.error('MongoDB connection error:', error);
        process.exit(1); // Exit the process with failure
    }
};

module.exports = connectDB;
