# Vercel Deployment Guide

## Fixed Issues

### 1. **Deprecated Multer Package**
- ✅ Upgraded from `multer@1.4.5-lts.1` to `multer@2.0.0`
- This resolves the security vulnerability warnings

### 2. **Vercel Configuration**
- ✅ Created `vercel.json` with proper build and routing configuration
- ✅ Created `api/index.js` as serverless function entry point
- ✅ Updated Express app to work as serverless function

## Important Notes for Vercel Deployment

### File Storage Limitations
⚠️ **Important**: On Vercel serverless functions:
- Files are stored in `/tmp` directory which is **ephemeral**
- Files are cleared between function invocations
- Uploaded face images will **not persist** across requests

**Solutions for Production:**
1. **Use Vercel Blob Storage** (recommended for Vercel)
2. **Use AWS S3** or other cloud storage
3. **Use Cloudinary** for image storage
4. **Store images as base64** in the database (limited by size)

### Database Limitations
⚠️ **Important**: SQLite in `/tmp` on Vercel:
- Database is **ephemeral** - data is lost between deployments
- SQLite is not recommended for production serverless functions

**Solutions for Production:**
1. **Use Vercel Postgres** (recommended for Vercel)
2. **Use PlanetScale** (MySQL-compatible, serverless)
3. **Use Supabase** (PostgreSQL)
4. **Use MongoDB Atlas** or other cloud databases

## Current Setup

The application is configured to:
- Use `/tmp` directory for uploads and database on Vercel
- Serve the React frontend from `client/dist`
- Route API requests through Express serverless function

## Build Process

Vercel will automatically:
1. Run `cd client && npm install && npm run build` (from vercel.json)
2. Build the frontend to `client/dist`
3. Deploy the Express app as a serverless function from `api/index.js`

## Environment Variables

Make sure to set these in Vercel dashboard if needed:
- `NODE_ENV=production` (automatically set)
- `VERCEL=true` (automatically set on Vercel)

## Testing Locally

To test the Vercel setup locally, install Vercel CLI:
```bash
npm i -g vercel
vercel dev
```

## Next Steps for Production

1. **Replace SQLite with Vercel Postgres:**
   ```bash
   vercel postgres create
   ```

2. **Set up Vercel Blob for file storage:**
   ```bash
   vercel blob
   ```

3. **Update database.js** to use Postgres instead of SQLite

4. **Update users.js route** to upload to Vercel Blob instead of `/tmp`

## Deployment

1. Push your code to GitHub
2. Import project in Vercel dashboard
3. Configure build settings (already set in vercel.json)
4. Deploy!

The deprecation warnings should now be resolved after upgrading multer.
