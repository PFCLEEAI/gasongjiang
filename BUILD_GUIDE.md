# 🔨 Build Guide - 가송장 생성기

This guide will help you create standalone executables for **macOS** and **Windows**.

---

## 🍎 macOS Build (.app)

### **Option 1: Use the Build Script (Easiest)**

```bash
cd /Users/changheelee/Documents/Coding/구매대행/주문도움이

# Make script executable
chmod +x build_executable.sh

# Run the build script
./build_executable.sh
```

**That's it!** The script will:
1. Create a virtual environment
2. Install all dependencies
3. Build the standalone .app
4. Output the final application in `dist/가송장_생성기.app`

### **Option 2: Manual Build**

If the script doesn't work, do this manually:

```bash
cd /Users/changheelee/Documents/Coding/구매대행/주문도움이

# 1. Create virtual environment
python3 -m venv venv

# 2. Activate it
source venv/bin/activate

# 3. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
pip install pyinstaller

# 4. Build executable
pyinstaller \
    --onefile \
    --windowed \
    --name="가송장_생성기" \
    main.py

# 5. Run (from dist folder)
./dist/가송장_생성기
```

### **After Building**

You'll find your app in:
```
dist/가송장_생성기.app
```

**To run it:**
- Double-click `dist/가송장_생성기.app` in Finder, OR
- Run from terminal: `./dist/가송장_생성기`

---

## 🪟 Windows Build (.exe)

### **On Windows Machine**

```batch
REM 1. Open Command Prompt or PowerShell
REM 2. Navigate to project folder
cd C:\Users\YourName\Documents\가송장_생성기

REM 3. Create virtual environment
python -m venv venv

REM 4. Activate it
venv\Scripts\activate

REM 5. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
pip install pyinstaller

REM 6. Build executable
pyinstaller ^
    --onefile ^
    --windowed ^
    --name="가송장_생성기" ^
    main.py

REM 7. Your .exe is ready in: dist\가송장_생성기.exe
```

### **Simpler Windows Command**

```batch
python -m pip install pyinstaller
pyinstaller --onefile --windowed --name="가송장_생성기" main.py
```

---

## 📦 Cross-Platform Build (macOS → Windows)

Unfortunately, **you cannot build a Windows .exe on macOS** directly. You need Windows for that.

**Solutions:**

### **Option 1: Use a Windows Machine**
Follow the Windows build instructions above on a Windows computer.

### **Option 2: Use Docker**
```bash
# Install Docker first, then:
docker run -v /path/to/project:/src python:3.11 /bin/bash -c "
  cd /src
  pip install -r requirements.txt pyinstaller
  pyinstaller --onefile --windowed --name='가송장_생성기' main.py
"
```

### **Option 3: Use Cloud Build Service**
Use online build services like:
- [py2exe](https://py2exe.org/)
- [Nuitka](https://nuitka.net/)
- GitHub Actions (automated builds)

---

## ✅ Verification

### **On macOS**

After building, verify the app works:

```bash
# Check if it exists
ls -la dist/가송장_생성기.app

# Try running it
./dist/가송장_생성기

# Or double-click in Finder
open dist/가송장_생성기.app
```

### **On Windows**

```batch
REM Check if executable exists
dir dist\가송장_생성기.exe

REM Run it
dist\가송장_생성기.exe
```

---

## 🐛 Troubleshooting

### **macOS: "Permission denied" error**

```bash
chmod +x dist/가송장_생성기
# or
chmod +x "dist/가송장_생성기.app/Contents/MacOS/가송장_생성기"
```

### **macOS: "Damaged application" error**

```bash
# Bypass macOS Gatekeeper
sudo xattr -rd com.apple.quarantine dist/가송장_생성기.app
```

### **macOS: Cannot open because it's not from App Store**

1. Open System Preferences
2. Security & Privacy
3. Allow the app to run

### **Windows: PyInstaller not found**

```batch
pip install --upgrade pip
pip install pyinstaller
```

### **Build is very slow**

This is normal - PyInstaller bundles everything. First build takes 3-5 minutes.

---

## 📊 Build Output

### **macOS**
```
dist/
└── 가송장_생성기.app/
    ├── Contents/
    │   ├── MacOS/가송장_생성기    (executable)
    │   ├── Resources/
    │   ├── Info.plist
    │   └── ...
```

**Size:** ~150-200 MB (includes Python + all libraries)

### **Windows**
```
dist/
└── 가송장_생성기.exe  (single executable)
```

**Size:** ~100-150 MB

---

## 🚀 Distribution

### **Share with Others**

**macOS Users:**
```bash
# Create zip
zip -r 가송장_생성기.zip dist/가송장_생성기.app

# They can extract and double-click to run
```

**Windows Users:**
```batch
REM Copy the .exe file
copy dist\가송장_생성기.exe 가송장_생성기.exe

REM Share 가송장_생성기.exe (single file, easy to distribute!)
```

---

## 🎯 Quick Reference

| Platform | Command | Output |
|----------|---------|--------|
| **macOS** | `./build_executable.sh` | `dist/가송장_생성기.app` |
| **Windows** | `pyinstaller --onefile --windowed main.py` | `dist/가송장_생성기.exe` |

---

## 💡 Pro Tips

1. **Add Icon** (optional):
   ```bash
   # macOS
   pyinstaller --onefile --windowed --icon=myicon.icns main.py

   # Windows
   pyinstaller --onefile --windowed --icon=myicon.ico main.py
   ```

2. **Hide Console** (Windows only):
   ```batch
   pyinstaller --onefile --windowed --noconsole main.py
   ```

3. **Add Version Info**:
   Create a `version.txt` file with build info

4. **Code Signing** (macOS):
   ```bash
   codesign -s - dist/가송장_생성기.app
   ```

---

## ❓ FAQ

**Q: Can I build Windows .exe on macOS?**
A: No, you need Windows. Use Docker or remote build service.

**Q: Can I build macOS .app on Windows?**
A: No, you need macOS. Use remote CI/CD service.

**Q: How do I update the app?**
A: Rebuild with new source code, replace old executable.

**Q: Can I distribute the .app/.exe commercially?**
A: Yes! The MIT license allows commercial use.

**Q: Will it run without Python installed?**
A: Yes! PyInstaller bundles everything needed.

---

**Ready to build?** Run:

### **macOS**
```bash
chmod +x build_executable.sh && ./build_executable.sh
```

### **Windows**
```batch
pip install pyinstaller && pyinstaller --onefile --windowed main.py
```

Your executable will be in `dist/` folder! 🎉
