#!/bin/bash
# Quick Railway Setup Script

set -e

echo "🚀 Labubu Marketplace - Railway Deployment Setup"
echo ""

# Check if railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "📦 Installing Railway CLI..."
    npm install -g @railway/cli
fi

echo "🔐 Logging into Railway..."
railway login

echo ""
echo "📍 Select your project or create a new one"
echo "   (Follow the prompts to link your GitHub repository)"
echo ""

railway link

echo ""
echo "📝 Setting environment variables..."
echo ""
echo "Add these variables in Railway Dashboard → Variables:"
echo ""
echo "FLASK_ENV=production"
echo "MONGO_HOST=mongo"
echo "MONGO_PORT=27017"
echo "MONGO_DB=labubu_listings"
echo "OPENAI_API_KEY=sk-your-key-here (optional)"
echo ""

echo "🚀 Deploying to Railway..."
railway up

echo ""
echo "✅ Deployment complete!"
echo ""
echo "📊 Check deployment status:"
echo "   railway status"
echo ""
echo "📝 View logs:"
echo "   railway logs -f"
echo ""
echo "🌐 Get your domain:"
echo "   railway domain"
echo ""
echo "💡 For detailed setup guide, see: RAILWAY_SETUP.md"
