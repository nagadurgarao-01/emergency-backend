const express = require("express");
const Alert = require("../models/Alert");
const Device = require("../models/Device");
const auth = require("../middleware/auth");
const router = express.Router();

router.post("/", auth, async (req, res) => {
  const { deviceId, latitude, longitude, trigger } = req.body;

  if (!deviceId || !latitude || !longitude) {
    return res.status(400).json({ error: "Invalid payload" });
  }

  // Auto-register device if not found (for demo purposes)
  let device = await Device.findOne({ deviceId });
  if (!device) {
    device = new Device({ deviceId, name: "Unknown Device", phone: "0000000000" });
    await device.save();
    console.log(`New device auto-registered: ${deviceId}`);
  }

  const alert = new Alert({
    deviceId,
    latitude,
    longitude,
    trigger
  });

  await alert.save();

  console.log("🚨 EMERGENCY ALERT:", alert);

  res.json({ success: true });
});

module.exports = router;
