!define PRODUCT_NAME "Nimbus Service for Windows Client"
!define PRODUCT_VERSION "1.0"
!define PRODUCT_PUBLISHER "Veezor"
!define PRODUCT_WEB_SITE "www.veezor.com"

; MUI 1.67 compatible ------
!include "MUI.nsh"

; MUI Settings
!define MUI_ABORTWARNING
!define MUI_ICON "${NSISDIR}\Contrib\Graphics\Icons\modern-install.ico"

!insertmacro MUI_PAGE_WELCOME
LangString NIMBUSIP_TITLE ${LANG_ENGLISH} "Configuração"
LangString NIMBUSIP_SUBTITLE ${LANG_ENGLISH} " "
Page custom NimbusIPPage 
!insertmacro MUI_PAGE_INSTFILES
Page custom SendNotify
!insertmacro MUI_PAGE_FINISH
!insertmacro MUI_LANGUAGE "English"

Name "${PRODUCT_NAME} ${PRODUCT_VERSION}"
OutFile "nimbus-winservice.exe"
InstallDir "C:\Nimbus\"
RequestExecutionLevel admin


Function .onInit
  !insertmacro MUI_INSTALLOPTIONS_EXTRACT_AS "ipnimbus.ini" "NimbusIP"
FunctionEnd

Var NimbusIP
Var Password

Function NimbusIPPage
   !insertmacro MUI_HEADER_TEXT "$(NIMBUSIP_TITLE)" "$(NIMBUSIP_SUBTITLE)"
   !insertmacro MUI_INSTALLOPTIONS_DISPLAY "NimbusIP"
   !insertmacro MUI_INSTALLOPTIONS_READ $NimbusIP "NimbusIP" "Field 2" "State"
   !insertmacro MUI_INSTALLOPTIONS_READ $Password "NimbusIP" "Field 5" "State"
FunctionEnd

Function SendNotify
   ExecWait '"$INSTDIR\pkgs\windowsnotifier.exe" admin $Password $NimbusIP' $0
   IntCmp $0 1 NOTOK DONE DONE
   NOTOK:
      MessageBox MB_Ok "Não foi possível notificar o nimbus. Avise ao administrador."
       
  Goto DONE
    DONE:
FunctionEnd

Section "MainSection" SEC01
  SetOutPath "$INSTDIR"
  SetOverwrite ifnewer
  WriteUninstaller $INSTDIR\Uninstall.exe
  WriteRegStr HKCU "Software\Nimbus Service for Windows Client" "" $INSTDIR
  File /r "pkgs"
SectionEnd

Section "Bacula" SEC02
  ExecWait '"$INSTDIR\pkgs\bacula-veezor-5.0.2.exe" /S'
SectionEnd


Section "Service" SEC03
  ExecWait '"$INSTDIR\pkgs\winservice.exe" --startup=auto install'
  ExecWait '"$INSTDIR\pkgs\winservice.exe" start'
SectionEnd


Section "WriteUninstallInfo" SEC04
  WriteRegStr   HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Nimbus" "DisplayName" "Nimbus Service for Windows Client"
  WriteRegStr   HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Nimbus" "InstallLocation" "$INSTDIR"
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Nimbus" "NoModify" 1
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Nimbus" "NoRepair" 1
  WriteRegStr   HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Nimbus" "URLUpdateInfo" "http://www.veezor.com"
  WriteRegStr   HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Nimbus" "URLInfoAbout" "http://www.veezor.com"
  WriteRegStr   HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Nimbus" "HelpLink" "http://www.veezor.com"
  WriteRegStr   HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Nimbus" "UninstallString" '"$INSTDIR\Uninstall.exe"'
SectionEnd


Section "Uninstall" SEC05
  ExecWait '"$INSTDIR\pkgs\winservice.exe" stop'
  ExecWait '"$INSTDIR\pkgs\winservice.exe" remove'
  ExecWait '"C:\Program Files\Bacula\Uninstall.exe" /S'
  Delete $INSTDIR\Uninstall.exe
  Delete $INSTDIR\pkgs\winservice.exe
  Delete $INSTDIR\pkgs\bacula-veezor-5.0.2.exe
  RMDir /r $INSTDIR
  DeleteRegKey /ifempty HKCU "Software\Nimbus Service for Windows Client"
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Nimbus"
SectionEnd




