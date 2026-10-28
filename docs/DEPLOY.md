# AAYAM — Vercel Deployment Guide

## Deploy in 3 Steps

### Step 1 — Connect Repository
1. Go to **[vercel.com/new](https://vercel.com/new)**
2. Click **"Import Git Repository"**
3. Select **`adityasingh221204-wq/AAYAM`** from the list

### Step 2 — Configure Project
Vercel will auto-detect the settings from `vercel.json`. Verify:

| Setting | Value |
|:--------|:------|
| Framework Preset | **Other** |
| Root Directory | `./` |
| Build Command | *(leave blank)* |
| Output Directory | *(leave blank)* |
| Install Command | `pip install -r requirements.txt` |

### Step 3 — Deploy
Click **Deploy** → Your URL will be ready in ~90 seconds.

---

## Environment Variables

**None required.** AAYAM uses zero external APIs or secrets.
All computation is local and data-driven from the `data/processed/` directory.

---

## Custom Domain (Optional)

After deploying:
1. Go to **Project Settings → Domains**
2. Add your custom domain (e.g. `aayam.yourdomain.in`)
3. Update DNS: Add a CNAME record → `cname.vercel-dns.com`

---

## Vercel CLI (Alternative)

```bash
# Install
npm install -g vercel

# Login
vercel login

# Deploy from project root
vercel

# Production deploy
vercel --prod
```

---

## Troubleshooting

| Issue | Fix |
|:------|:----|
| `ModuleNotFoundError: flask` | Ensure `requirements.txt` is at root and `vercel.json` points to `api/index.py` |
| Static files 404 | All static routes go through Flask — no separate CDN config needed |
| Build timeout | Vercel's free tier allows 45s build. AAYAM builds in <10s |
| Python version | Must be Python 3.12 (set in `runtime.txt`) |
