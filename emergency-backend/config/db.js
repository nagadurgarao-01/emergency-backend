const mongoose = require("mongoose");

const connectDB = async () => {
  try {
    await mongoose.connect(process.env.MONGO_URI, {
      dbName: 'women_safety',
    });
    console.log("MongoDB connected to women_safety");
  } catch (err) {
    console.error(err);
    process.exit(1);
  }
};

module.exports = connectDB;
