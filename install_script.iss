#define MyAppName "Wiki-CLI"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "DaDevMikey"
#define MyAppURL "https://github.com/DaDevMikey/Wikipedia-command-line-interface"
#define MyAppExeName "wiki.exe"

[Setup]
AppId={{YOUR-GUID-HERE}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
LicenseFile=LICENSE
OutputBaseFilename=wiki-cli-setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern
ChangesEnvironment=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "dist\wiki\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "LICENSE"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Registry]
Root: HKLM; Subkey: "SYSTEM\CurrentControlSet\Control\Session Manager\Environment"; ValueType: expandsz; ValueName: "Path"; ValueData: "{olddata};{app}"; Check: NeedsAddPath(ExpandConstant('{app}'))

[Code]
function NeedsAddPath(Param: string): boolean;
var
  OrigPath: string;
begin
  if not RegQueryStringValue(HKEY_LOCAL_MACHINE,
    'SYSTEM\CurrentControlSet\Control\Session Manager\Environment',
    'Path', OrigPath)
  then begin
    Result := True;
    exit;
  end;
  Result := Pos(';' + Uppercase(Param) + ';', ';' + Uppercase(OrigPath) + ';') = 0;
end;

function InitializeSetup(): Boolean;
var
  ResultCode: Integer;
  PythonPath: string;
  i: Integer;
  PathParts: TStringList;
  Found: Boolean;
begin

  // 1. Check for Python in the PATH environment variable (most common)
  PythonPath := ExpandConstant('{sys}\path');

  if PythonPath <> '' then
  begin
    PathParts := TStringList.Create;
    try
      PathParts.Text := PythonPath;

      Found := False;

      for i := 0 to PathParts.Count - 1 do
      begin
        if (FileExists(PathParts[i] + '\python.exe')) or (FileExists(PathParts[i] + '\python3.exe')) or (FileExists(PathParts[i] + '\py.exe')) then
        begin
          Found := True;
          break;
        end;
      end;

      if Found then
      begin
        Result := True;
        exit;
      end;
    finally
      PathParts.Free;
    end;
  end;

  // 2. Check common registry locations (for older installers)
  if RegKeyExists(HKEY_LOCAL_MACHINE, 'SOFTWARE\Python\PythonCore\3.7') or
     RegKeyExists(HKEY_LOCAL_MACHINE, 'SOFTWARE\Python\PythonCore\3.8') or
     RegKeyExists(HKEY_LOCAL_MACHINE, 'SOFTWARE\Python\PythonCore\3.9') or
     RegKeyExists(HKEY_LOCAL_MACHINE, 'SOFTWARE\Python\PythonCore\3.10') or
     RegKeyExists(HKEY_LOCAL_MACHINE, 'SOFTWARE\Python\PythonCore\3.11') or
     RegKeyExists(HKEY_LOCAL_MACHINE, 'SOFTWARE\Python\PythonCore\3.12') or
     RegKeyExists(HKEY_LOCAL_MACHINE, 'SOFTWARE\Python\PythonCore\3.13') then
  begin
    Result := True;
    exit;
  end;

  // 3. Check for Python Launcher (py.exe)
  if FileExists(ExpandConstant('{sys}\py.exe')) then
  begin
      Result := True;
      exit;
  end;

  // 4. If none of the above are found, prompt for installation OR CONTINUE ANYWAY
  if not Result then  // Only if Python is NOT found
  begin
    if MsgBox('Python 3.7 or later is required but not installed. Would you like to install it now?', mbConfirmation, MB_YESNO) = IDYES then
    begin
      ShellExec('open', 'https://www.python.org/downloads/', '', '', SW_SHOW, ewNoWait, ResultCode);
      Result := False; // Don't continue the install if user wants to install Python
    end
    else // User chose "No" (or now "Continue Anyways")
    begin
      Log('Python not found, but continuing installation anyway.'); // Log this for debugging
      Result := True; // Continue the installation EVEN IF PYTHON IS NOT FOUND
    end;
  end;
end;