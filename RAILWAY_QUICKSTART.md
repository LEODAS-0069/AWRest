# 🚀 RAILWAY QUICK START

## ⚡ Deploy in 60 Seconds (FREE!)

### Step 1️⃣: Go to Railway
```
https://railway.app → Sign up with GitHub
```

### Step 2️⃣: Create New Project
```
Click "New Project" → Select "Deploy from GitHub repo"
→ Choose your AWRest repository → Click "Deploy"
```

### Step 3️⃣: Wait 2 Minutes
Railway builds and deploys automatically!

### Step 4️⃣: Check Your App
```
Your app is live at: https://your-project.railway.app
```

---

## ✅ What You Get (FREE)

- ✅ **$5 free credits** (1-2 months free)
- ✅ **Flask API** running 24/7
- ✅ **Databases included** (MongoDB + PostgreSQL)
- ✅ **Auto-scaling** (handles load spikes)
- ✅ **Auto-deploys** on every GitHub push
- ✅ **Free HTTPS** (SSL certificate)

---

## 🔧 Post-Deployment Setup

### 1. Add Databases
In Railway Dashboard → "Add Service":
- Click "**+**" button
- Search "**MongoDB**"
- Click "Deploy"
- Repeat for "PostgreSQL"

### 2. Set API Key (Optional - for Chatbot)
In Variables tab, add:
```
OPENAI_API_KEY=sk-your-openai-key-here
```

### 3. Test It
```bash
curl https://your-project.railway.app/health
```

---

## 📍 Access Your Services

| Service | URL |
|---------|-----|
| **Frontend & API** | `https://your-project.railway.app` |
| **Health Check** | `https://your-project.railway.app/health` |
| **Products API** | `https://your-project.railway.app/api/products` |

---

## 📊 Monitor Deployment

```bash
# Install Railway CLI (optional)
npm install -g @railway/cli

# Check status
railway status

# View logs
railway logs -f

# Get your domain
railway domain
```

---

## 💰 Cost After Free Credits

| Service | Cost |
|---------|------|
| Flask API | $5/month |
| PostgreSQL | Free (included) |
| MongoDB | Free (included) |
| **Total** | **$5+/month** |

---

## 🎯 Complete Setup Guide

For detailed instructions, see: **[RAILWAY_SETUP.md](./RAILWAY_SETUP.md)**

Topics covered:
- ✅ Step-by-step deployment
- ✅ Environment variables
- ✅ Database setup options
- ✅ Frontend deployment (Vercel/GitHub Pages)
- ✅ Monitoring & scaling
- ✅ Troubleshooting
- ✅ Auto-deploy from GitHub

---

## 🚨 Troubleshooting

**App won't start?**
```bash
railway logs -f  # Check logs for errors
```

**Database connection failed?**
```bash
# Rebuild and redeploy
railway redeploy
```

**Need help?**
- Railway Docs: https://docs.railway.app
- See: RAILWAY_SETUP.md (Troubleshooting section)

---

## 🎉 That's It!

Your Labubu Marketplace is now live and scaling automatically!

Next steps:
1. ✅ Deploy on Railway (you're here!)
2. 📊 Monitor in Railway Dashboard
3. 🚀 Push code to GitHub → Auto-deploys
4. 📈 Scale as your users grow

**Questions?** See RAILWAY_SETUP.md for comprehensive guide.

---

**Last Updated**: March 25, 2026 | **Status**: ✅ Ready for Production
