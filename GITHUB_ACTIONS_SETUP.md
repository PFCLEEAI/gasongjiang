# 🚀 GitHub Actions CI/CD Setup Guide

## Automated Windows .exe Builds with GitHub Actions

This guide shows how to set up automatic Windows .exe builds using GitHub Actions.

---

## 📋 **What This Does**

Every time you push code to GitHub:

```
You push code → GitHub Actions triggers → Build runs on Windows → .exe created → Available for download
```

**Features:**
- ✅ Automatic builds on every push
- ✅ Zero local setup needed
- ✅ Works on Windows-latest runner (always up-to-date)
- ✅ Builds both Windows .exe and macOS .app
- ✅ Artifacts stored for 30 days
- ✅ Auto-releases on version tags

---

## 🎯 **Prerequisites**

1. **GitHub Account** (free)
2. **Your project on GitHub** (public or private)
3. That's it! No secrets or special setup needed

---

## ⚙️ **Setup Steps**

### **Step 1: Create GitHub Repository**

If you don't have one already:

```bash
cd /Users/changheelee/Documents/Coding/구매대행/주문도움이
git init
git add .
git commit -m "Initial commit: 가송장 생성기 application"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/gasongjiang.git
git push -u origin main
```

Replace `YOUR_USERNAME` with your GitHub username.

### **Step 2: Verify Workflow File**

The workflow file is already in place:
```
.github/workflows/build-windows.yml
```

This file triggers on:
- ✅ Push to `main` or `develop` branches
- ✅ Pull requests to `main`
- ✅ Manual workflow trigger (via GitHub UI)

### **Step 3: Push Your Code**

```bash
git push origin main
```

The workflow will trigger automatically!

### **Step 4: Check Build Status**

**On GitHub:**
1. Go to your repository
2. Click **"Actions"** tab
3. Watch the build progress in real-time

---

## 📊 **Build Pipeline Steps**

The workflow does this automatically:

```
1. 📥 Checkout code
   └─ Gets latest source from Git

2. 🐍 Set up Python 3.11
   └─ On Windows-latest runner

3. 🔧 Create virtual environment
   └─ Isolated Python environment

4. ⬆️ Upgrade pip
   └─ Latest package manager

5. 📦 Install dependencies
   └─ From requirements-windows.txt

6. 🏗️ Build .exe with PyInstaller
   └─ Using gasongjiang.spec
   └─ Fallback if spec fails

7. ✅ Verify build output
   └─ Check file exists and size

8. 📤 Upload artifact
   └─ Available for 30 days
   └─ Downloadable from Actions

9. 🏷️ Create Release (if tagged)
   └─ Auto-create GitHub release

10. 📦 Upload to Release
    └─ .exe available for download
```

---

## 🔗 **How to Download the Built .exe**

### **Method 1: From Artifacts (for every build)**

1. Go to your GitHub repository
2. Click **"Actions"** tab
3. Click the latest successful workflow run
4. Scroll down to **"Artifacts"**
5. Click **"가송장_생성기-windows-exe"**
6. Download the `.exe` file

**Retention:** 30 days

### **Method 2: From Releases (for tagged versions)**

For tagged releases, the .exe is available in Releases:

1. Go to **"Releases"** tab
2. Find your version
3. Download the `.exe` from the release

---

## 🏷️ **Creating Release Versions**

To create an automatic release with the .exe:

```bash
# Tag your version
git tag -a v1.0.0 -m "Release version 1.0.0"

# Push tag to GitHub
git push origin v1.0.0
```

GitHub Actions will:
- ✅ Build the .exe
- ✅ Create a Release automatically
- ✅ Upload .exe to the release
- ✅ Make it downloadable for users

---

## 📈 **Workflow Triggers**

The workflow triggers on:

### **Automatic (on these events):**
- Push to `main` branch
- Push to `develop` branch
- Pull request to `main`
- Changes to source code or config

### **Manual (click button in GitHub UI):**
- Click "Run workflow" in Actions tab
- Select branch
- Click "Run"

---

## 🔍 **Monitoring Builds**

### **View Build Status**

```
Repository > Actions > build-windows > Runs
```

**Status indicators:**
- 🟢 ✅ Success
- 🔴 ❌ Failed
- 🟡 ⏳ Running
- ⚪ ⏸️ Skipped

### **View Build Logs**

Click on any workflow run to see:
- Step-by-step execution logs
- Exact commands run
- Error messages (if any)
- Build time

---

## 📝 **Example Workflow Run**

**Scenario:** You push a fix to `main` branch

```
10:15 AM - Push code to GitHub
10:16 AM - Workflow triggered automatically
10:16 AM - Windows-latest runner started
10:17 AM - Python 3.11 installed
10:18 AM - Dependencies installed
10:20 AM - PyInstaller builds .exe
10:21 AM - Verification complete ✅
10:22 AM - Artifact uploaded
10:23 AM - Email notification sent
```

**Total time:** ~8 minutes (first run), ~5 minutes (subsequent)

---

## 💾 **What Gets Built**

The workflow creates:

### **Windows .exe**
- **Location:** `dist/가송장_생성기.exe`
- **Size:** ~130 MB (standalone, includes Python)
- **Requires:** No Python on user's machine
- **Available:** Artifact download or Release

### **macOS .app** (bonus)
- **Location:** `dist/가송장_생성기.app`
- **Size:** ~7 MB
- **Available:** Artifact download

---

## 🔒 **Security & Permissions**

**GitHub Actions uses:**
- ✅ `GITHUB_TOKEN` - automatically provided
- ✅ No credentials stored
- ✅ No secrets needed (for this simple build)
- ✅ Runs on Microsoft-hosted runners
- ✅ Safe for public repositories

**To add secrets** (if needed later):
1. Go to Settings > Secrets and variables > Actions
2. Click "New repository secret"
3. Add secret name and value
4. Use in workflow with `${{ secrets.SECRET_NAME }}`

---

## 🐛 **Troubleshooting**

### **Build Failed**

1. Check the logs (click the failed run)
2. Look for error messages
3. Common issues:
   - Missing `requirements-windows.txt` (check file exists)
   - Spec file issues (check `gasongjiang.spec`)
   - Python version mismatch (check `.python-version`)

### **Artifact Not Found**

- Check if build succeeded (green checkmark)
- Artifacts only created if build passes
- Artifacts expire after 30 days

### **Release Not Created**

- Tag must start with `v` (e.g., `v1.0.0`)
- Push the tag to trigger: `git push origin v1.0.0`

---

## 📚 **File Structure**

```
가송장_생성기/
├── .github/
│   └── workflows/
│       └── build-windows.yml        ← Main workflow file
├── src/
├── tests/
├── main.py
├── requirements.txt
├── requirements-windows.txt
├── gasongjiang.spec
└── ... (other files)
```

---

## 🎯 **Typical Workflow**

**Day-to-day development:**

```
1. Make code changes locally
2. Test on your machine
3. Commit: git commit -m "fix: ..."
4. Push: git push
5. GitHub Actions builds .exe automatically
6. Download from Artifacts
7. Test the .exe
```

**Create a release:**

```
1. Make sure all tests pass
2. Tag version: git tag -a v1.0.0 -m "Release 1.0.0"
3. Push tag: git push origin v1.0.0
4. GitHub creates Release automatically
5. .exe available in Releases tab
6. Share with users!
```

---

## 📊 **Workflow Customization**

### **Build on different Python versions**

Edit `.github/workflows/build-windows.yml`:

```yaml
strategy:
  matrix:
    python-version: ['3.9', '3.10', '3.11', '3.12']
```

### **Build on schedule**

Add to workflow:

```yaml
on:
  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM UTC
```

### **Build only on specific files**

Already in the workflow:

```yaml
paths:
  - 'src/**'
  - 'main.py'
  - 'requirements.txt'
```

---

## ✅ **Success Checklist**

Before using GitHub Actions:

- [ ] Code pushed to GitHub repository
- [ ] `.github/workflows/build-windows.yml` exists
- [ ] `requirements-windows.txt` exists
- [ ] `gasongjiang.spec` exists
- [ ] Can see "Actions" tab in repository
- [ ] Workflow shows "build-windows"

---

## 🚀 **Next Steps**

1. **Push your code to GitHub** (if not already done)
   ```bash
   git push origin main
   ```

2. **Watch the build** in Actions tab

3. **Download the .exe** when complete

4. **Test the .exe** on Windows

5. **Share the link** with users (Releases tab)

---

## 📖 **Resources**

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [PyInstaller + GitHub Actions](https://github.com/marketplace/actions/pyinstaller-windows)
- [Creating Releases](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository)

---

## 💡 **Pro Tips**

1. **Auto-update badges** - Add build status badge to README.md:
   ```markdown
   ![Build Status](https://github.com/USERNAME/gasongjiang/actions/workflows/build-windows.yml/badge.svg)
   ```

2. **Slack notifications** - Add Slack alerts for build status

3. **Code signing** - Add certificate to sign .exe (requires paid action)

4. **Installers** - Use NSIS to create Windows installer (.msi)

5. **Auto-deployment** - Deploy releases to AWS S3 or similar

---

## 🎉 **You're All Set!**

Your application now builds automatically on every push!

**Benefits:**
- ✅ No manual builds needed
- ✅ Consistent, reproducible builds
- ✅ Always on latest Windows environment
- ✅ Professional release management
- ✅ Easy distribution to users

Happy building! 🚀

