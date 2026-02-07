const mongoose = require("mongoose");

const DeviceSchema = new mongoose.Schema({
  deviceId: { type: String, unique: true },
  primaryNumber: String,
  backupNumber: String,
  createdAt: { type: Date, default: Date.now }
});

module.exports = mongoose.model("Device", DeviceSchema);
