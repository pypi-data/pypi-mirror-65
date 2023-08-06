[Setup]
AppName = Acheron
AppID = Suprock Tech Acheron
AppVersion = {#VERSION}
AppVerName = Acheron {#VERSION}
AppPublisher = Suprock Tech
AppPublisherURL = http://suprocktech.com/
CloseApplications = force
DefaultDirName = {autopf}\Acheron
DefaultGroupName = Acheron
DisableProgramGroupPage = yes
Compression = lzma2
SolidCompression = yes
OutputBaseFilename = Acheron 32-bit Setup
WizardImageFile=compiler:WizModernImage-IS.bmp
WizardSmallImageFile=compiler:WizModernSmallImage-IS.bmp
SetupIconFile=acheron.ico

; Win Vista
MinVersion = 6.0

; This installation requires admin priviledges. This is needed to install
; drivers on windows vista and later.
PrivilegesRequired = admin

[InstallDelete]
; Remove library files from the last installation; this is the easiest way to allow deletions
Type: filesandordirs; Name: "{app}\lib"

[Files]
Source: "*"; DestDir: "{app}"; Excludes: "\*.iss,\*.ico,\Output,lib\hyperborea\7zip_*,lib\asphodel\lib*"; Flags: recursesubdirs
Source: "lib\hyperborea\7zip_32bit\*"; DestDir: "{app}\lib\hyperborea\7zip_32bit"
Source: "lib\asphodel\lib32\*.dll"; DestDir: "{app}\lib\asphodel\lib32"

[Run]
Filename: "{app}\acheron.exe"; Description: "Launch Acheron"; Flags: postinstall nowait

[Icons]
Name: "{group}\Acheron (32-bit)"; Filename: "{app}\acheron.exe";

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
