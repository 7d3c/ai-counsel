# LLM Council - Deployment Guide

This guide covers deploying LLM Council to Railway.app using Docker.

## 📋 Prerequisites

- Git repository access
- [Railway.app](https://railway.app/) account (free tier available)
- OpenRouter API key ([get one here](https://openrouter.ai/))

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
2. Add the following environment variable:
   ```
   OPENROUTER_API_KEY=your_openrouter_api_key_here
   ```
3. Click **"Add"** to save

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
| `OPENROUTER_API_KEY` | ✅ Yes | - | Your OpenRouter API key |
| `PORT` | No | 8001 | Server port (Railway sets this automatically) |
| `ALLOWED_ORIGINS` | No | `*` | CORS allowed origins (comma-separated) |

### Updating Council Models

To change the council members or chairman model:

1. Edit `backend/config.py`:
   ```python
   COUNCIL_MODELS = [
       "openai/gpt-5.1",
       "google/gemini-3-pro-preview",
       "anthropic/claude-sonnet-4.5",
       "x-ai/grok-4",
   ]

   CHAIRMAN_MODEL = "google/gemini-3-pro-preview"
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

# Run with environment variables
docker run -p 8001:8001 \
  -e OPENROUTER_API_KEY=your_api_key_here \
  llm-council
```

### Or use Docker Compose

```bash
# Create .env file
echo "OPENROUTER_API_KEY=your_api_key_here" > .env

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
- Check Railway logs: likely missing `OPENROUTER_API_KEY`
- Verify environment variables are set correctly
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
- Check OpenRouter status for model availability

## 📈 Cost Estimation

Railway.app:
- **Free tier:** $5 in credits per month
- **Hobby plan:** $5/month after credits expire
- **Usage-based** after that

OpenRouter API:
- **Varies by model** - check [OpenRouter pricing](https://openrouter.ai/models)
- **Typical cost:** $0.01-0.10 per council session (depends on models used)
- **Recommendation:** Set spending limits on OpenRouter

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
- [OpenRouter API Docs](https://openrouter.ai/docs)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)

## 💡 Next Steps

After deployment:

1. ✅ Test the application thoroughly
2. ✅ Set up monitoring and alerts
3. ✅ Configure custom domain
4. ✅ Consider adding persistent storage
5. ✅ Set up backups for conversations (if needed)
6. ✅ Monitor API costs on OpenRouter

---

**Need help?** Check the main [README.md](README.md) or [CLAUDE.md](CLAUDE.md) for development information.
