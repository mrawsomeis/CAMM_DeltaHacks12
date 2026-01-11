const express = require('express');
const db = require('../database');
const router = express.Router();

// Create a new alert
router.post('/', async (req, res) => {
  try {
    const {
      userId,
      alertType,
      location,
      message
    } = req.body;

    // Validate required fields
    if (!userId || !alertType) {
      return res.status(400).json({ 
        error: 'Missing required fields: userId and alertType are required' 
      });
    }

    // Verify user exists and has given consent
    const user = await db.get(
      'SELECT id, full_name FROM users WHERE id = ? AND consent_given = 1',
      [userId]
    );

    if (!user) {
      return res.status(404).json({ 
        error: 'User not found or has not given consent' 
      });
    }

    // Create alert
    const result = await db.run(
      `INSERT INTO alerts (user_id, alert_type, location, message, status)
       VALUES (?, ?, ?, ?, 'active')`,
      [userId, alertType, location || null, message || null]
    );

    // Get alert details with user info
    const alert = await db.get(
      `SELECT a.*, u.full_name, u.email, u.phone, u.address, u.medical_info, u.emergency_contact
       FROM alerts a
       JOIN users u ON a.user_id = u.id
       WHERE a.id = ?`,
      [result.id]
    );

    res.status(201).json({
      message: 'Alert created successfully',
      alert: alert
    });
  } catch (error) {
    console.error('Alert creation error:', error);
    res.status(500).json({ error: 'Failed to create alert', details: error.message });
  }
});

// Get all active alerts
router.get('/', async (req, res) => {
  try {
    const alerts = await db.query(
      `SELECT a.*, u.full_name, u.email, u.phone, u.address, u.medical_info, u.emergency_contact
       FROM alerts a
       JOIN users u ON a.user_id = u.id
       WHERE a.status = 'active'
       ORDER BY a.created_at DESC`
    );
    res.json(alerts);
  } catch (error) {
    console.error('Error fetching alerts:', error);
    res.status(500).json({ error: 'Failed to fetch alerts' });
  }
});

// Get alert by ID
router.get('/:id', async (req, res) => {
  try {
    const alert = await db.get(
      `SELECT a.*, u.full_name, u.email, u.phone, u.address, u.medical_info, u.emergency_contact
       FROM alerts a
       JOIN users u ON a.user_id = u.id
       WHERE a.id = ?`,
      [req.params.id]
    );
    
    if (!alert) {
      return res.status(404).json({ error: 'Alert not found' });
    }
    
    res.json(alert);
  } catch (error) {
    console.error('Error fetching alert:', error);
    res.status(500).json({ error: 'Failed to fetch alert' });
  }
});

// Update alert status (e.g., when responded to)
router.patch('/:id', async (req, res) => {
  try {
    const { status, respondedBy } = req.body;
    
    if (!status) {
      return res.status(400).json({ error: 'Status is required' });
    }

    const result = await db.run(
      'UPDATE alerts SET status = ?, responded_by = ? WHERE id = ?',
      [status, respondedBy || null, req.params.id]
    );

    if (result.changes === 0) {
      return res.status(404).json({ error: 'Alert not found' });
    }

    res.json({ message: 'Alert updated successfully' });
  } catch (error) {
    console.error('Error updating alert:', error);
    res.status(500).json({ error: 'Failed to update alert' });
  }
});

module.exports = router;


const express = require('express');
const AlertManager = require('../alert_manager');

// Your existing routes here...
// router.get('/', async (req, res) => { ... });
// router.post('/', async (req, res) => { ... });

// NEW: Route for Python main.py to trigger real-time alerts
router.post('/trigger', async (req, res) => {
  try {
    const { userId, alertType, location, message, aiResponse } = req.body;
    
    console.log('🚨 Alert trigger received:', alertType);
    
    // Get io from global (set in index.js)
    if (!global.io) {
      return res.status(500).json({ error: 'WebSocket not initialized' });
    }
    
    const alertManager = new AlertManager(global.io);
    
    const alert = alertManager.sendAlert(
      userId,
      alertType,
      location,
      message,
      aiResponse
    );
    
    // Optional: Also save to database
    // const db = require('../database');
    // await db.query('INSERT INTO alerts (user_id, alert_type, location, message) VALUES (?, ?, ?, ?)',
    //   [userId, alertType, location, message]);
    
    res.json({ success: true, alert });
  } catch (error) {
    console.error('❌ Error triggering alert:', error);
    res.status(500).json({ error: 'Failed to trigger alert' });
  }
});

module.exports = router;
