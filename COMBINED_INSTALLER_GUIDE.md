# 통합 설치 패키지 가이드
# Combined Installer Package Guide

## 개요 (Overview)

이 가이드는 **3개의 소프트웨어를 하나의 설치 패키지로 통합**하는 방법을 설명합니다.

This guide explains how to **combine 3 software applications into ONE installation package**:
- ✅ 가송장 생성기 (Python/PyQt5) - Already prepared
- ⚙️ .NET Application 1 - Need your files
- ⚙️ .NET Application 2 - Need your files

## 🎯 What You Need to Provide

To complete the combined installer, I need information about your .NET applications:

### For Each .NET Application:

**1. Application Files Location**
```
Where are the built .exe and .dll files?
Example: C:\Projects\App1\bin\Release\
```

**2. Application Name**
```
What is the application name?
Example: "재고 관리 시스템"
```

**3. Main Executable Name**
```
What is the main .exe file name?
Example: InventorySystem.exe
```

**4. Required Files**
```
What files are needed? (Check one or provide details)
[ ] All files in Release folder (*.exe, *.dll, *.config)
[ ] Specific files only (please list)
[ ] Subfolders needed (please list)
```

**5. .NET Framework Version**
```
What .NET Framework version is required?
[ ] .NET Framework 4.5
[ ] .NET Framework 4.6
[ ] .NET Framework 4.7.2
[ ] .NET Framework 4.8
[ ] Other: _________
```

**6. Desktop Shortcut**
```
Should this app have a desktop shortcut by default?
[ ] Yes
[ ] No (optional only)
```

## 📋 Information Template

Please fill out this template for each .NET application:

### .NET Application 1:
```yaml
Name: [Application Name Here]
Main EXE: [ExeName.exe]
Location: [C:\Path\To\App1\bin\Release\]
.NET Version: [4.7.2]
Files Needed:
  - *.exe
  - *.dll
  - *.config
  - [any specific files or folders]
Desktop Shortcut: [Yes/No]
Description: [Brief description for installer]
```

### .NET Application 2:
```yaml
Name: [Application Name Here]
Main EXE: [ExeName.exe]
Location: [C:\Path\To\App2\bin\Release\]
.NET Version: [4.7.2]
Files Needed:
  - *.exe
  - *.dll
  - *.config
  - [any specific files or folders]
Desktop Shortcut: [Yes/No]
Description: [Brief description for installer]
```

## 🔧 Current Status

### ✅ Already Prepared:
- [x] 가송장 생성기 Python application built
- [x] Combined installer script template created
- [x] Documentation prepared

### ⏳ Waiting For:
- [ ] .NET Application 1 details
- [ ] .NET Application 2 details
- [ ] File paths and locations
- [ ] Application names and descriptions

## 🚀 Next Steps - After You Provide Info

Once you provide the information above, I will:

### Step 1: Update Combined Installer Script
```ini
; I will fill in these sections:
Source: "YOUR_APP_PATH\*.exe"; DestDir: "{app}\YourApp"; ...
Name: "{group}\Your App"; Filename: "{app}\YourApp\YourApp.exe"
```

### Step 2: Create Installation Structure
```
C:\Program Files\IntegratedSoftware\
├── GasongJang\
│   └── 가송장_생성기.exe (Python app)
├── DotNetApp1\
│   └── YourApp1.exe (.NET app)
└── DotNetApp2\
    └── YourApp2.exe (.NET app)
```

### Step 3: Configure Start Menu
```
Start Menu → 통합 소프트웨어\
├── 가송장 생성기\
│   ├── 가송장 생성기
│   └── README
├── [Your App 1 Name]\
│   └── [Your App 1 Name]
├── [Your App 2 Name]\
│   └── [Your App 2 Name]
└── 프로그램 제거
```

### Step 4: Build Final Installer
```
Output: 통합_소프트웨어_설치_v1.0.0.exe
Size: ~[TBD based on all 3 apps]
Installs: All 3 applications at once
```

## 💡 Example - How It Will Look

If your apps were named "재고 관리" and "주문 처리", the installer would create:

```
Installation Folder:
C:\Program Files\IntegratedSoftware\
├── GasongJang\
│   ├── 가송장_생성기.exe
│   └── resources\
├── InventoryManager\
│   ├── 재고관리.exe
│   ├── 재고관리.dll
│   └── 재고관리.exe.config
└── OrderProcessor\
    ├── 주문처리.exe
    ├── 주문처리.dll
    └── 주문처리.exe.config

Start Menu:
통합 소프트웨어\
├── 가송장 생성기\
│   └── 가송장 생성기
├── 재고 관리\
│   └── 재고 관리
├── 주문 처리\
│   └── 주문 처리
└── 프로그램 제거

Desktop (optional):
├── 가송장 생성기 (shortcut)
├── 재고 관리 (shortcut)
└── 주문 처리 (shortcut)
```

## ✅ Advantages of Combined Installer

1. **One-Click Install**: Users install all 3 apps at once
2. **Consistent Experience**: All apps in same Start Menu folder
3. **Easier Distribution**: One file to share instead of 3
4. **Professional**: Looks like integrated software suite
5. **Shared Uninstaller**: Remove all apps together
6. **Version Control**: All apps versioned together

## 🔍 Technical Details

### Technologies Supported
- ✅ Python applications (PyInstaller exe)
- ✅ .NET Framework applications (.exe + .dll)
- ✅ .NET Core applications
- ✅ Native C++ applications
- ✅ Java applications (with bundled JRE)
- ✅ Mixed (all of the above in one installer)

### Installer Features
- Automatic .NET Framework detection
- Download prompt if .NET missing
- Custom installation directory selection
- Component selection (install all or specific apps)
- Silent installation support
- Unattended installation for IT deployment
- Update support for future versions

### File Size Expectations
```
가송장 생성기: ~64 MB (Python + dependencies)
.NET App 1: ~[depends on app size]
.NET App 2: ~[depends on app size]
Total Installer: ~[sum of all apps + compression]
```

Inno Setup's LZMA2 compression typically achieves 30-50% size reduction.

## 📞 Next Action Required

**Please provide the information requested in the "Information Template" section above.**

Once you share:
1. Application names
2. File locations
3. .NET versions
4. Required files

I will:
1. Update `combined_installer.iss` with correct paths
2. Build the unified installer
3. Test installation process
4. Provide the final distributable package

## 🎓 How to Gather Information

### Finding Your .NET App Files:

**Option 1: Visual Studio**
1. Open your .NET solution
2. Right-click project → Open Folder in File Explorer
3. Navigate to `bin\Release\` or `bin\Debug\`
4. Note the full path

**Option 2: File Explorer Search**
1. Open Windows Explorer
2. Search for your .exe file name
3. Note the folder location

**Option 3: Recent Builds**
Look for folders like:
- `C:\Users\YourName\source\repos\ProjectName\bin\Release\`
- `C:\Projects\ProjectName\bin\Release\`

### Finding .NET Framework Version:

**Option 1: Visual Studio**
1. Right-click project → Properties
2. Look at "Target Framework"

**Option 2: app.exe.config file**
1. Open the .config file in Notepad
2. Look for `<supportedRuntime version="v4.0"` or similar

---

**Ready to proceed?** Share the .NET application details and I'll complete the combined installer! 🚀
