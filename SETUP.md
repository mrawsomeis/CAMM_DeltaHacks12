# CAMM Setup Instructions

## Quick Start

1. **Install all dependencies:**
   ```bash
   npm run install-all
   ```

2. **Start the development server:**
   ```bash
   npm run dev
   ```
   This will start both the frontend (port 3000) and backend (port 5000) concurrently.

3. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5000

## Individual Commands

If you prefer to run them separately:

**Terminal 1 - Backend:**
```bash
npm run server
```

**Terminal 2 - Frontend:**
```bash
npm run client
```

## First Run

On first run, the following will be automatically created:
- `server/database.sqlite` - SQLite database file
- `server/uploads/faces/` - Directory for uploaded face images

## Camera Permissions

When registering, your browser will ask for camera permissions. Please allow access for the face scanning feature to work.

## Features Implemented

✅ Homepage with program overview
✅ Consent page with detailed terms
✅ Registration form with:
   - Personal information fields
   - Medical information (optional)
   - Face capture using webcam
   - Consent verification
✅ Alert system:
   - Create emergency alerts
   - View all active alerts
   - Display user information during alerts

## Testing

1. Go to http://localhost:3000
2. Click "Get Started" to see the consent page
3. Accept consent and proceed to registration
4. Fill in your information and capture your face
5. Submit registration
6. Go to the Alerts page to create test alerts

## Troubleshooting

- **Camera not working**: Make sure you've granted camera permissions in your browser
- **Database errors**: Delete `server/database.sqlite` and restart the server
- **Port already in use**: Change the PORT in `server/index.js` or kill the process using that port
