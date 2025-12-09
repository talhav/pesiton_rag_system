# Running embedding.py on Railway (Safe - No Changes to Main Service)

**This approach will NOT affect your existing API service at all.**

## Recommended: Use Railway CLI (100% Safe)

This runs the script in your Railway environment without touching your Dockerfile or service configuration.

### Steps:

1. **Install Railway CLI** (if not already installed):
   ```bash
   npm i -g @railway/cli
   ```

2. **Login and link to your project**:
   ```bash
   railway login
   railway link
   ```
   (Select your existing project when prompted)

3. **Run the embedding script**:
   ```bash
   railway run uv run python src/script/embedding.py
   ```

That's it! This will:
- ✅ Use your existing Railway environment
- ✅ Automatically load all your environment variables
- ✅ Run the script and exit
- ✅ **NOT affect your API service at all**

## Alternative: Create a Completely Separate Service

If you want to run it from the Railway dashboard:

1. In Railway Dashboard → Click **"New"** → **"Service"**
2. Select **"GitHub Repo"** → Choose your repository
3. Configure:
   - **Service Name**: `embedding-worker` (or any name)
   - **Start Command**: `uv run python src/script/embedding.py`
   - **Environment Variables**: Railway can share variables from your main service, or add manually:
     - `BEDROCK_KEY`
     - `MONGODB_URL`
4. Click **"Deploy"**

This creates a completely separate service that won't interfere with your main API.

---

**Important**: Your main API service remains completely unchanged and will continue working exactly as before.

