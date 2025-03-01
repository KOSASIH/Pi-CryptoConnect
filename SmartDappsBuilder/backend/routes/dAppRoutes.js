const express = require('express');
const router = express.Router();
const dAppController = require('../controllers/dAppController');
const { authenticate } = require('../middleware/authMiddleware'); // Middleware for authentication

// Route to create a new DApp
router.post('/create', authenticate, dAppController.createDApp);

// Route to get all DApps
router.get('/', dAppController.getAllDApps);

// Route to get a single DApp by ID
router.get('/:id', dAppController.getDAppById);

// Route to update a DApp by ID
router.put('/:id', authenticate, dAppController.updateDApp);

// Route to delete a DApp by ID
router.delete('/:id', authenticate, dAppController.deleteDApp);

module.exports = router;
