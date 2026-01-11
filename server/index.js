const express = require('express');
const cors = require('cors');
const path = require('path');
const db = require('./database');
const userRoutes = require('./routes/users');
const alertRoutes = require('./routes/alerts');

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Check if running on Vercel (serverless)
const isVercel = process.env.VERCEL || process.env.VERCEL_ENV;

// Serve uploaded face images
if (isVercel) {
  // On Vercel, serve files from /tmp (they're ephemeral but available during request)
  app.use('/uploads', express.static('/tmp/uploads'));
} else {
  // Local development
  app.use('/uploads', express.static(path.join(__dirname, 'uploads')));
}

// Initialize database
db.init();

// API Routes
// When deployed on Vercel, requests come to /api/users, /api/alerts, etc.
// The Express app should handle these paths as-is
app.use('/api/users', userRoutes);
app.use('/api/alerts', alertRoutes);

// Health check
app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', message: 'CAMM API is running', environment: isVercel ? 'vercel' : 'local' });
});

// Only start server if not on Vercel (Vercel uses serverless functions)
if (!isVercel) {
  // Serve static files from client build (local dev only)
  app.use(express.static(path.join(__dirname, '../client/dist')));
  
  // Serve React app for all other routes (local dev only)
  app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, '../client/dist/index.html'));
  });

  app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
  });
}

// Export for Vercel serverless function
module.exports = app;

// Your existing imports...
const express = require('express');
// ... other imports

// ADD THESE NEW IMPORTS
const { createServer } = require('http');
const { Server } = require('socket.io');

const httpServer = createServer(app);

// Initialize Socket.IO
const io = new Server(httpServer, {
  cors: {
    origin: "*", // In production, specify your React app URL
    methods: ["GET", "POST"]
  }
});

// Your existing middleware and routes...
app.use(express.json());
// ... other middleware

// Socket.IO connection handling
io.of('/alerts').on('connection', (socket) => {
  console.log('Client connected to alerts namespace');
  
  socket.emit('connection_response', { status: 'connected' });
  
  socket.on('acknowledge_alert', (data) => {
    console.log('Alert acknowledged:', data);
    io.of('/alerts').emit('alert_acknowledged', data);
  });
  
  socket.on('disconnect', () => {
    console.log('Client disconnected from alerts namespace');
  });
});

// Export io for use in other files
global.io = io;

// Your existing routes
const alertsRouter = require('./routes/alerts');
const usersRouter = require('./routes/users');
// ... other routes

app.use('/api/alerts', alertsRouter);
app.use('/api/users', usersRouter);
// ... other route uses

// Change this at the bottom:
// FROM: app.listen(PORT, ...)
// TO:
httpServer.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});


