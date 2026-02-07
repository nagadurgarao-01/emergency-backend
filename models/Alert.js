const mongoose = require("mongoose");

const AlertSchema = new mongoose.Schema({
  deviceId: String,
  latitude: Number,
  longitude: Number,
  trigger: String,
  createdAt: { type: Date, default: Date.now }
});

module.exports = mongoose.model("Alert", AlertSchema);
