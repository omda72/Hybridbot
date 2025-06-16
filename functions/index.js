const functions = require("firebase-functions");
const express = require("express");
const cors = require("cors");

const app = express();
app.use(cors());
app.use(express.json());

// 🌐 Webhook route (for Solana/Ethereum bot events)
app.post("/webhook", (req, res) => {
  const event = req.body;
  console.log("📥 Webhook received:", event);

  // Later: trigger a test trade or log to Firestore here

  res.status(200).send("✅ Webhook received");
});

// 🧪 Optional: test route for verifying connection
app.get("/ping", (req, res) => {
  res.send("🚀 Firebase Function is live!");
});
// ✅ NEW: Live route your frontend is calling
app.get("/bots", (req, res) => {
  const bots = [
    { id: 1, name: 'MomentumBot', status: 'active' },
    { id: 2, name: 'MeanReverter', status: 'paused' }
  ];
  res.status(200).json(bots);
});
exports.api = functions.https.onRequest(app);
