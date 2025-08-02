const express = require("express");
const PORT = process.env.PORT || 3000;

const app = express();
app.use(express.json());

// Store pending wake requests
let pendingWake = null;

// Endpoint for external trigger
app.post("/wake", (req, res) => {
    const { mac } = req.body;
    if (!mac) return res.status(400).send("MAC address required");

    // Save wake request
    pendingWake = { mac, timestamp: Date.now() };
    console.log(`💡 Wake request queued for ${mac}`);
    res.send({ success: true, message: "Wake request queued" });
});

// Endpoint polled by Raspberry Pi
app.get("/wake-request", (req, res) => {
    if (pendingWake && Date.now() - pendingWake.timestamp < 60000) {
        const response = { wake: true, mac: pendingWake.mac };
        pendingWake = null; // Consume request so it’s used once
        return res.json(response);
    }
    res.json({ wake: false });
});

// Health check
app.get("/", (req, res) => res.send("✅ Server is alive"));

app.listen(PORT, () => {
    console.log(`Relay server running on port ${PORT}`);
});

