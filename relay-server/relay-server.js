const express = require("express");
const path = require("path");
const PORT = process.env.PORT || 3000;

const app = express();
app.use(express.json());

app.use(express.static(path.join(__dirname, "public")));

let pendingWake = null;

app.post("/wake", (req, res) => {
    const { mac } = req.body;
    if (!mac) return res.status(400).send("MAC address required");

    // Save wake request
    pendingWake = { mac, timestamp: Date.now() };
    console.log(`💡 Wake request queued for ${mac}`);
    res.send({ success: true, message: "Wake request queued" });
});

app.get("/wake-request", (req, res) => {
    if (pendingWake && Date.now() - pendingWake.timestamp < 60000) {
        const response = { wake: true, mac: pendingWake.mac };
        pendingWake = null; // Consume request so it’s only used once
        return res.json(response);
    }
    res.json({ wake: false });
});

// Default fallback (if no static file found)
app.get("*", (req, res) => {
    res.sendFile(path.join(__dirname, "public", "index.html"));
});

app.listen(PORT, () => {
    console.log(`Relay server running on port ${PORT}`);
});
