# Fixing Vercel Runtime Error

## Error: "Function Runtimes must have a valid version"

This error occurs when Vercel tries to parse an invalid runtime specification. Here's what has been fixed:

### Changes Made:
1. ✅ Removed any runtime specifications from `vercel.json`
2. ✅ Added Node.js version in root `package.json` under `engines`
3. ✅ Simplified `vercel.json` to minimal configuration
4. ✅ Added `vercel-build` script to `client/package.json`

### Current Configuration:

**vercel.json** - Minimal configuration, no runtime specs:
```json
{
  "buildCommand": "cd client && npm install && npm run build",
  "outputDirectory": "client/dist",
  "rewrites": [
    {
      "source": "/api/(.*)",
      "destination": "/api/index.js"
    }
  ]
}
```

**package.json** - Node.js version specified:
```json
{
  "engines": {
    "node": "18.x"
  }
}
```

## If Error Persists:

### Check Vercel Dashboard Settings:

1. **Go to your Vercel project settings**
2. **Check "Functions" section:**
   - Make sure there's NO runtime specification set manually
   - Remove any runtime overrides if present

3. **Check "General" settings:**
   - Framework Preset: Should be "Other" or "Vite" 
   - Node.js Version: Should match `package.json` engines (18.x)
   - Build Command: Can be left empty (uses vercel.json)
   - Output Directory: Can be left empty (uses vercel.json)

4. **Delete and Redeploy:**
   - Sometimes cached configurations cause issues
   - Try deleting the deployment and creating a fresh one

### Alternative: Use Vercel CLI to Deploy

```bash
npm i -g vercel
vercel
```

This will guide you through deployment and can help identify configuration issues.

### Verify API Function:

The `api/index.js` file should simply export the Express app:
```javascript
const app = require('../server/index');
module.exports = app;
```

Vercel will automatically detect this as a Node.js function since:
- It's in the `api/` directory
- It uses CommonJS (`require`, `module.exports`)
- Root `package.json` has Node.js dependencies

### Last Resort:

If the error still persists, try creating a fresh Vercel project:
1. Delete the current project in Vercel dashboard
2. Import repository again
3. Let Vercel auto-detect settings
4. It should work with the current `vercel.json` configuration
