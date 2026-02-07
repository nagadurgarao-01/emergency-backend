const express = require("express");
const Device = require("../models/Device");
const auth = require("../middleware/auth");
const router = express.Router();

router.post("/register", auth, async (req, res) => {
  const { deviceId, primaryNumber, backupNumber } = req.body;

  if (!deviceId || !primaryNumber) {
    return res.status(400).json({ error: "Missing data" });
  }

  const device = await Device.findOneAndUpdate(
    { deviceId },
    { primaryNumber, backupNumber },
    { upsert: true, new: true }
  );

  res.json({ success: true, device });
});

module.exports = router;
