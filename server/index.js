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

// Serve uploaded face images
app.use('/uploads', express.static(path.join(__dirname, 'uploads')));

// Serve static files from client build
app.use(express.static(path.join(__dirname, '../client/dist')));

// Initialize database
db.init();

// API Routes
app.use('/api/users', userRoutes);
app.use('/api/alerts', alertRoutes);

// Health check
app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', message: 'CAMM API is running' });
});

// Serve React app for all other routes
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, '../client/dist/index.html'));
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
