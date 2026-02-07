require("dotenv").config();
const express = require("express");
const connectDB = require("./config/db");

const app = express();
connectDB();

app.use(express.json());

app.use("/api/device", require("./routes/deviceRoutes"));
app.use("/api/alert", require("./routes/alertRoutes"));
app.use("/api/missing", require("./routes/missingPersonRoutes"));
app.use("/uploads", express.static("uploads"));

app.get("/api/status", (req, res) => {
  res.json({ status: "Backend running" });
});

app.listen(process.env.PORT, () =>
  console.log("Server started")
);
