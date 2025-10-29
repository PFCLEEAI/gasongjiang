# ⚡ GitHub Actions Quick Start (5 Minutes)

## Get Automatic Windows .exe Builds in 5 Steps

---

## 🎯 **Step 1: Create GitHub Repository (2 min)**

If you don't have a GitHub account:
1. Go to https://github.com/signup
2. Create account (free!)
3. Create new repository named `gasongjiang`

If you already have one, skip this step.

---

## 📤 **Step 2: Push Your Code to GitHub (2 min)**

```bash
# Navigate to project
cd /Users/changheelee/Documents/Coding/구매대행/주문도움이

# Initialize git (if not already done)
git init
git add .
git commit -m "Initial commit: 가송장 생성기 application"

# Add GitHub remote
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/gasongjiang.git

# Push to GitHub
git push -u origin main
```

**Replace `YOUR_USERNAME` with your actual GitHub username**

---

## ⚙️ **Step 3: Enable Actions (1 min)**

1. Go to your GitHub repository
2. Click **"Actions"** tab
3. You should see **"build-windows"** workflow listed
4. That's it! It's already configured!

---

## 🚀 **Step 4: Trigger First Build (immediately)**

**Option A: Automatic (recommended)**
- The build triggers automatically when you push code
- Wait for it to complete (takes ~8 minutes first time)

**Option B: Manual**
1. Go to **Actions** tab
2. Click **"build-windows"** on the left
3. Click **"Run workflow"** button
4. Select `main` branch
5. Click **"Run workflow"**

---

## 📥 **Step 5: Download Your .exe (1 min)**

### **From Artifacts:**
1. Go to **Actions** tab
2. Click the latest successful workflow run
3. Scroll to **"Artifacts"** section
4. Click **"가송장_생성기-windows-exe"**
5. Download the `.exe` file

**Done! Your Windows executable is ready!** 🎉

---

## 📋 **What Happens Automatically**

```
You push code
    ↓
GitHub detects push
    ↓
Windows-latest runner starts
    ↓
Python 3.11 installed
    ↓
Dependencies installed (~2 min)
    ↓
PyInstaller builds .exe (~3 min)
    ↓
Artifact created
    ↓
Email notification sent
    ↓
Available for download!
```

**Total time:** ~8 minutes (first run), ~5 minutes (subsequent)

---

## 🎁 **Bonus: Auto-Create Releases**

Create a version release that users can download:

```bash
# Tag your version
git tag -a v1.0.0 -m "Release version 1.0.0"

# Push tag
git push origin v1.0.0
```

**GitHub Actions will automatically:**
- ✅ Create a Release page
- ✅ Upload .exe to the release
- ✅ Make it available for download

Users can then download from **Releases** tab!

---

## ✅ **That's It!**

Your application now builds automatically on every push!

**Key features:**
- ✅ Zero local setup
- ✅ Always uses latest Windows environment
- ✅ Professional, reproducible builds
- ✅ Easy distribution to users

---

## 🔗 **Quick Links**

- **View builds:** `https://github.com/YOUR_USERNAME/gasongjiang/actions`
- **Download .exe:** Actions > Latest run > Artifacts
- **View releases:** `https://github.com/YOUR_USERNAME/gasongjiang/releases`

---

## 📝 **Example: Complete Workflow**

```bash
# 1. Make a code change
nano src/core/tracking_generator.py

# 2. Commit and push
git add .
git commit -m "fix: improve tracking number generation"
git push

# 3. Wait ~5-8 minutes for build to complete

# 4. Download .exe from Actions > Artifacts

# 5. Test on Windows

# 6. When happy, create release
git tag -a v1.0.1 -m "Bugfix release"
git push origin v1.0.1

# 7. Users download from Releases tab!
```

---

## 🆘 **Troubleshooting**

### "Build Failed"
- Check Actions log for error message
- Usually config file issue
- Contact support if needed

### "No Artifacts"
- Build must succeed (green checkmark)
- Check the workflow logs

### "Can't push to GitHub"
- Did you do `git remote add origin ...`?
- Check username/repository name is correct

---

## 🎓 **Want to Learn More?**

Read: `GITHUB_ACTIONS_SETUP.md` (full documentation)

---

**🚀 You're ready! Push your code and watch the magic happen!**
