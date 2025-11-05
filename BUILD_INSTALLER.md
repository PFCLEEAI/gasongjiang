# 🚀 Quick Start: Build Windows Installer

This guide shows you how to create a professional Windows installer for 가송장 생성기.

## Prerequisites

### 1. Install Inno Setup (Free)
1. Download from: https://jrsoftware.org/isdl.php
2. Download the latest stable version (e.g., `innosetup-6.x.x.exe`)
3. Run the installer and accept all defaults
4. Installation takes about 1 minute

## Steps to Create Installer

### Step 1: Rebuild EXE for Production (No Console Window)

First, we need to rebuild the exe without the console window for a cleaner user experience:

1. Open `gasongjiang.spec` file
2. Find the line `console=True,` (around line 52)
3. Change it to `console=False,`
4. Save the file

Then rebuild:
```bash
./venv/Scripts/pyinstaller.exe gasongjiang.spec
```

This will create a new `dist/가송장_생성기.exe` without the console window.

### Step 2: Open Inno Setup

1. Start Menu → Search for "Inno Setup Compiler"
2. Or navigate to: `C:\Program Files (x86)\Inno Setup 6\ISCC.exe`

### Step 3: Load the Installer Script

1. In Inno Setup: **File** → **Open**
2. Navigate to your project folder
3. Select `installer.iss`
4. Click **Open**

You should see the script loaded with Korean text.

### Step 4: Compile the Installer

**Option A: Using the GUI**
1. Click **Build** → **Compile** (or press `Ctrl+F9`)
2. Watch the compilation progress in the window
3. Wait for "Successful compile" message

**Option B: Using Command Line**
```bash
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer.iss
```

### Step 5: Find Your Installer

The installer will be created in:
```
Output/가송장_생성기_설치_v1.0.0.exe
```

This is your final distributable installer!

## What Gets Installed

When users run the installer, it will:

1. **Welcome Screen**: Shows application info
2. **Installation Directory**: Default: `C:\Program Files\GasongJang`
3. **Desktop Shortcut**: Optional (user can choose)
4. **Install Files**:
   - `가송장_생성기.exe` (main application)
   - `resources/` folder (app resources)
   - `README.md` (documentation)
5. **Start Menu Items**:
   - 가송장 생성기 (launch app)
   - README 읽기 (view docs)
   - 데이터 폴더 열기 (open data folder)
   - 가송장 생성기 제거 (uninstall)
6. **Data Folder**: Created in `%LOCALAPPDATA%\GasongJang` for number_history.json

## Testing Your Installer

### Before Distribution

1. **Test Installation**:
   ```
   - Run Output/가송장_생성기_설치_v1.0.0.exe
   - Follow installation wizard
   - Verify Start Menu shortcuts appear
   - Check desktop shortcut (if selected)
   ```

2. **Test Application**:
   ```
   - Launch from Start Menu
   - Import an Excel file
   - Generate tracking numbers
   - Export to Excel
   - Verify numbers are unique
   ```

3. **Test Uninstall**:
   ```
   - Control Panel → Programs and Features
   - Find "가송장 생성기"
   - Click Uninstall
   - Verify all files removed (except user data)
   ```

### Distribution Checklist

- [ ] Installer builds successfully
- [ ] Installation completes without errors
- [ ] Application launches correctly
- [ ] All features work (import, generate, export)
- [ ] Start Menu shortcuts work
- [ ] Desktop shortcut works (if created)
- [ ] Uninstaller removes application cleanly
- [ ] Tested on clean Windows 10/11 machine

## Distributing the Installer

### File Information
- **Filename**: `가송장_생성기_설치_v1.0.0.exe`
- **Size**: ~65-70 MB (includes all dependencies)
- **Requires**: Windows 10 or later

### Sharing Options

**Option 1: Cloud Storage**
- Upload to Google Drive, Dropbox, OneDrive
- Share download link with users
- Users download and run

**Option 2: Company Network**
- Place on network share: `\\server\software\`
- Users access from network location

**Option 3: Email** (if company allows)
- Compress with 7-Zip or WinRAR if too large
- Note: Some email providers block .exe files

**Option 4: USB Drive**
- Copy installer to USB drive
- Distribute physically

### Security Note

**Without Code Signing**, users will see:
```
"Windows protected your PC"
Unknown Publisher
```

They need to:
1. Click "More info"
2. Click "Run anyway"

This is normal for unsigned applications. For production use, consider purchasing a code signing certificate ($100-300/year) to avoid this warning.

## Troubleshooting

### Compilation Errors

**Error: "Can't find file dist/가송장_생성기.exe"**
- **Solution**: Run PyInstaller first to build the exe

**Error: "Can't find file resources/"**
- **Solution**: Make sure you're in the project root directory

**Error: "Korean text shows as ???"**
- **Solution**: Make sure Inno Setup is using Korean language support

### Installation Issues

**Issue: "Installation failed"**
- Run installer as Administrator (Right-click → Run as administrator)

**Issue: Application won't launch after install**
- Check Windows Defender didn't quarantine the exe
- Go to Windows Security → Virus & threat protection → Allow an app

**Issue: Missing DLL errors**
- Rebuild exe with PyInstaller (it should bundle all DLLs)

## Customization

### Change Application Name
Edit `installer.iss`, line 5:
```ini
#define MyAppName "가송장 생성기"
```

### Change Publisher Name
Edit `installer.iss`, line 7:
```ini
#define MyAppPublisher "Your Company Name"
```

### Add Application Icon
1. Create/obtain a 256x256 PNG icon
2. Save as `resources/icon.png`
3. Uncomment line 50 in `installer.iss`:
```ini
SetupIconFile=resources\icon.png
```

### Change Installation Directory
Edit `installer.iss`, line 18:
```ini
DefaultDirName={autopf}\YourFolderName
```

## Next Version Updates

When you release version 1.1.0:

1. **Update version in code** (if displayed in app)
2. **Update installer.iss** line 6:
   ```ini
   #define MyAppVersion "1.1.0"
   ```
3. **Rebuild exe**:
   ```bash
   ./venv/Scripts/pyinstaller.exe gasongjiang.spec
   ```
4. **Recompile installer** in Inno Setup
5. **Test thoroughly**
6. **Distribute new installer**: `가송장_생성기_설치_v1.1.0.exe`

## Silent Installation (For IT Admins)

To install silently without user interaction:
```cmd
가송장_생성기_설치_v1.0.0.exe /VERYSILENT /NORESTART
```

To uninstall silently:
```cmd
"C:\Program Files\GasongJang\unins000.exe" /VERYSILENT /NORESTART
```

## Support

For issues or questions:
- Check documentation: `README.md`
- Review technical details: `TECH.md`
- Check GitHub: https://github.com/PFCLEEAI/gasongjiang

---

**Ready to build?** Just follow Steps 1-5 above! 🎉
