; =============================================================================
; Inno Setup 安装脚本
; 电脑鼠迷宫上位机 v3.4.2
; 开发者：石殷睿（苏州大学电子信息学院）
; 用途：电子系统课程设计
; 联系方式：yinrui_shi@163.com
; 更新日期：2025
; =============================================================================

#define MyAppName "电脑鼠迷宫上位机"
#define MyAppVersion "3.4.2"
#define MyAppVersionFull "3.4.2.0"
#define MyAppPublisher "石殷睿"
#define MyAppURL "https://www.quartz.xin"
#define MyAppExeName "电脑鼠上位机.exe"
#define MyDeveloper "苏州大学 | 石殷睿"
#define MyProject "【2025电子系统设计】课程设计"
#define MySchool "苏州大学电子信息学院"
#define MyAppEmail "yinrui_shi@163.com"
#define MyAppDescription "电脑鼠迷宫上位机 - 实时通信、轨迹可视化和迷宫墙体自动绘制"

[Setup]
; 注意: AppId的值为单独标识这个应用程序
; 不要为其他安装程序使用相同的AppId值
AppId={{A5E31B2D-1C5F-4A25-B7C5-2E4F58D1C92A}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
AppContact={#MyAppEmail}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=auto
AllowNoIcons=yes
; 以下行取消注释，以在非管理安装模式下运行（仅为当前用户安装）
;PrivilegesRequired=lowest
OutputBaseFilename=电脑鼠上位机_v{#MyAppVersion}_安装程序
OutputDir=.
SetupIconFile=icon.ico
UninstallDisplayIcon={app}\{#MyAppExeName}
UninstallDisplayName={#MyAppName}
WizardImageFile=
WizardSmallImageFile=
SolidCompression=yes
WizardStyle=modern
Compression=lzma2/ultra
InternalCompressLevel=ultra
LZMAUseSeparateProcess=yes
LZMANumBlockThreads=2
; 最小化安装时显示
MinVersion=6.1
; 安装前检查
AllowRootDirectory=no
DirExistsWarning=auto

; 添加版权信息
AppCopyright=Copyright © 2025 {#MyAppPublisher}

; 添加详细的版本信息
VersionInfoVersion={#MyAppVersionFull}
VersionInfoCompany={#MyAppPublisher}
VersionInfoDescription={#MyAppDescription}
VersionInfoCopyright=Copyright © 2025 {#MyAppPublisher}
VersionInfoProductName={#MyAppName}
VersionInfoProductVersion={#MyAppVersion}
VersionInfoProductTextVersion={#MyAppVersion}
VersionInfoOriginalFileName={#MyAppExeName}
VersionInfoComments={#MyProject} | {#MySchool}
VersionInfoInternalName={#MyAppName}
VersionInfoOriginalFile={#MyAppExeName}

; 自定义安装向导窗口大小和样式
WizardSizePercent=120
WizardResizable=yes
; 显示欢迎页面和完成页面
DisableWelcomePage=no
DisableFinishedPage=no
DisableReadyPage=no
DisableReadyMemo=no
; 许可协议（可选）
;LicenseFile=license.txt
; 信息文件（可选）
;InfoBeforeFile=readme.txt
;InfoAfterFile=changelog.txt

; 安装日志
SetupLogging=yes

; 显示详细的安装信息
ShowLanguageDialog=auto

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"; LicenseFile=""
Name: "chinesesimplified"; MessagesFile: "compiler:Languages\ChineseSimplified.isl"; LicenseFile=""

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "创建快速启动图标"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1
Name: "startmenu"; Description: "创建开始菜单文件夹"; GroupDescription: "{cm:AdditionalIcons}"; Flags: checkedonce
Name: "associate"; Description: "关联配置文件（.config）"; GroupDescription: "文件关联"; Flags: unchecked
Name: "autostart"; Description: "开机自启动（可选）"; GroupDescription: "其他选项"; Flags: unchecked

[Files]
; 主程序文件（优先从 dist 目录，如果没有则从当前目录）
Source: "dist\电脑鼠上位机.exe"; DestDir: "{app}"; Flags: ignoreversion signonce; Check: FileExists(ExpandConstant('{src}\dist\电脑鼠上位机.exe'))
Source: "电脑鼠上位机.exe"; DestDir: "{app}"; Flags: ignoreversion signonce; Check: (not FileExists(ExpandConstant('{src}\dist\电脑鼠上位机.exe'))) and FileExists(ExpandConstant('{src}\电脑鼠上位机.exe'))
Source: "icon.ico"; DestDir: "{app}"; Flags: ignoreversion; Attribs: readonly
; 包含其他必要文件（排除开发文件）
Source: "*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs; Excludes: "*.iss,*.py,*.spec,*.pyc,__pycache__,dist\*,build\*,*.log,*.tmp,*.bak,*.md,测试更新检查.py,backup.py"

[InstallDelete]
; 清理旧版本可能残留的文件
Type: filesandordirs; Name: "{app}\build"
Type: filesandordirs; Name: "{app}\dist"
Type: filesandordirs; Name: "{app}\__pycache__"
Type: files; Name: "{app}\*.pyc"
Type: files; Name: "{app}\*.pyo"
Type: files; Name: "{app}\*.py"
Type: files; Name: "{app}\*.spec"
Type: files; Name: "{app}\*.log"

[UninstallDelete]
; 卸载时删除的文件和目录
Type: filesandordirs; Name: "{app}\config"
Type: filesandordirs; Name: "{app}\logs"
Type: filesandordirs; Name: "{app}\cache"
Type: files; Name: "{app}\*.log"
Type: files; Name: "{app}\*.tmp"

[Icons]
; 开始菜单图标
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Comment: "{#MyProject}"; IconFilename: "{app}\icon.ico"; Tasks: startmenu
Name: "{group}\卸载 {#MyAppName}"; Filename: "{uninstallexe}"; Comment: "卸载 {#MyAppName}"; Tasks: startmenu
Name: "{group}\项目主页"; Filename: "{#MyAppURL}"; Comment: "访问项目主页"; Tasks: startmenu
; 桌面图标
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Comment: "{#MyProject}"; IconFilename: "{app}\icon.ico"; Tasks: desktopicon
; 快速启动图标（仅Windows 7及以下）
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\icon.ico"; Tasks: quicklaunchicon
; 开机自启动
Name: "{userstartup}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\icon.ico"; Tasks: autostart

[Run]
; 安装完成后运行程序
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent; Check: CheckExeExists
; 打开项目主页
Filename: "{#MyAppURL}"; Description: "访问项目主页"; Flags: postinstall shellexec skipifsilent unchecked
; 打开安装目录
Filename: "{app}"; Description: "打开安装目录"; Flags: postinstall shellexec skipifsilent unchecked

[Registry]
; 注册程序卸载信息
Root: HKCU; Subkey: "Software\{#MyAppPublisher}\{#MyAppName}"; ValueType: string; ValueName: "Version"; ValueData: "{#MyAppVersion}"; Flags: uninsdeletekey
Root: HKCU; Subkey: "Software\{#MyAppPublisher}\{#MyAppName}"; ValueType: string; ValueName: "InstallPath"; ValueData: "{app}"; Flags: uninsdeletekey
Root: HKCU; Subkey: "Software\{#MyAppPublisher}\{#MyAppName}"; ValueType: string; ValueName: "InstallDate"; ValueData: "{code:GetInstallDate}"; Flags: uninsdeletekey

; 添加到"添加或删除程序"
Root: HKLM; Subkey: "Software\Microsoft\Windows\CurrentVersion\Uninstall\{#MyAppName}"; ValueType: string; ValueName: "DisplayName"; ValueData: "{#MyAppName}"; Flags: uninsdeletevalue
Root: HKLM; Subkey: "Software\Microsoft\Windows\CurrentVersion\Uninstall\{#MyAppName}"; ValueType: string; ValueName: "DisplayVersion"; ValueData: "{#MyAppVersion}"; Flags: uninsdeletevalue
Root: HKLM; Subkey: "Software\Microsoft\Windows\CurrentVersion\Uninstall\{#MyAppName}"; ValueType: string; ValueName: "Publisher"; ValueData: "{#MyAppPublisher}"; Flags: uninsdeletevalue
Root: HKLM; Subkey: "Software\Microsoft\Windows\CurrentVersion\Uninstall\{#MyAppName}"; ValueType: string; ValueName: "URLInfoAbout"; ValueData: "{#MyAppURL}"; Flags: uninsdeletevalue
Root: HKLM; Subkey: "Software\Microsoft\Windows\CurrentVersion\Uninstall\{#MyAppName}"; ValueType: string; ValueName: "DisplayIcon"; ValueData: "{app}\{#MyAppExeName},0"; Flags: uninsdeletevalue
Root: HKLM; Subkey: "Software\Microsoft\Windows\CurrentVersion\Uninstall\{#MyAppName}"; ValueType: string; ValueName: "UninstallString"; ValueData: "{uninstallexe}"; Flags: uninsdeletevalue
Root: HKLM; Subkey: "Software\Microsoft\Windows\CurrentVersion\Uninstall\{#MyAppName}"; ValueType: dword; ValueName: "NoModify"; ValueData: "1"; Flags: uninsdeletevalue
Root: HKLM; Subkey: "Software\Microsoft\Windows\CurrentVersion\Uninstall\{#MyAppName}"; ValueType: dword; ValueName: "NoRepair"; ValueData: "1"; Flags: uninsdeletevalue
Root: HKLM; Subkey: "Software\Microsoft\Windows\CurrentVersion\Uninstall\{#MyAppName}"; ValueType: string; ValueName: "Comments"; ValueData: "{#MyProject}"; Flags: uninsdeletevalue

[CustomMessages]
; 中文消息（使用英文语言但显示中文内容）
english.WelcomeLabel2=欢迎使用 [name] 安装向导！%n%n这是由 {#MyDeveloper} 开发的 {#MyProject}。%n%n本程序专为电子系统设计课程开发，具有以下功能：%n• 实时串口通信%n• 轨迹可视化显示%n• 迷宫墙体自动绘制%n• 3D轨迹回放%n%n建议您在继续安装前关闭所有其他应用程序。
english.FinishedLabelNoIcons=安装程序已在您的计算机上成功安装 [name]。%n%n开发者：{#MyDeveloper}%n学校：{#MySchool}%n项目：{#MyProject}%n版本：{#MyAppVersion}%n%n如有问题或建议，欢迎通过以下方式联系：%n邮箱：{#MyAppEmail}%n网站：{#MyAppURL}%n%n感谢您的使用！
english.FinishedLabel=安装程序已在您的计算机上成功安装 [name]。%n%n开发者：{#MyDeveloper}%n学校：{#MySchool}%n项目：{#MyProject}%n版本：{#MyAppVersion}%n%n您可以通过选择安装的图标来运行此程序。%n%n如有问题或建议，欢迎通过以下方式联系：%n邮箱：{#MyAppEmail}%n网站：{#MyAppURL}%n%n感谢您的使用！
english.AboutApp=关于 %1
english.DeveloperInfo=开发者：{#MyDeveloper}
english.DevelopedFor={#MyProject}

[Code]
var
  OldVersion: String;
  UninstallPage: TOutputProgressWizardPage;

// ============================================================================
// 辅助函数
// ============================================================================

// 检查可执行文件是否存在
function CheckExeExists(): Boolean;
begin
  Result := FileExists(ExpandConstant('{src}\dist\{#MyAppExeName}')) or 
            FileExists(ExpandConstant('{src}\{#MyAppExeName}'));
end;

// 获取安装日期
function GetInstallDate(Param: String): String;
begin
  // 使用 Inno Setup 的日期时间格式化函数
  Result := GetDateTimeString('yyyy-mm-dd hh:nn:ss', #0, #0);
end;

// 检查磁盘空间（需要至少500MB）
function CheckDiskSpace(): Boolean;
var
  FreeSpace, RequiredSpace: Int64;
begin
  RequiredSpace := 500 * 1024 * 1024; // 500MB
  FreeSpace := DiskFreeSpace(ExtractFileDrive(ExpandConstant('{app}')));
  Result := FreeSpace >= RequiredSpace;
  
  if not Result then
  begin
    MsgBox('错误：磁盘空间不足！' + #13#10 +
           '需要至少 500 MB 的可用空间。' + #13#10 +
           '当前可用空间：' + FormatByteSize(FreeSpace), 
           mbError, MB_OK);
  end;
end;

// 检查是否已安装旧版本
function CheckOldVersion(): Boolean;
var
  UninstallKey: String;
  UninstallString: String;
  OldVersionString: String;
begin
  Result := False;
  UninstallKey := 'Software\Microsoft\Windows\CurrentVersion\Uninstall\{#MyAppName}';
  
  // 检查注册表中是否有旧版本
  if RegQueryStringValue(HKLM, UninstallKey, 'UninstallString', UninstallString) then
  begin
    // 尝试读取旧版本号
    if RegQueryStringValue(HKLM, UninstallKey, 'DisplayVersion', OldVersionString) then
    begin
      OldVersion := OldVersionString;
      Result := True;
    end
    else
    begin
      OldVersion := '未知版本';
      Result := True;
    end;
  end
  else if RegQueryStringValue(HKCU, 'Software\{#MyAppPublisher}\{#MyAppName}', 'Version', OldVersionString) then
  begin
    OldVersion := OldVersionString;
    Result := True;
  end;
end;

// 卸载旧版本
procedure UninstallOldVersion();
var
  UninstallKey: String;
  UninstallString: String;
  ErrorCode: Integer;
begin
  UninstallKey := 'Software\Microsoft\Windows\CurrentVersion\Uninstall\{#MyAppName}';
  
  if RegQueryStringValue(HKLM, UninstallKey, 'UninstallString', UninstallString) then
  begin
    // 提取卸载程序路径（去掉 /S 参数）
    if Pos('/SILENT', UninstallString) > 0 then
      UninstallString := Copy(UninstallString, 1, Pos('/SILENT', UninstallString) - 2)
    else if Pos('/VERYSILENT', UninstallString) > 0 then
      UninstallString := Copy(UninstallString, 1, Pos('/VERYSILENT', UninstallString) - 2);
    
    UninstallString := RemoveQuotes(UninstallString);
    
    // 静默卸载旧版本
    if Exec(UninstallString, '/SILENT /NORESTART', '', SW_HIDE, ewWaitUntilTerminated, ErrorCode) then
    begin
      // 等待卸载完成
      Sleep(2000);
      // 删除旧版本目录（如果存在）
      if DirExists(ExpandConstant('{app}')) then
        DelTree(ExpandConstant('{app}'), False, True, True);
    end;
  end;
end;

// ============================================================================
// 安装过程函数
// ============================================================================

// 安装初始化
function InitializeSetup(): Boolean;
var
  Response: Integer;
begin
  Result := True;
  
  // 检查磁盘空间
  if not CheckDiskSpace() then
  begin
    Result := False;
    Exit;
  end;
  
  // 检查旧版本
  if CheckOldVersion() then
  begin
    Response := MsgBox('检测到已安装的旧版本：' + OldVersion + #13#10#13#10 +
                      '是否要卸载旧版本并安装新版本？' + #13#10#13#10 +
                      '点击"是"自动卸载旧版本，点击"否"取消安装。',
                      mbConfirmation, MB_YESNO);
    
    if Response = IDYES then
    begin
      UninstallOldVersion();
    end
    else
    begin
      Result := False;
      Exit;
    end;
  end;
  
  // 显示欢迎信息
    if MsgBox('{#MyAppName} v{#MyAppVersion}' + #13#10#13#10 +
            '开发者：{#MyDeveloper}' + #13#10 +
            '学校：{#MySchool}' + #13#10 +
            '项目：{#MyProject}' + #13#10#13#10 +
            '本程序为电子系统设计课程开发，具有以下功能：' + #13#10 +
            '• 实时串口通信' + #13#10 +
            '• 轨迹可视化显示' + #13#10 +
            '• 迷宫墙体自动绘制' + #13#10 +
            '• 3D轨迹回放' + #13#10#13#10 +
            '是否继续安装？', 
            mbInformation, MB_YESNO) = IDNO then
    Result := False;
end;

// 安装向导页面改变事件
procedure CurPageChanged(CurPageID: Integer);
begin
  case CurPageID of
    wpWelcome:
    begin
      // 自定义欢迎页面
      WizardForm.WelcomeLabel2.Caption := 
        '欢迎使用 {#MyAppName} 安装向导！' + #13#10#13#10 +
        '这是由 {#MyDeveloper} 开发的 {#MyProject}。' + #13#10#13#10 +
        '本程序专为电子系统设计课程开发，具有以下功能：' + #13#10 +
        '• 实时串口通信' + #13#10 +
        '• 轨迹可视化显示' + #13#10 +
        '• 迷宫墙体自动绘制' + #13#10 +
        '• 3D轨迹回放' + #13#10#13#10 +
        '建议您在继续安装前关闭所有其他应用程序。';
    end;
    
    wpInstalling:
  begin
      // 自定义安装进度页面
    WizardForm.StatusLabel.Caption := '正在安装 {#MyAppName} v{#MyAppVersion}...';
    WizardForm.FilenameLabel.Caption := '开发者：{#MyDeveloper} | {#MySchool}';
    end;
    
    wpFinished:
    begin
      // 自定义完成页面
      WizardForm.FinishedLabel.Caption := 
        '{#MyAppName} 已成功安装到您的计算机。' + #13#10#13#10 +
        '开发者：{#MyDeveloper}' + #13#10 +
        '学校：{#MySchool}' + #13#10 +
        '项目：{#MyProject}' + #13#10 +
        '版本：{#MyAppVersion}' + #13#10#13#10 +
        '如有问题或建议，欢迎通过以下方式联系：' + #13#10 +
        '邮箱：{#MyAppEmail}' + #13#10 +
        '网站：{#MyAppURL}';
    end;
  end;
end;

// 初始化卸载过程
function InitializeUninstall(): Boolean;
var
  Response: Integer;
  ConfigPath: String;
begin
  Result := True;
  
  // 检查是否有用户配置文件需要保留
  ConfigPath := ExpandConstant('{app}\config');
  
  Response := MsgBox('即将卸载 {#MyAppName} v{#MyAppVersion}' + #13#10#13#10 +
            '开发者：{#MyDeveloper}' + #13#10 +
            '学校：{#MySchool}' + #13#10#13#10 +
            '卸载后，所有程序文件将被删除。' + #13#10#13#10 +
            '确定要卸载吗？' + #13#10#13#10 +
            '感谢您使用本软件！如有问题欢迎反馈。', 
            mbConfirmation, MB_YESNO or MB_DEFBUTTON2);
  
  if Response = IDNO then
    Result := False;
end;

// 卸载进度页面改变
procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
begin
  case CurUninstallStep of
    usUninstall:
    begin
      // 卸载中
      UninstallProgressForm.StatusLabel.Caption := '正在卸载 {#MyAppName}...';
    end;
    
    usPostUninstall:
    begin
      // 卸载完成
      MsgBox('{#MyAppName} 已成功从您的计算机卸载。' + #13#10#13#10 +
             '感谢您的使用！', 
             mbInformation, MB_OK);
    end;
  end;
end;

// 需要重启检查（如果需要）
function ShouldSkipPage(PageID: Integer): Boolean;
begin
  Result := False;
end;

// 检查是否需要重启
function NeedRestart(): Boolean;
var
  Response: Integer;
  ProcessID: LongWord;
begin
  Result := False;
  // 检查是否有程序正在运行（尝试查找进程）
  if IsModuleLoaded('{#MyAppExeName}') then
  begin
    Response := MsgBox('检测到 {#MyAppName} 正在运行。' + #13#10#13#10 +
                      '需要关闭程序才能继续安装。是否立即关闭？', 
                      mbConfirmation, MB_YESNO);
    if Response = IDYES then
    begin
      // 尝试关闭程序
      Exec('taskkill', '/F /IM "{#MyAppExeName}"', '', SW_HIDE, ewWaitUntilTerminated, Response);
      Sleep(1000);
    end;
  end;
end;

// 安装前的目录检查
function NextButtonClick(CurPageID: Integer): Boolean;
begin
  Result := True;
  
  if CurPageID = wpSelectDir then
  begin
    // 检查目录是否可写
    if not DirExists(ExpandConstant('{app}')) then
    begin
      if not CreateDir(ExpandConstant('{app}')) then
      begin
        MsgBox('无法创建安装目录，请检查权限或选择其他目录。', mbError, MB_OK);
        Result := False;
        Exit;
      end;
    end;
    
    // 再次检查磁盘空间
    if not CheckDiskSpace() then
      Result := False;
  end;
end;