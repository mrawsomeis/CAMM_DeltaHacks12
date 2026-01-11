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
