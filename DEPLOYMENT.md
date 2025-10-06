# 🚀 Deployment Guide - Reason Net AI

## ✅ Deployment Status

### Frontend (Vercel)
- **Status**: ✅ **DEPLOYED**
- **Project Name**: `reason-net-ai`
- **Production URL**: https://reason-net-fad18l78u-atharva-deos-projects.vercel.app
- **Dashboard**: https://vercel.com/atharva-deos-projects/reason-net-ai
- **Framework**: Vite + React + TypeScript

### Backend (Local/Development)
- **Status**: ✅ **RUNNING**
- **Local URL**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Framework**: FastAPI + Python

---

## 🏃 Running Locally

### Backend Server

```bash
# Navigate to project root
cd /Users/atharvadeo/Desktop/PROF/Hackies/Mockathon-HackiOps

# Start backend (port 8000)
python3 -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

**Backend will be available at:**
- API: http://localhost:8000
- Swagger Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Frontend Development Server

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies (if not already done)
npm install

# Start development server (port 5174)
npm run dev
```

**Frontend will be available at:**
- Local: http://localhost:5174

---

## 🌐 Environment Configuration

### Frontend Environment Variables

The frontend uses environment variables to configure the backend API URL.

**Local Development** (`.env.local`):
```bash
VITE_API_BASE_URL=http://localhost:8000
```

**Production** (Vercel Environment Variables):
```bash
VITE_API_BASE_URL=https://your-backend-api-url.com
```

To set production environment variables:
1. Go to Vercel Dashboard: https://vercel.com/atharva-deos-projects/reason-net-ai
2. Navigate to Settings → Environment Variables
3. Add `VITE_API_BASE_URL` with your production backend URL
4. Redeploy for changes to take effect

---

## 📦 Building for Production

### Frontend Build

```bash
cd frontend
npm run build
```

Build output will be in `frontend/dist/`

---

## 🔄 Redeploying to Vercel

### Option 1: Automatic (Git Push)
If connected to GitHub:
```bash
git add .
git commit -m "Update deployment"
git push origin main
```
Vercel will automatically deploy on push.

### Option 2: Manual (Vercel CLI)
```bash
cd frontend
vercel --prod
```

### Option 3: Vercel Dashboard
1. Visit: https://vercel.com/atharva-deos-projects/reason-net-ai
2. Go to Deployments tab
3. Click "Redeploy" on the latest deployment

---

## 🔧 Vercel Configuration

### `vercel.json`
```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "framework": "vite",
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ]
}
```

This configuration:
- Builds the Vite app
- Outputs to `dist` directory
- Enables SPA routing (all routes serve index.html)

---

## 🚨 Important Notes

### CORS Configuration
If deploying backend to production, ensure CORS is configured to allow requests from Vercel domain:

```python
# backend/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5174",
        "https://reason-net-fad18l78u-atharva-deos-projects.vercel.app",
        "https://*.vercel.app"  # Allow all Vercel preview deployments
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Backend Deployment Options

For production, consider deploying backend to:
- **Railway**: Easy Python deployment
- **Render**: Free tier available
- **AWS Lambda**: Serverless option
- **Google Cloud Run**: Container-based
- **Heroku**: Traditional hosting

---

## 📊 Current Deployment Architecture

```
┌─────────────────────────────────────────────────────────┐
│  USER ACCESS                                            │
└─────────────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────────────┐
│  FRONTEND (Vercel - Production)                         │
│  https://reason-net-fad18l78u-atharva-deos-projects...  │
│  - React + TypeScript + Vite                            │
│  - Served via Vercel CDN                                │
└─────────────────────────────────────────────────────────┘
                    ↓ API Calls
┌─────────────────────────────────────────────────────────┐
│  BACKEND (Local - Development)                          │
│  http://localhost:8000                                  │
│  - FastAPI + Python                                     │
│  - ML Model + Evidence Agent                            │
└─────────────────────────────────────────────────────────┘
```

**⚠️ Note**: Currently backend is running locally. For full production deployment, backend needs to be hosted on a cloud platform.

---

## 🧪 Testing Deployment

### Test Frontend
Visit: https://reason-net-fad18l78u-atharva-deos-projects.vercel.app

### Test Backend Locally
```bash
curl http://localhost:8000/api/v1/process-url \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.bbc.com/news"}'
```

### Test Integration
1. Open frontend URL in browser
2. Navigate to Dashboard
3. Enter a URL in the URL tab
4. Click "Analyze"
5. Verify results display correctly

---

## 📱 Vercel Project Settings

**Project**: reason-net-ai  
**Owner**: atharva-deos-projects  
**Framework**: Vite  
**Node Version**: Auto-detected  
**Build Command**: `npm run build`  
**Output Directory**: `dist`  
**Install Command**: `npm install`

---

## 🎉 Next Steps

1. ✅ Frontend deployed to Vercel
2. ✅ Backend running locally
3. 🔜 Deploy backend to production service
4. 🔜 Update frontend environment variables with production backend URL
5. 🔜 Set up custom domain (optional)
6. 🔜 Configure CI/CD pipeline (optional)

---

## 🆘 Troubleshooting

### Frontend Not Loading
- Check Vercel deployment logs
- Verify build completed successfully
- Check browser console for errors

### API Calls Failing
- Verify backend is running on port 8000
- Check CORS configuration
- Verify `VITE_API_BASE_URL` environment variable

### Build Errors
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run build
```

---

**Last Updated**: October 6, 2025  
**Deployment Version**: 1.0.0  
**Status**: ✅ Production Ready
