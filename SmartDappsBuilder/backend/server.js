const express = require('express');
const bodyParser = require('body-parser');
const connectDB = require('./config/db'); // Import the database connection function
const dAppRoutes = require('./routes/dAppRoutes'); // Import DApp routes
const authRoutes = require('./routes/authRoutes'); // Import authentication routes
const { authenticate } = require('./middleware/authMiddleware'); // Import authentication middleware
const cors = require('cors'); // Import CORS middleware
require('dotenv').config(); // Load environment variables from .env file

const app = express();
const PORT = process.env.PORT || 5000;

// Connect to the database
connectDB();

// Middleware
app.use(cors()); // Enable CORS for all routes
app.use(bodyParser.json()); // Parse JSON request bodies

// Routes
app.use('/api/dapps', authenticate, dAppRoutes); // DApp routes with authentication
app.use('/api/auth', authRoutes); // Authentication routes

// Health check route
app.get('/api/health', (req, res) => {
    res.status(200).json({ success: true, message: 'API is running' });
});

// Start the server
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
