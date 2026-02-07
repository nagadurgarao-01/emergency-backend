const mongoose = require('mongoose');

const MissingPersonSchema = new mongoose.Schema({
    name: { type: String, required: true },
    age: { type: Number, required: true },
    gender: { type: String, required: true },
    description: { type: String, required: true },
    lastSeenLocation: {
        lat: { type: Number, required: true },
        lng: { type: Number, required: true }
    },
    lastSeenTime: { type: Date, default: Date.now },
    photoUrl: { type: String, required: true }, // Path to local file or URL
    contactDeviceId: { type: String, required: true },
    status: { type: String, enum: ['ACTIVE', 'FOUND'], default: 'ACTIVE' },
    createdAt: { type: Date, default: Date.now }
});

module.exports = mongoose.model('MissingPerson', MissingPersonSchema);
