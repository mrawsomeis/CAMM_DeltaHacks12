const express = require('express');
const cors = require('cors');
const path = require('path');
const { createServer } = require('http');
const { Server } = require('socket.io');
const db = require('./database');
const userRoutes = require('./routes/users');
const alertRoutes = require('./routes/alerts');

const app = express();
const httpServer = createServer(app);
const PORT = process.env.PORT || 5000;

// Initialize Socket.IO
const io = new Server(httpServer, {
  cors: {
    origin: "*",
    methods: ["GET", "POST"]
  }
});

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Check if running on Vercel (serverless)
const isVercel = process.env.VERCEL || process.env.VERCEL_ENV;

// Serve uploaded face images
if (isVercel) {
  app.use('/uploads', express.static('/tmp/uploads'));
} else {
  app.use('/uploads', express.static(path.join(__dirname, 'uploads')));
}

// Initialize database
db.init();

// Socket.IO connection handling
io.of('/alerts').on('connection', (socket) => {
  console.log('✓ Client connected to alerts namespace');
  
  socket.emit('connection_response', { status: 'connected' });
  
  socket.on('acknowledge_alert', (data) => {
    console.log('Alert acknowledged:', data);
    io.of('/alerts').emit('alert_acknowledged', data);
  });
  
  socket.on('disconnect', () => {
    console.log('✗ Client disconnected from alerts namespace');
  });
});

// Export io for use in other files
global.io = io;

// API Routes
app.use('/api/users', userRoutes);
app.use('/api/alerts', alertRoutes);

// Health check
app.get('/api/health', (req, res) => {
  res.json({ 
    status: 'ok', 
    message: 'CAMM API is running', 
    environment: isVercel ? 'vercel' : 'local',
    websocket: 'enabled'
  });
});

// Only start server if not on Vercel
if (!isVercel) {
  // Serve static files from client build (local dev only)
}