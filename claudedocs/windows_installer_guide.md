# Windows Installer Package Creation Guide

## Overview
This document explains how to create a professional Windows installer (.exe) for the 가송장 생성기 application.

## Prerequisites

### 1. Inno Setup (Recommended)
- **Download**: https://jrsoftware.org/isdl.php
- **Version**: 6.x or later
- **Size**: ~2MB installer
- **Why**: Free, widely used, creates small professional installers

### Alternative Tools
- **NSIS** (Nullsoft Scriptable Install System): More complex but very flexible
- **WiX Toolset**: Creates MSI files, more enterprise-focused
- **Advanced Installer**: Commercial tool with GUI

## Installation Package Components

### What Gets Packaged
```
Installer Package/
├── Application Executable (가송장_생성기.exe)
├── Resources folder (icons, assets)
├── number_history.json (uniqueness tracking)
├── README.md (user documentation)
├── License file (optional)
└── Uninstaller
```

### Installation Features
1. **Start Menu Integration**: Adds application to Start Menu
2. **Desktop Shortcut**: Optional desktop icon
3. **Uninstaller**: Proper Windows uninstall support
4. **Registry Entries**: Application registration (optional)
5. **Auto-update check** (future feature)

## Step-by-Step: Creating Installer with Inno Setup

### Step 1: Install Inno Setup
1. Download Inno Setup from https://jrsoftware.org/isdl.php
2. Run the installer
3. Accept defaults and complete installation

### Step 2: Create Inno Setup Script
The script file (`installer.iss`) defines:
- Application metadata (name, version, publisher)
- Files to include
- Installation directory
- Start menu entries
- Desktop shortcuts
- Uninstaller configuration

### Step 3: Configure Application Details
```ini
[Setup]
AppName=가송장 생성기
AppVersion=1.0.0
AppPublisher=Your Company Name
DefaultDirName={autopf}\GasongJang
DefaultGroupName=가송장 생성기
OutputBaseFilename=가송장_생성기_설치
Compression=lzma2
SolidCompression=yes
```

### Step 4: Specify Files
```ini
[Files]
Source: "dist\가송장_생성기.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "resources\*"; DestDir: "{app}\resources"; Flags: ignoreversion recursesubdirs
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion
```

### Step 5: Create Shortcuts
```ini
[Icons]
Name: "{group}\가송장 생성기"; Filename: "{app}\가송장_생성기.exe"
Name: "{autodesktop}\가송장 생성기"; Filename: "{app}\가송장_생성기.exe"
```

### Step 6: Compile Installer
1. Open Inno Setup
2. Load the `.iss` script file
3. Click "Compile" (or press Ctrl+F9)
4. Installer will be created in the `Output` folder

## Installer Features

### Installation Flow
1. **Welcome Screen**: Greets user
2. **License Agreement**: (Optional) Display license
3. **Installation Directory**: User chooses install location (default: C:\Program Files\GasongJang)
4. **Components**: User selects optional components
5. **Ready to Install**: Confirmation screen
6. **Installing**: Progress bar showing installation
7. **Finish**: Launch application option

### Post-Installation
- Application added to Start Menu
- Desktop shortcut created
- Uninstaller registered in Control Panel
- Application ready to run

## Testing Checklist

### Before Distribution
- [ ] Install on clean Windows machine
- [ ] Test all shortcuts work
- [ ] Verify application launches correctly
- [ ] Test core functionality (generate tracking numbers)
- [ ] Test Excel import/export
- [ ] Verify uninstaller removes all files
- [ ] Check Start Menu entries
- [ ] Test on different Windows versions (10, 11)

### Final Distribution Package
```
Release/
├── 가송장_생성기_설치.exe (Installer)
├── README.md (Installation instructions)
└── CHANGELOG.md (Version history)
```

## Distribution

### File Sharing
- **File Size**: ~65MB installer (includes all dependencies)
- **Upload to**: Google Drive, Dropbox, or company server
- **Share link** with end users

### Enterprise Distribution
- Deploy via Group Policy
- Use network share for installation
- Silent installation: `installer.exe /VERYSILENT`

## Troubleshooting

### Common Issues

**Issue**: Installer won't run
- **Solution**: Right-click → Run as Administrator

**Issue**: Application doesn't launch after install
- **Solution**: Check Windows Defender didn't quarantine exe

**Issue**: Missing DLL errors
- **Solution**: Ensure PyInstaller bundled all dependencies (already handled)

**Issue**: Installer too large
- **Solution**: Use UPX compression (already enabled in spec file)

## Version Updates

### When Releasing New Version
1. Update version number in:
   - `installer.iss` (AppVersion)
   - `main.py` (if version displayed in app)
2. Rebuild exe with PyInstaller
3. Recompile installer with Inno Setup
4. Test new installer thoroughly
5. Distribute updated installer

### Update Strategy
- **Minor updates**: Overwrite existing installation
- **Major updates**: Prompt to uninstall old version first
- **Auto-update** (future): Check for updates on launch

## Security Considerations

### Code Signing (Recommended for Production)
- Purchase code signing certificate (~$100-300/year)
- Sign exe before creating installer
- Sign installer exe itself
- **Benefit**: No Windows SmartScreen warnings

### Without Code Signing
- Users may see "Unknown Publisher" warning
- Can still install by clicking "More info" → "Run anyway"
- Not a problem for internal company use

## Next Steps

1. Install Inno Setup on your machine
2. Review the generated `installer.iss` script
3. Customize branding (app name, publisher, icon)
4. Compile installer
5. Test on a clean Windows machine
6. Distribute to users

## Resources

- **Inno Setup Documentation**: https://jrsoftware.org/ishelp/
- **Example Scripts**: Included with Inno Setup installation
- **Community Support**: https://stackoverflow.com/questions/tagged/inno-setup
