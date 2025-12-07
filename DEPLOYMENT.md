# LLM Council - Deployment Guide

This guide covers deploying LLM Council to Railway.app using Docker.

## 📋 Prerequisites

- Git repository access
- [Railway.app](https://railway.app/) account (free tier available)
- API keys for the LLM providers you want to use:
  - [Anthropic Claude](https://console.anthropic.com/)
  - [Google Gemini](https://aistudio.google.com/app/apikey)
  - [OpenAI](https://platform.openai.com/api-keys)
  - [xAI Grok](https://console.x.ai/)

## 🚀 Railway.app Deployment

### Step 1: Prepare Your Repository

Ensure all Docker files are committed:
```bash
git add Dockerfile docker-compose.yml .dockerignore railway.toml
git commit -m "Add Docker and Railway configuration"
git push
```

### Step 2: Create Railway Project

1. Go to [Railway.app](https://railway.app/) and sign in
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Choose your `ai-counsel` repository
5. Railway will automatically detect the Dockerfile

### Step 3: Configure Environment Variables

In your Railway project dashboard:

1. Go to **"Variables"** tab
2. Add the API keys for the models you want to use:
   ```
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   GOOGLE_API_KEY=your_google_api_key_here
   OPENAI_API_KEY=your_openai_api_key_here
   XAI_API_KEY=your_xai_api_key_here
   ```
   Note: You don't need all keys, only for the models you configured in `backend/config.py`
3. Click **"Add"** for each variable

### Step 4: Deploy

Railway will automatically:
- Build the Docker image
- Deploy the container
- Assign a public URL (e.g., `your-app.up.railway.app`)

### Step 5: Access Your Application

Once deployed:
- Click on the deployed service
- Find your public URL (e.g., `https://your-app.up.railway.app`)
- Open it in your browser
- Your LLM Council is now live! 🎉

## 🔧 Configuration

### Custom Domain (Optional)

1. In Railway dashboard, go to **"Settings"**
2. Scroll to **"Domains"**
3. Click **"Add Domain"**
4. Follow instructions to configure DNS

### Environment Variables

Available environment variables:

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `ANTHROPIC_API_KEY` | Conditional | - | Anthropic Claude API key (required if using Claude models) |
| `GOOGLE_API_KEY` | Conditional | - | Google Gemini API key (required if using Gemini models) |
| `OPENAI_API_KEY` | Conditional | - | OpenAI API key (required if using GPT models) |
| `XAI_API_KEY` | Conditional | - | xAI Grok API key (required if using Grok models) |
| `PORT` | No | 8001 | Server port (Railway sets this automatically) |
| `ALLOWED_ORIGINS` | No | `*` | CORS allowed origins (comma-separated) |

### Updating Council Models

To change the council members or chairman model:

1. Edit `backend/config.py`:
   ```python
   # Available models:
   # Claude: claude-sonnet-4.5, claude-sonnet-4, claude-opus-4
   # Gemini: gemini-2.0-flash, gemini-2.5-flash, gemini-3-pro
   # OpenAI: gpt-4o, gpt-4o-mini, gpt-5.1, o1, o1-mini
   # Grok: grok-beta, grok-4

   COUNCIL_MODELS = [
       "gpt-4o",
       "gemini-2.0-flash",
       "claude-sonnet-4.5",
       "grok-beta",
   ]

   CHAIRMAN_MODEL = "gemini-2.0-flash"
   ```

2. Commit and push:
   ```bash
   git add backend/config.py
   git commit -m "Update council models"
   git push
   ```

3. Railway will automatically redeploy

## 🧪 Local Testing with Docker

Before deploying, test locally using Docker:

### Build and Run

```bash
# Build the Docker image
docker build -t llm-council .

# Run with environment variables (add only the keys you need)
docker run -p 8001:8001 \
  -e ANTHROPIC_API_KEY=your_anthropic_key \
  -e GOOGLE_API_KEY=your_google_key \
  -e OPENAI_API_KEY=your_openai_key \
  -e XAI_API_KEY=your_xai_key \
  llm-council
```

### Or use Docker Compose

```bash
# Create .env file with your API keys
cat > .env <<EOF
ANTHROPIC_API_KEY=your_anthropic_key
GOOGLE_API_KEY=your_google_key
OPENAI_API_KEY=your_openai_key
XAI_API_KEY=your_xai_key
EOF

# Start the application
docker compose up

# Stop the application
docker compose down
```

The app will be available at `http://localhost:8001`

## 📊 Monitoring

### View Logs on Railway

1. Go to your Railway project
2. Click on the deployed service
3. Select **"Deployments"** tab
4. Click on the active deployment
5. View real-time logs

### Health Check

Railway uses the `/health` endpoint to check if the service is running:
```bash
curl https://your-app.up.railway.app/health
```

Expected response:
```json
{"status": "healthy", "service": "LLM Council API"}
```

## 💾 Data Persistence

**Important:** Railway's file system is ephemeral. Conversations are stored in-memory and will be lost on restart.

For persistent storage, consider:

1. **Railway PostgreSQL Plugin** (requires code changes to use database)
2. **Railway Volume Mounting** (attach persistent volume)
3. **External Storage** (S3, etc.)

Current implementation stores conversations in `data/conversations/` which will reset on deployment.

## 🔒 Security Best Practices

1. **Never commit `.env` files** - Already in `.gitignore`
2. **Use Railway's environment variables** for all secrets
3. **Restrict CORS** in production if needed:
   ```
   ALLOWED_ORIGINS=https://yourdomain.com
   ```
4. **Monitor API usage** on OpenRouter dashboard
5. **Set spending limits** on OpenRouter to avoid unexpected charges

## 🐛 Troubleshooting

### Build Fails

**Issue:** Docker build fails on Railway

**Solution:**
- Check Railway logs for specific error
- Ensure all dependencies are in `pyproject.toml` and `package.json`
- Try building locally first: `docker build -t test .`

### App Crashes After Deployment

**Issue:** App starts but crashes immediately

**Solution:**
- Check Railway logs: likely missing API keys
- Verify environment variables are set correctly (at least one API key for each model you're using)
- Check health endpoint: `/health`

### CORS Errors

**Issue:** Frontend can't connect to backend

**Solution:**
- In production, frontend and backend are same origin (no CORS needed)
- If using custom setup, add your domain to `ALLOWED_ORIGINS`

### Slow Response Times

**Issue:** Council responses are very slow

**Solution:**
- This is expected - the app makes multiple API calls to different models
- Consider reducing number of council members in `backend/config.py`
- Check individual API provider status pages for model availability

## 📈 Cost Estimation

**Railway.app:**
- **Free tier:** $5 in credits per month
- **Hobby plan:** $5/month after credits expire
- **Usage-based** after that

**API Costs:**
Costs vary significantly by provider and model. Approximate pricing per 1M tokens:

- **Claude (Anthropic):**
  - Claude Sonnet 4.5: $3 input / $15 output
  - Claude Opus 4: $15 input / $75 output

- **Gemini (Google):**
  - Gemini 2.0 Flash: $0.075 input / $0.30 output (free tier available!)
  - Gemini 3 Pro: $1.25 input / $5 output

- **OpenAI:**
  - GPT-4o: $2.50 input / $10 output
  - GPT-5.1: Pricing TBD

- **Grok (xAI):**
  - Grok Beta: Pricing varies, check [xAI pricing](https://x.ai/pricing)

**Typical cost per council session:** $0.02-0.20 depending on models used and response length

**Recommendation:** Start with Gemini 2.0 Flash (free tier) to test, then add other models as needed

## 🔄 CI/CD

Railway automatically redeploys when you push to your repository:

```bash
# Make changes
git add .
git commit -m "Your changes"
git push

# Railway will automatically:
# 1. Pull latest code
# 2. Build Docker image
# 3. Deploy new container
# 4. Health check
# 5. Switch traffic to new deployment
```

## 📚 Additional Resources

- [Railway Documentation](https://docs.railway.app/)
- [Docker Documentation](https://docs.docker.com/)
- [Anthropic Claude API Docs](https://docs.anthropic.com/)
- [Google Gemini API Docs](https://ai.google.dev/docs)
- [OpenAI API Docs](https://platform.openai.com/docs)
- [xAI Grok API Docs](https://docs.x.ai/)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)

## 💡 Next Steps

After deployment:

1. ✅ Test the application thoroughly
2. ✅ Set up monitoring and alerts
3. ✅ Configure custom domain
4. ✅ Consider adding persistent storage
5. ✅ Set up backups for conversations (if needed)
6. ✅ Monitor API costs on each provider's dashboard

---

**Need help?** Check the main [README.md](README.md) or [CLAUDE.md](CLAUDE.md) for development information.
