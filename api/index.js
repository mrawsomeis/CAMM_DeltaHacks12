// Vercel serverless function wrapper for Express app
const app = require('../server/index');

// Export the Express app as the handler
// Vercel will automatically detect this as a Node.js function
module.exports = app;
