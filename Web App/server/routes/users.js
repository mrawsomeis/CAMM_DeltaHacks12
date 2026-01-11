const express = require('express');
const multer = require('multer');
const path = require('path');
const fs = require('fs');
const db = require('../database');
const router = express.Router();

// Configure multer for face image uploads
// Use /tmp for Vercel serverless (only writable directory)
const isVercel = process.env.VERCEL || process.env.VERCEL_ENV;
const uploadBaseDir = isVercel 
  ? path.join('/tmp', 'uploads', 'faces')
  : path.join(__dirname, '../uploads/faces');

const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    if (!fs.existsSync(uploadBaseDir)) {
      fs.mkdirSync(uploadBaseDir, { recursive: true });
    }
    cb(null, uploadBaseDir);
  },
  filename: (req, file, cb) => {
    const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1E9);
    cb(null, 'face-' + uniqueSuffix + path.extname(file.originalname));
  }
});

const upload = multer({ 
  storage: storage,
  limits: { fileSize: 5 * 1024 * 1024 }, // 5MB limit
  fileFilter: (req, file, cb) => {
    const allowedTypes = /jpeg|jpg|png|webp/;
    const extname = allowedTypes.test(path.extname(file.originalname).toLowerCase());
    const mimetype = allowedTypes.test(file.mimetype);
    
    if (extname && mimetype) {
      cb(null, true);
    } else {
      cb(new Error('Only image files are allowed'));
    }
  }
});

// Register new user
router.post('/register', upload.single('faceImage'), async (req, res) => {
  try {
    const {
      email,
      fullName,
      phone,
      address,
      medicalInfo,
      emergencyContact,
      consentGiven
    } = req.body;

    // Validate required fields
    if (!email || !fullName || !consentGiven || consentGiven !== 'true') {
      return res.status(400).json({ 
        error: 'Missing required fields or consent not given' 
      });
    }

    // Check if user already exists
    const existingUser = await db.get('SELECT id FROM users WHERE email = ?', [email]);
    if (existingUser) {
      return res.status(400).json({ error: 'User with this email already exists' });
    }

    // Handle face image
    let faceDataPath = null;
    if (req.file) {
      // For Vercel, we'll need to serve from /tmp or use a different approach
      // For now, store the path - in production, consider using cloud storage
      faceDataPath = isVercel 
        ? `/tmp/uploads/faces/${req.file.filename}`
        : `/uploads/faces/${req.file.filename}`;
    }

    // Insert user
    const result = await db.run(
      `INSERT INTO users 
       (email, full_name, phone, address, medical_info, emergency_contact, face_data_path, consent_given, consent_timestamp)
       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)`,
      [
        email,
        fullName,
        phone || null,
        address || null,
        medicalInfo || null,
        emergencyContact || null,
        faceDataPath,
        consentGiven === 'true' ? 1 : 0,
        new Date().toISOString()
      ]
    );

    // Log consent
    if (consentGiven === 'true') {
      await db.run(
        'INSERT INTO consent_logs (user_id, consent_type, granted) VALUES (?, ?, ?)',
        [result.id, 'program_participation', 1]
      );
    }

    res.status(201).json({
      message: 'User registered successfully',
      userId: result.id
    });
  } catch (error) {
    console.error('Registration error:', error);
    res.status(500).json({ error: 'Failed to register user', details: error.message });
  }
});

// Get all users (for community alerts)
router.get('/', async (req, res) => {
  try {
    const users = await db.query(
      `SELECT id, full_name, email, phone, address, medical_info, emergency_contact 
       FROM users 
       WHERE consent_given = 1 
       ORDER BY created_at DESC`
    );
    res.json(users);
  } catch (error) {
    console.error('Error fetching users:', error);
    res.status(500).json({ error: 'Failed to fetch users' });
  }
});

// Get user by ID
router.get('/:id', async (req, res) => {
  try {
    const user = await db.get(
      `SELECT id, full_name, email, phone, address, medical_info, emergency_contact, face_data_path
       FROM users 
       WHERE id = ? AND consent_given = 1`,
      [req.params.id]
    );
    
    if (!user) {
      return res.status(404).json({ error: 'User not found' });
    }
    
    res.json(user);
  } catch (error) {
    console.error('Error fetching user:', error);
    res.status(500).json({ error: 'Failed to fetch user' });
  }
});

module.exports = router;
