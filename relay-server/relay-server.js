const express = require('express');
const http = require('http');
const { Server } = require('socket.io');

const app = express();
app.use(express.json());

const server = http.createServer(app);
const io = new Server(server);

let piSocket = null;

io.on('connection', (socket) => {
    console.log('WebSocket connected');

    socket.on('identify', (role) => {
        if (role === 'pi') {
            piSocket = socket;
            console.log('Pi connected');
        }
    });

    socket.on('disconnect', () => {
        if (socket === piSocket) {
            piSocket = null;
            console.log('Pi disconnected');
        }
    });
});

app.post('/wake', (req, res) => {
    const { mac } = req.body;
    if (!mac) return res.status(400).send('MAC address required');
    if (!piSocket) return res.status(500).send('Pi not connected');

    piSocket.emit('wake', mac);
    res.send('WOL command sent');
});

server.listen(3000, () => {
    console.log('Relay server listening on port 3000');
});