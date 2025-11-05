; Combined Installer for 3 Applications
; - 가송장 생성기 (Python/PyQt5)
; - .NET Application 1
; - .NET Application 2

#define MyAppName "Integrated Software Suite"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "PFCLEEAI"
#define TrackIDName "TrackID_Generator"
#define TrackIDNameKR "가송장생성기"

[Setup]
; Application identification
AppId={{B1C2D3E4-F5A6-B7C8-D9E0-F1A2B3C4D5E6}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}

; Installation directories
DefaultDirName={autopf}\IntegratedSoftware
DefaultGroupName=Integrated Software Suite
DisableProgramGroupPage=yes

; Output configuration
OutputDir=Output
OutputBaseFilename=IntegratedSoftware_Setup_v{#MyAppVersion}

; Compression
Compression=lzma2/ultra64
SolidCompression=yes

; Installation UI
WizardStyle=modern
SetupIconFile=compiler:SetupClassicIcon.ico

; Privileges
PrivilegesRequired=admin
PrivilegesRequiredOverridesAllowed=dialog

; Versioning
VersionInfoVersion={#MyAppVersion}
VersionInfoCompany={#MyAppPublisher}

[Languages]
Name: "korean"; MessagesFile: "compiler:Languages\Korean.isl"

[Tasks]
Name: "desktopicon"; Description: "바탕 화면에 바로가기 만들기"; GroupDescription: "추가 아이콘:"; Flags: unchecked

[Files]
; ============================================
; APPLICATION 1: TrackID_Generator (가송장생성기) - Python
; ============================================
Source: "dist\가송장_생성기.exe"; DestDir: "{app}\TrackID_Generator"; Flags: ignoreversion
Source: "resources\*"; DestDir: "{app}\TrackID_Generator\resources"; Flags: ignoreversion recursesubdirs createallsubdirs; Check: DirExists('resources')
Source: "README.md"; DestDir: "{app}\TrackID_Generator"; Flags: ignoreversion; Check: FileExists('README.md')
Source: "TECH.md"; DestDir: "{app}\TrackID_Generator"; Flags: ignoreversion; Check: FileExists('TECH.md')
Source: "PRD.md"; DestDir: "{app}\TrackID_Generator"; Flags: ignoreversion; Check: FileExists('PRD.md')

; ============================================
; APPLICATION 2: .NET Application 1
; ============================================
; IMPORTANT: Update these paths to your actual .NET app locations
; Example structure - adjust paths as needed:
; Source: "..\DotNetApp1\bin\Release\*.exe"; DestDir: "{app}\DotNetApp1"; Flags: ignoreversion
; Source: "..\DotNetApp1\bin\Release\*.dll"; DestDir: "{app}\DotNetApp1"; Flags: ignoreversion
; Source: "..\DotNetApp1\bin\Release\*.config"; DestDir: "{app}\DotNetApp1"; Flags: ignoreversion

; ============================================
; APPLICATION 3: .NET Application 2
; ============================================
; IMPORTANT: Update these paths to your actual .NET app locations
; Example structure - adjust paths as needed:
; Source: "..\DotNetApp2\bin\Release\*.exe"; DestDir: "{app}\DotNetApp2"; Flags: ignoreversion
; Source: "..\DotNetApp2\bin\Release\*.dll"; DestDir: "{app}\DotNetApp2"; Flags: ignoreversion
; Source: "..\DotNetApp2\bin\Release\*.config"; DestDir: "{app}\DotNetApp2"; Flags: ignoreversion

[Dirs]
; Create application data directories
Name: "{localappdata}\TrackID_Generator"; Permissions: users-full
Name: "{localappdata}\DotNetApp1"; Permissions: users-full
Name: "{localappdata}\DotNetApp2"; Permissions: users-full

[Icons]
; ============================================
; START MENU SHORTCUTS
; ============================================
; TrackID_Generator (가송장생성기)
Name: "{group}\TrackID Generator\{#TrackIDNameKR}"; Filename: "{app}\TrackID_Generator\가송장_생성기.exe"
Name: "{group}\TrackID Generator\README"; Filename: "{app}\TrackID_Generator\README.md"; Check: FileExists(ExpandConstant('{app}\TrackID_Generator\README.md'))
Name: "{group}\TrackID Generator\Technical Documentation"; Filename: "{app}\TrackID_Generator\TECH.md"; Check: FileExists(ExpandConstant('{app}\TrackID_Generator\TECH.md'))

; .NET Application 1
; Name: "{group}\.NET App 1\.NET App 1"; Filename: "{app}\DotNetApp1\App1.exe"

; .NET Application 2
; Name: "{group}\.NET App 2\.NET App 2"; Filename: "{app}\DotNetApp2\App2.exe"

; Uninstaller
Name: "{group}\프로그램 제거"; Filename: "{uninstallexe}"

; ============================================
; DESKTOP SHORTCUTS (Optional)
; ============================================
Name: "{autodesktop}\{#TrackIDNameKR}"; Filename: "{app}\TrackID_Generator\가송장_생성기.exe"; Tasks: desktopicon
; Name: "{autodesktop}\.NET App 1"; Filename: "{app}\DotNetApp1\App1.exe"; Tasks: desktopicon
; Name: "{autodesktop}\.NET App 2"; Filename: "{app}\DotNetApp2\App2.exe"; Tasks: desktopicon

[Run]
; Option to launch applications after installation
Filename: "{app}\TrackID_Generator\가송장_생성기.exe"; Description: "Launch {#TrackIDNameKR}"; Flags: nowait postinstall skipifsilent unchecked
; Filename: "{app}\DotNetApp1\App1.exe"; Description: ".NET App 1 실행"; Flags: nowait postinstall skipifsilent unchecked
; Filename: "{app}\DotNetApp2\App2.exe"; Description: ".NET App 2 실행"; Flags: nowait postinstall skipifsilent unchecked

[Code]
// Custom welcome message for combined installer
procedure CurPageChanged(CurPageID: Integer);
begin
  if CurPageID = wpWelcome then
  begin
    WizardForm.WelcomeLabel2.Caption :=
      'This installer will install 3 integrated software applications:' + #13#10 + #13#10 +
      '1. TrackID Generator (가송장생성기)' + #13#10 +
      '   - Generate 14-digit date-based tracking numbers' + #13#10 +
      '   - Excel import/export functionality' + #13#10 +
      '   - Guaranteed uniqueness (810,000 daily combinations)' + #13#10 + #13#10 +
      '2. .NET Application 1' + #13#10 +
      '   - [Application 1 Description - To be added]' + #13#10 + #13#10 +
      '3. .NET Application 2' + #13#10 +
      '   - [Application 2 Description - To be added]' + #13#10 + #13#10 +
      'Click Next to continue.';
  end;
end;

// Check for .NET Framework requirement
function InitializeSetup(): Boolean;
var
  NetFrameworkInstalled: Boolean;
  ErrorCode: Integer;
begin
  // Check if .NET Framework 4.7.2 or later is installed
  // Adjust version as needed for your .NET apps
  NetFrameworkInstalled := RegKeyExists(HKLM, 'SOFTWARE\Microsoft\NET Framework Setup\NDP\v4\Full');

  if not NetFrameworkInstalled then
  begin
    if MsgBox('.NET Framework가 설치되어 있지 않습니다.' + #13#10 +
              '지금 다운로드 페이지를 여시겠습니까?',
              mbConfirmation, MB_YESNO) = IDYES then
    begin
      ShellExec('open', 'https://dotnet.microsoft.com/download/dotnet-framework',
                '', '', SW_SHOWNORMAL, ewNoWait, ErrorCode);
    end;
    Result := False;
  end
  else
  begin
    Result := True;
  end;
end;
