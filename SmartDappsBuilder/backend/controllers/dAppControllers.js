const DApp = require('../models/DAppModel');

// Create a new DApp
exports.createDApp = async (req, res) => {
    try {
        const { name, description } = req.body;

        // Validate input
        if (!name || !description) {
            return res.status(400).json({ success: false, message: 'Name and description are required.' });
        }

        const newDApp = new DApp({
            name,
            description,
            creator: req.user._id // Assuming req.user is set by the authentication middleware
        });

        await newDApp.save();
        res.status(201).json({ success: true, data: newDApp });
    } catch (error) {
        console.error('Error creating DApp:', error);
        res.status(500).json({ success: false, message: 'Server error. Please try again later.' });
    }
};

// Get all DApps
exports.getAllDApps = async (req, res) => {
    try {
        const dApps = await DApp.find().populate('creator', 'username'); // Populate creator field with username
        res.status(200).json({ success: true, data: dApps });
    } catch (error) {
        console.error('Error fetching DApps:', error);
        res.status(500).json({ success: false, message: 'Server error. Please try again later.' });
    }
};

// Get a single DApp by ID
exports.getDAppById = async (req, res) => {
    try {
        const dApp = await DApp.findById(req.params.id).populate('creator', 'username');
        if (!dApp) {
            return res.status(404).json({ success: false, message: 'DApp not found.' });
        }
        res.status(200).json({ success: true, data: dApp });
    } catch (error) {
        console.error('Error fetching DApp:', error);
        res.status(500).json({ success: false, message: 'Server error. Please try again later.' });
    }
};

// Update a DApp by ID
exports.updateDApp = async (req, res) => {
    try {
        const { name, description } = req.body;

        // Validate input
        if (!name || !description) {
            return res.status(400).json({ success: false, message: 'Name and description are required.' });
        }

        const updatedDApp = await DApp.findByIdAndUpdate(
            req.params.id,
            { name, description, updatedAt: Date.now() },
            { new: true, runValidators: true } // Return the updated document
        );

        if (!updatedDApp) {
            return res.status(404).json({ success: false, message: 'DApp not found.' });
        }

        res.status(200).json({ success: true, data: updatedDApp });
    } catch (error) {
        console.error('Error updating DApp:', error);
        res.status(500).json({ success: false, message: 'Server error. Please try again later.' });
    }
};

// Delete a DApp by ID
exports.deleteDApp = async (req, res) => {
    try {
        const deletedDApp = await DApp.findByIdAndDelete(req.params.id);
        if (!deletedDApp) {
            return res.status(404).json({ success: false, message: 'DApp not found.' });
        }
        res.status(200).json({ success: true, message: 'DApp deleted successfully.' });
    } catch (error) {
        console.error('Error deleting DApp:', error);
        res.status(500).json({ success: false, message: 'Server error. Please try again later.' });
    }
};
