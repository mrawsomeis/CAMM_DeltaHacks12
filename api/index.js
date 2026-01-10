// Vercel serverless function wrapper for Express app
// Import the Express app from the server directory
const app = require('../server/index');

// Export as serverless function
module.exports = app;
