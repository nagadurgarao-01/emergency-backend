const express = require('express');
const router = express.Router();
const multer = require('multer');
const path = require('path');
const MissingPerson = require('../models/MissingPerson');

const fs = require('fs');

const { storage } = require('../config/cloudinary');
const upload = multer({ storage: storage });

// Create a new Missing Person Alert
router.post('/create', upload.single('image'), async (req, res) => {
    try {
        const { name, age, gender, description, lat, lng, contactDeviceId } = req.body;

        // Construct photo URL (assuming server serves 'uploads' statically)
        // If running locally, it might be http://localhost:PORT/uploads/filename
        // Ideally, we store the relative path and the client prepends the base URL, 
        // or we construct the full URL here using req.protocol + '://' + req.get('host')

        if (!req.file) {
            return res.status(400).json({ error: 'Image is required' });
        }

        const photoUrl = req.file.path; // Cloudinary URL

        const newAlert = new MissingPerson({
            name,
            age,
            gender,
            description,
            lastSeenLocation: { lat, lng },
            photoUrl,
            contactDeviceId
        });

        await newAlert.save();
        res.status(201).json({ message: 'Alert created successfully', alert: newAlert });

    } catch (error) {
        console.error('Error creating alert:', error);
        res.status(500).json({ error: 'Server error' });
    }
});

// Get all active alerts
router.get('/active', async (req, res) => {
    try {
        const alerts = await MissingPerson.find({ status: 'ACTIVE' }).sort({ createdAt: -1 });
        res.json(alerts);
    } catch (error) {
        res.status(500).json({ error: 'Server error' });
    }
});

module.exports = router;
