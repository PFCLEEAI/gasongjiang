; Inno Setup Script for 가송장 생성기
; This script creates a Windows installer for the application

#define MyAppName "TrackID Generator"
#define MyAppNameKR "가송장생성기"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "PFCLEEAI"
#define MyAppExeName "가송장_생성기.exe"
#define MyAppURL "https://github.com/PFCLEEAI/gasongjiang"

[Setup]
; Application identification
AppId={{E8F9A2B1-3C4D-5E6F-7A8B-9C0D1E2F3A4B}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}

; Installation directories
DefaultDirName={autopf}\TrackID_Generator
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes

; Output configuration
OutputDir=Output
OutputBaseFilename=TrackID_Generator_Setup_v{#MyAppVersion}

; Compression
Compression=lzma2/ultra64
SolidCompression=yes
LZMAUseSeparateProcess=yes
LZMANumBlockThreads=4

; Installation UI
WizardStyle=modern
WizardSizePercent=100

; License (optional - uncomment if you have a license file)
; LicenseFile=LICENSE

; README (optional - uncomment if you want to show README)
; InfoBeforeFile=README.md

; Privileges
PrivilegesRequired=admin
PrivilegesRequiredOverridesAllowed=dialog

; Visual appearance
; SetupIconFile=resources\icon.png  ; Uncomment if you add an icon
UninstallDisplayIcon={app}\{#MyAppExeName}

; Versioning
VersionInfoVersion={#MyAppVersion}
VersionInfoCompany={#MyAppPublisher}
VersionInfoDescription={#MyAppName} ({#MyAppNameKR}) Setup
VersionInfoCopyright=Copyright (C) 2025 {#MyAppPublisher}

[Languages]
Name: "korean"; MessagesFile: "compiler:Languages\Korean.isl"

[Tasks]
Name: "desktopicon"; Description: "바탕 화면에 바로가기 만들기"; GroupDescription: "추가 아이콘:"; Flags: unchecked

[Files]
; Main executable
Source: "dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion

; Resources folder (if exists)
Source: "resources\*"; DestDir: "{app}\resources"; Flags: ignoreversion recursesubdirs createallsubdirs; Check: DirExists('resources')

; Documentation
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion; Check: FileExists('README.md')

; User data folder for number_history.json
; This will be created in user's AppData folder to persist across updates

[Dirs]
; Create application data directory in user's AppData
Name: "{localappdata}\TrackID_Generator"; Permissions: users-full

[Icons]
; Start Menu shortcuts
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\README 읽기"; Filename: "{app}\README.md"; Check: FileExists(ExpandConstant('{app}\README.md'))
Name: "{group}\{#MyAppName} 제거"; Filename: "{uninstallexe}"

; Desktop shortcut (if user selected)
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
; Option to launch application after installation
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[UninstallRun]
; Clean up user data on uninstall (optional - be careful with this)
; Filename: "{cmd}"; Parameters: "/C ""rmdir /S /Q ""{localappdata}\GasongJang""" "; Flags: runhidden

[Code]
// Custom code for installation logic

// Check if application is running before uninstall
function InitializeUninstall(): Boolean;
var
  ErrorCode: Integer;
begin
  Result := True;
  // Try to close the application gracefully
  if CheckForMutexes('{#MyAppName}') then
  begin
    if MsgBox('가송장 생성기가 실행 중입니다. 프로그램을 종료하고 제거를 계속하시겠습니까?',
              mbConfirmation, MB_YESNO) = IDYES then
    begin
      // User confirmed, continue with uninstall
      Result := True;
    end
    else
    begin
      // User cancelled
      Result := False;
    end;
  end;
end;

// Custom welcome message
procedure CurPageChanged(CurPageID: Integer);
begin
  if CurPageID = wpWelcome then
  begin
    WizardForm.WelcomeLabel2.Caption :=
      '이 프로그램은 컴퓨터에 가송장 생성기를 설치합니다.' + #13#10 + #13#10 +
      '가송장 생성기는 날짜 기반의 고유한 송장번호를 생성하는 프로그램입니다.' + #13#10 +
      '- 14자리 날짜 기반 송장번호 생성' + #13#10 +
      '- Excel 파일 가져오기/내보내기' + #13#10 +
      '- 완전한 고유성 보장 (하루 81만 개 조합)' + #13#10 + #13#10 +
      '계속하려면 [다음]을 클릭하십시오.';
  end;
end;

// Installation completion message
procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    // Create a shortcut to user data folder
    CreateShellLink(
      ExpandConstant('{group}\데이터 폴더 열기.lnk'),
      ExpandConstant('{localappdata}\GasongJang'),
      '',
      '',
      '',
      '',
      0,
      SW_SHOWNORMAL
    );
  end;
end;
