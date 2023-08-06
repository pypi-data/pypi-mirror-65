[Setup]
AppName = Mondo
AppID = Suprock Tech Mondo
AppVersion = {#VERSION}
AppVerName = Mondo {#VERSION}
AppPublisher = Suprock Tech
AppPublisherURL = http://suprocktech.com/
DefaultDirName = {autopf}\Mondo
DefaultGroupName = Mondo
DisableProgramGroupPage = yes
Compression = lzma2
SolidCompression = yes
OutputBaseFilename = Mondo 32-bit Setup
WizardImageFile=compiler:WizModernImage-IS.bmp
WizardSmallImageFile=compiler:WizModernSmallImage-IS.bmp
SetupIconFile=mondo.ico

; Win Vista
MinVersion = 6.0

; This installation requires admin priviledges. This is needed to install
; drivers on windows vista and later.
PrivilegesRequired = admin

[InstallDelete]
; Remove library files from the last installation; this is the easiest way to allow deletions
Type: filesandordirs; Name: "{app}\lib"

[Files]
Source: "*"; DestDir: "{app}"; Excludes: "\*.iss,\*.ico,\Output,lib\asphodel\lib*"; Flags: recursesubdirs
Source: "lib\asphodel\lib32\*.dll"; DestDir: "{app}\lib\asphodel\lib32"

[Run]
Filename: "{app}\mondo.exe"; Description: "Launch Mondo"; Flags: postinstall nowait

[Icons]
Name: "{group}\Mondo (32-bit)"; Filename: "{app}\mondo.exe";

[Code]
(* This deletes the installer if run with /DeleteInstaller=Yes *)
procedure CurStepChanged(CurStep: TSetupStep);
var
  strContent: String;
  intErrorCode: Integer;
  strSelf_Delete_BAT: String;
begin
  if CurStep=ssDone then
  begin
    if ExpandConstant('{param:DeleteInstaller|No}') = 'Yes' then
    begin
      strContent := ':try_delete' + #13 + #10 +
            'del "' + ExpandConstant('{srcexe}') + '"' + #13 + #10 +
            'if exist "' + ExpandConstant('{srcexe}') + '" goto try_delete' + #13 + #10 +
            'del %0';
  
      strSelf_Delete_BAT := ExtractFilePath(ExpandConstant('{tmp}')) + 'SelfDelete.bat';
      SaveStringToFile(strSelf_Delete_BAT, strContent, False);
      Exec(strSelf_Delete_BAT, '', '', SW_HIDE, ewNoWait, intErrorCode);
    end;
  end;
end;
