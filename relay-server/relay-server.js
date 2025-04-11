const express = require("express");
const { createServer } = require("http");
const { Server } = require("socket.io");
const cors = require("cors");

const app = express();
const httpServer = createServer(app);
const io = new Server(httpServer, {
  cors: {
    origin: "*"
  }
});

// Maps client IDs (e.g., "pi") to socket IDs
const clients = new Map();

app.use(cors());
app.use(express.json());

app.get("/", (req, res) => {
  res.send("Relay server is up!");
});

app.post("/wake", (req, res) => {
  const { mac } = req.body;

  const piSocketId = clients.get("pi");
  if (piSocketId && io.sockets.sockets.get(piSocketId)) {
    io.to(piSocketId).emit("wake", mac);
    console.log("📨 Wake signal sent to Pi for:", mac);
    res.status(200).send({ message: "Wake signal sent to Pi" });
  } else {
    console.log("❌ Pi not connected");
    res.status(500).send({ error: "Pi not connected" });
  }
});

io.on("connection", (socket) => {
  console.log("🔌 New client connected:", socket.id);

  socket.on("identify", (id) => {
    clients.set(id, socket.id);
    console.log(`🆔 ${id} registered with socket ID ${socket.id}`);
  });

  socket.on("disconnect", () => {
    for (const [id, sockId] of clients.entries()) {
      if (sockId === socket.id) {
        clients.delete(id);
        console.log(`❌ ${id} disconnected`);
      }
    }
  });
});

const PORT = process.env.PORT || 3000;
httpServer.listen(PORT, () => {
  console.log(`🚀 Server listening on port ${PORT}`);
});
