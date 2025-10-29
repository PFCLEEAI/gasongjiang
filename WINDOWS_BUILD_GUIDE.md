# 🪟 Windows .exe Build Guide

## 가송장 생성기 - Windows Executable Builder

This guide will help you build the Windows .exe executable on your Windows machine.

---

## ✅ Prerequisites

### 1. **Python 3.9+**
- Download from [python.org](https://www.python.org/downloads/)
- **IMPORTANT**: Check "Add Python to PATH" during installation

### 2. **Project Files**
- Copy the entire project folder to your Windows machine
- Path example: `C:\Users\YourName\Documents\가송장_생성기`

---

## 🚀 Step-by-Step Build Instructions

### **Step 1: Open Command Prompt or PowerShell**

1. Press `Win + R` (Windows Run dialog)
2. Type: `cmd` or `powershell`
3. Press Enter

### **Step 2: Navigate to Project Folder**

```batch
cd C:\Users\YourName\Documents\가송장_생성기
```

Replace `YourName` with your Windows username.

### **Step 3: Verify Python Installation**

```batch
python --version
```

You should see: `Python 3.9.x` or higher

### **Step 4: Create Virtual Environment**

```batch
python -m venv venv
```

This creates an isolated Python environment for your project.

### **Step 5: Activate Virtual Environment**

**For Command Prompt (cmd.exe):**
```batch
venv\Scripts\activate.bat
```

**For PowerShell:**
```powershell
venv\Scripts\Activate.ps1
```

You should see `(venv)` at the beginning of your command line.

### **Step 6: Upgrade pip**

```batch
python -m pip install --upgrade pip setuptools wheel
```

### **Step 7: Install Dependencies**

```batch
pip install -r requirements.txt
```

This installs: PyQt5, pandas, openpyxl, xlrd, pydantic, etc.

### **Step 8: Install PyInstaller**

```batch
pip install pyinstaller
```

### **Step 9: Build the .exe Using Spec File**

```batch
pyinstaller gasongjiang.spec
```

**Or build without spec file (alternative):**

```batch
pyinstaller ^
    --onefile ^
    --windowed ^
    --name="가송장_생성기" ^
    --icon=resources\icon.ico ^
    main.py
```

### **Step 10: Wait for Build to Complete**

This takes **2-5 minutes** depending on your computer speed.

You'll see:
```
...
Building EXE from EXE-00.toc completed successfully.
Build complete! The results are available in: dist
```

---

## ✅ Build Successful!

Your Windows executable is ready at:

```
C:\Users\YourName\Documents\가송장_생성기\dist\가송장_생성기.exe
```

### **Test the Executable**

1. **Double-click** `dist\가송장_생성기.exe`
2. The application window should open
3. Click "📂 파일 선택" to upload an Excel file
4. Click "🔄 송장 생성" to generate tracking numbers
5. Click "💾 Excel 다운로드" to save the output

---

## 📦 Share the Executable

The `.exe` file is **self-contained** - it includes Python and all dependencies.

### **To Share with Others:**

1. Navigate to: `dist\` folder
2. Copy: `가송장_생성기.exe`
3. They can run it on any Windows machine (no Python needed!)

---

## 🐛 Troubleshooting

### **Error: "Python not found"**

```
❌ Python not found. Please install Python 3.9+ from python.org
```

**Solution:**
1. Install Python from [python.org](https://www.python.org/downloads/)
2. During installation, **CHECK** "Add Python to PATH"
3. Restart Command Prompt

### **Error: "pip: command not found"**

```
❌ 'pip' is not recognized as an internal or external command
```

**Solution:**
1. Make sure Python is in PATH
2. Or use: `python -m pip install ...` instead of `pip install ...`

### **Error: "Failed to build wheel for pandas"**

```
❌ error: Microsoft Visual C++ 14.0 is required
```

**Solution:**
1. Install [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
2. Or use pre-built wheel:
   ```batch
   pip install --only-binary :all: pandas
   ```

### **Error: "Failed to install PyInstaller"**

```
❌ ERROR: Could not find a version that satisfies the requirement
```

**Solution:**
```batch
pip install --upgrade setuptools
pip install pyinstaller==6.3.0
```

### **Application Won't Start**

**Solution 1:** Run with error output
```batch
dist\가송장_생성기.exe
```

Look for error messages.

**Solution 2:** Check log file
```batch
type error.log
```

**Solution 3:** Run in debug mode
```batch
pyinstaller --debug=all gasongjiang.spec
```

---

## 📊 Build Output Comparison

### **Size Comparison**

| Component | Size |
|-----------|------|
| Single `.exe` file | ~120-150 MB |
| With dependencies bundled | Included in .exe |
| No Python installation needed | ✅ Yes |
| Portable to other Windows PCs | ✅ Yes |

### **Build Time**

- First build: 3-5 minutes
- Subsequent builds: 2-3 minutes
- Depends on PC speed and dependencies

---

## 🎯 Quick Command Reference

**Full Build from Scratch:**

```batch
REM 1. Navigate to project
cd C:\Users\YourName\Documents\가송장_생성기

REM 2. Create venv
python -m venv venv

REM 3. Activate venv (Command Prompt)
venv\Scripts\activate.bat

REM 4. Install dependencies
pip install -r requirements.txt
pip install pyinstaller

REM 5. Build .exe
pyinstaller gasongjiang.spec

REM 6. Done! Find at: dist\가송장_생성기.exe
```

---

## 🔗 Useful Links

- **Python Download**: https://www.python.org/downloads/
- **PyInstaller Docs**: https://pyinstaller.org/
- **PyQt5 Documentation**: https://www.riverbankcomputing.com/static/Docs/PyQt5/
- **Pandas Documentation**: https://pandas.pydata.org/docs/

---

## 💡 Pro Tips

### **Tip 1: Skip Console Window**

The `--windowed` flag in the build command hides the console window. This is already set in `gasongjiang.spec`.

### **Tip 2: Add Custom Icon**

To add a custom icon:

```batch
pyinstaller ^
    --onefile ^
    --windowed ^
    --icon=C:\path\to\icon.ico ^
    main.py
```

### **Tip 3: Version Information**

To add version info, create `version.txt`:

```batch
VSVersionInfo(
  ffi=FixedFileInfo(
    mask=0x3f,
    mask_bits=0x3f,
    ver_date=(0, 0),
    serial_num=0,
    struct_ver=(1, 0, 0, 0),
    struct_date=(0, 0),
    file_version=(1, 0, 0, 0),
    prod_version=(1, 0, 0, 0),
    mask=0x3f,
    ver_flags=0x0,
    ver_os=0x4,
    ver_type=0x1,
    ver_lang=0x0,
    ver_charset=0x0,
    company_name="Your Company",
    file_description="가송장 생성기",
    file_version="1.0.0",
    internal_name="gasongjiang_generator",
    legal_copyright="© 2025",
    original_name="가송장_생성기.exe",
    product_name="가송장 생성기",
    product_version="1.0.0"
  )
)
```

### **Tip 4: Reduce File Size**

If the `.exe` is too large, use UPX compression:

```batch
pip install upx
pyinstaller gasongjiang.spec --upx-dir=C:\path\to\upx
```

---

## ✨ Next Steps

1. **Follow steps 1-10 above** on your Windows machine
2. **Test the .exe** by running it
3. **Try with a sample Excel file** to verify it works
4. **Share with others** - just copy the `.exe` file!

---

## 🆘 Still Having Issues?

1. Check that all prerequisites are installed
2. Make sure you're in the correct project directory
3. Try using Command Prompt instead of PowerShell
4. Run as Administrator (right-click → Run as Administrator)
5. Check the error messages carefully - they usually hint at the solution

---

**Good luck! Your Windows .exe is almost ready!** 🚀

