# Deploying the Barber Site to Vercel

This site is a static HTML file ready to deploy to Vercel. Follow the steps below.

---

## Option A: Deploy via Vercel Dashboard (No CLI needed — easiest)

1. Go to https://vercel.com and sign in (or create a free account).
2. Click "Add New Project" on your dashboard.
3. Choose "Browse" or drag-and-drop the folder:
   `C:\Users\KyeronBradley\Desktop\Kyeron\barber-site`
4. Vercel will detect it as a static site automatically.
5. Click "Deploy". Your site will be live in under a minute with a `.vercel.app` URL.

---

## Option B: Deploy via Vercel CLI

### Step 1 — Install Node.js (if not already installed)
Download and install from: https://nodejs.org (LTS version recommended)

### Step 2 — Install the Vercel CLI
Open a terminal (PowerShell or Command Prompt) and run:
```
npm install -g vercel
```

### Step 3 — Log in to Vercel
```
vercel login
```
Follow the prompts to authenticate via browser or email.

### Step 4 — Deploy the site
```
cd "C:\Users\KyeronBradley\Desktop\Kyeron\barber-site"
vercel --yes --prod
```

- `--yes` accepts all default prompts automatically.
- `--prod` deploys directly to your production URL.

### Step 5 — Get your live URL
After deployment completes, the CLI will output a URL like:
```
https://barber-site-xxxx.vercel.app
```
Visit it to confirm the site is live.

---

## Files in this folder

| File          | Purpose                                      |
|---------------|----------------------------------------------|
| `index.html`  | The barber website (33,945 bytes)            |
| `vercel.json` | Vercel configuration for static hosting      |
| `DEPLOY.md`   | This deployment guide                        |

---

## Connecting a Custom Domain (Optional)

1. In the Vercel dashboard, open your project.
2. Go to Settings > Domains.
3. Add your domain (e.g., `yourbarbershop.com`).
4. Update your domain's DNS records as instructed by Vercel.
