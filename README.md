# CAMM - Community Assistive Monitor Model

A neighbourhood tool that helps communities support each other during emergencies, alleviating the burden on first responders and enabling residents to assist each other.

## Features

- **Opt-in Registration**: Residents can voluntarily register with facial, medical, and personal data
- **Facial Recognition**: Face scanning and storage for emergency identification
- **Consent Management**: Clear consent process for data sharing
- **Emergency Alerts**: System to send and receive emergency alerts
- **Community Response**: Share relevant information with neighbors during emergencies

## Tech Stack

- **Frontend**: React + Vite
- **Backend**: Node.js + Express
- **Database**: SQLite
- **File Upload**: Multer

## Getting Started

### Prerequisites

- Node.js (v16 or higher)
- npm or yarn

### Installation

1. Install all dependencies:
```bash
npm run install-all
```

2. Start the development server (runs both frontend and backend):
```bash
npm run dev
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000

### Individual Commands

- Start backend only: `npm run server`
- Start frontend only: `npm run client`
- Build for production: `npm run build`

## Project Structure

```
├── client/                 # React frontend
│   ├── src/
│   │   ├── pages/         # Page components
│   │   │   ├── Home.jsx   # Homepage
│   │   │   ├── Consent.jsx # Consent page
│   │   │   ├── Register.jsx # Registration with face capture
│   │   │   └── Alerts.jsx  # Alerts management
│   │   ├── App.jsx        # Main app component
│   │   └── main.jsx       # Entry point
│   └── package.json
├── server/                 # Express backend
│   ├── routes/            # API routes
│   │   ├── users.js      # User registration endpoints
│   │   └── alerts.js     # Alert endpoints
│   ├── database.js       # Database setup and queries
│   └── index.js          # Server entry point
└── package.json
```

## API Endpoints

### Users
- `POST /api/users/register` - Register a new user (with face image upload)
- `GET /api/users` - Get all registered users
- `GET /api/users/:id` - Get user by ID

### Alerts
- `POST /api/alerts` - Create a new emergency alert
- `GET /api/alerts` - Get all active alerts
- `GET /api/alerts/:id` - Get alert by ID
- `PATCH /api/alerts/:id` - Update alert status

## Usage

1. **Homepage**: Overview of the CAMM program
2. **Consent Page**: Read and accept the program terms
3. **Registration**: 
   - Fill in personal and medical information
   - Capture face image using webcam
   - Submit registration
4. **Alerts**: View and create emergency alerts

## Privacy & Consent

All participation in CAMM is voluntary. Users must explicitly consent before their data is stored or shared. Users can withdraw consent at any time.

## Development Notes

- Face images are stored in `server/uploads/faces/`
- Database is automatically created as `server/database.sqlite` on first run
- Camera access requires user permission in the browser

## License

MIT
