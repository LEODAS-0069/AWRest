# 🚀 Railway Deployment Guide - FREE Setup

This guide walks you through deploying the Labubu Marketplace on Railway with **$5 free credits**.

## 📋 Prerequisites

- GitHub account (with AWRest repository)
- Railway account (free): [railway.app](https://railway.app)
- OpenAI API key (optional for chatbot)

---

## ⚡ Quick Start (5 Minutes)

### Step 1: Sign Up on Railway
1. Go to [railway.app](https://railway.app)
2. Click "Start Building"
3. Sign up with GitHub (authorize access)

### Step 2: Create New Project
1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Find & select your `AWRest` repository
4. Click "Deploy"

**That's it! Railway auto-deploys in ~2 minutes**

---

## 🔧 Configuration (Manual Setup)

If auto-deployment doesn't work, follow these steps:

### Step 1: Link Your Project
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Link to your project
railway link

# Set environment
railway env
```

### Step 2: Set Environment Variables
In Railway dashboard, go to **Variables** and add:

```
FLASK_ENV=production
MONGO_HOST=mongo
MONGO_PORT=27017
MONGO_DB=labubu_listings
OPENAI_API_KEY=sk-your-key-here  (OPTIONAL)
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your-key (if using real DynamoDB)
AWS_SECRET_ACCESS_KEY=your-secret (if using real DynamoDB)
DATABASE_URL=postgresql://user:pass@host/db (auto-generated)
```

### Step 3: Deploy Backend Services

Railway will automatically detect and run:
- **web**: Flask API (main service)
- **worker**: Tornado async service
- **chatbot**: Gradio interface

---

## 🗄️ Database Setup

### Option A: Railway Databases (Easiest - FREE)

Railway provides free databases:

1. **Add MongoDB**:
   - Click "Add Service"
   - Select "MongoDB"
   - Click "Deploy"
   - Copy connection string to `MONGO_URI`

2. **Add PostgreSQL**:
   - Click "Add Service"
   - Select "PostgreSQL"
   - Click "Deploy"
   - Copy connection string to `DATABASE_URL`

### Option B: Use Free Tier Services

**MongoDB**: MongoDB Atlas (free tier)
```
https://www.mongodb.com/cloud/atlas
- Sign up free
- Create cluster (free tier)
- Copy connection string
```

**PostgreSQL**: ElephantSQL (free tier)
```
https://www.elephantsql.com
- Sign up free
- Create database
- Copy connection string
```

---

## 🌐 Frontend Deployment

### Option 1: Deploy Frontend on Railway (Simplest)
```bash
# Railway auto-serves static HTML from frontend/ folder
# Your frontend will be at: https://your-app.railway.app
```

### Option 2: Deploy Frontend on Vercel (Recommended)
```bash
# 1. Push frontend to separate GitHub repo
# 2. Go to vercel.com
# 3. Import GitHub repo
# 4. Update frontend API_URL to Railway backend:

const API_URL = 'https://your-railway-app.railway.app/api';
```

### Option 3: Deploy Frontend on GitHub Pages (FREE)
```bash
# 1. Create gh-pages branch
# 2. Push frontend to gh-pages
# 3. Enable GitHub Pages in settings
# 4. Update API_URL in frontend/app.js:

const API_URL = 'https://your-railway-app.railway.app/api';
```

---

## 📊 Verify Deployment

### Check Services Running
```bash
railway status
```

### View Logs
```bash
# Flask API logs
railway logs -s web

# Tornado worker logs
railway logs -s worker

# Chatbot logs
railway logs -s chatbot
```

### Test API
```bash
# Get your Railway domain
railway domain

# Test health check
curl https://your-app.railway.app/health

# Test API
curl https://your-app.railway.app/api/products
```

---

## 💰 Cost Overview

### FREE ($0/month initially)
- **$5 free credits** covers:
  - ✅ All services for ~1-2 months
  - ✅ Databases included
  - ✅ 100GB bandwidth
  - ✅ Auto-scaling

### After Credits ($7+/month minimum)
| Service | Cost |
|---------|------|
| Flask API | $5/month |
| Tornado Worker | $5/month |
| Chatbot | $5/month |
| MongoDB | Free tier or $10+/month |
| PostgreSQL | Free tier |
| **Total** | **$15-25/month** |

---

## 🔐 Environment Variables Guide

### Required Variables
```
FLASK_ENV=production          # Production mode
MONGO_HOST=mongodb-hostname   # From Railway MongoDB
MONGO_PORT=27017
MONGO_DB=labubu_listings
DATABASE_URL=postgresql://... # From Railway PostgreSQL
```

### Optional Variables
```
OPENAI_API_KEY=sk-...         # For chatbot (free tier: $5/month API credits)
AWS_ACCESS_KEY_ID=...         # Only if using real DynamoDB
AWS_SECRET_ACCESS_KEY=...     # Only if using real DynamoDB
SECRET_KEY=your-secret-key    # Flask secret
```

---

## 🐛 Troubleshooting

### Build Fails
```bash
# Check build logs
railway logs -s web

# Clear cache and rebuild
railway redeploy
```

### Database Won't Connect
```bash
# Verify connection string
railway env

# Test connection
mongosh <MONGO_CONNECTION_STRING>
psql <DATABASE_URL>
```

### API Returns 502 (Bad Gateway)
```bash
# Check if services are running
railway status

# View logs
railway logs -f

# Restart service
railway redeploy
```

### Chatbot Not Working
```bash
# Added OPENAI_API_KEY?
railway env | grep OPENAI

# Check chatbot logs
railway logs -s chatbot
```

---

## 📈 Monitoring & Scaling

### View Metrics
In Railway dashboard:
- **Deployments** → View deployment status
- **Logs** → Real-time logs
- **Metrics** → CPU, Memory, Network usage

### Auto-Scale
Railway auto-scales based on:
- CPU usage (optional monitoring)
- Memory usage
- Request volume

Configure in project settings.

---

## 🚀 Advanced: Multiple Environments

### Deploy Staging Environment
```bash
# Create staging branch
git checkout -b staging

# Modify for staging
# Then deploy:
railway link  # Link to staging project
railway up
```

### Preview Deployments
Railway automatically creates preview deployments for pull requests!

---

## 📱 Access Your App

After deployment:

| Service | URL |
|---------|-----|
| **Frontend** | `https://your-project.railway.app` |
| **API** | `https://your-project.railway.app/api` |
| **Chatbot** | `https://your-project.railway.app:7860` |
| **Health** | `https://your-project.railway.app/health` |

---

## 🔄 Update & Redeploy

### Auto-Deploy from GitHub
Railway auto-deploys when you push to the connected branch.

```bash
# Just push your changes
git add .
git commit -m "Update features"
git push origin main

# Railway automatically redeploys!
```

### Manual Redeploy
```bash
railway redeploy
```

---

## 💡 Tips & Best Practices

1. **Use Railway's Free Tier First**
   - Test everything before upgrading
   - $5 credits = 1-2 months free

2. **Monitor Costs**
   - Set up billing alerts in Railway settings
   - Track credit usage in dashboard

3. **Use GitHub Integration**
   - Auto-deploy on push
   - Auto-rollback on failure

4. **Environment Variables**
   - Store secrets in Railway, not in code
   - Never commit `.env` files

5. **Optimize Resources**
   - Start with minimal replicas
   - Scale based on actual usage

---

## 🆘 Support

- **Railway Docs**: [docs.railway.app](https://docs.railway.app)
- **Railway Community**: [railway.app/community](https://railway.app/community)
- **Your API**: `/api/status` - Shows system health

---

## ✅ Deployment Checklist

- [ ] Created Railway account
- [ ] Connected GitHub repository
- [ ] Set environment variables
- [ ] Added MongoDB (Railway or Atlas)
- [ ] Added PostgreSQL (Railway or ElephantSQL)
- [ ] Frontend deployed (Railway or Vercel)
- [ ] Tested `/health` endpoint
- [ ] Tested `/api/products` endpoint
- [ ] Updated frontend API_URL
- [ ] Chatbot working (if OpenAI key added)
- [ ] Monitored first deployment in Railway logs

---

## 🎉 You're Done!

Your Labubu Marketplace is now live on Railway, completely free for the first 1-2 months!

**Questions?** Check the logs:
```bash
railway logs -f
```

---

**Last Updated**: March 25, 2026
