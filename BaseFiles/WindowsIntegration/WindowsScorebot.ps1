


$admins = @("cyan","orange","yellow")

$secedit = secedit /export /cfg C:\secpol.cfg
$secpol = (gc C:\secpol.cfg) -replace '\s',''

function checkPass {
    [CmdletBinding()]
    Param
    (
        [string]$UserName,
        [string]$ComputerName = $env:COMPUTERNAME,
        [string]$Password,
        [switch]$Blank
        
    )
    if (!($UserName) -or ( !($Password) -and !($Blank) ) ) {
        Write-Warning 'Test-LocalCredential: Please specify both user name and password'
    }
    else {
        Add-Type -AssemblyName System.DirectoryServices.AccountManagement
        $DS = New-Object System.DirectoryServices.AccountManagement.PrincipalContext('machine', $ComputerName)
        if (($Blank)) { $Password = $null }
        $DS.ValidateCredentials($UserName, $Password)
    }
}

class User {
    [string]$name

    User(
        [string]$n
    ) {
        $this.name = $n
    }

    [string] getName() {
        return $this.name
    }

    [int] works() {
        try {
            if ($((Get-LocalUser -Name $this.name).enabled) | Select-String -Pattern 'True') {
                return 1
            }
            else {
                return 0
            }
        }
        catch {
            return 0
        }
        return 0
    }
}


class Task {
    [string]$Level
    [string]$Desc
    [int]$Val
    [string]$Boolean

    Task(
        [string]$l,
        [string]$d, 
        [int]$v,
        [string]$b      
    ) {
        $this.Desc = $d
        $this.Boolean = $b
        $this.Val = $v
        $this.Level = $l
    }

    [int] getValue() {
        return $this.Val
    }

    [string] getLevel() {
        return $this.Level
    }
 
    [string] getDescription() {
        return $this.Desc
    }

    [int] isFixed() {
        if ($(Invoke-Expression $this.Boolean)) {
            return 1
        }
        else {
            return 0
        }
    }
}

$users = @([User]::new("red"),[User]::new("blue"),[User]::new("cyan"),[User]::new("green"),[User]::new("purple"),[User]::new("yellow"),[User]::new("orange"))

$allTasks = @(

    [Task]::new("Beginner", "Beginnner Forensics 1", 5 , "(Get-Content -Path C:\Users\cyber\Desktop\'Forensics 1.txt') | Select-String 'red is sus'")
    [Task]::new("Intermediate", "Intermediate Forensics 2",5, "Get-Content -Path C:\Users\cyber\Desktop\'Forensics 2.txt' | Select-String -Pattern '80'")
    [Task]::new("Beginner", "removed purple as admin", 1, " !(net localgroup Administrators | Select-String -Pattern 'purple')")
    [Task]::new("Beginner", "cyan has a password", 1, "!(checkPass -u cyan -p drip)")
    [Task]::new("Beginner", "Disabled PlugPlay", 3, "(Get-Service -Name 'PlugPlay').Status | Select-String -Pattern 'Stopped'")
    [Task]::new("Beginner", "Disabled Secondary Logon", 3, "(Get-Service -Name 'seclogon').Status | Select-String -Pattern 'Stopped'")
    [Task]::new("Beginner", "Configured UAC", 3, "(Get-ItemProperty 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System' 'ConsentPromptBehaviorAdmin').ConsentPromptBehaviorAdmin | Select-String -Pattern '2'")
    [Task]::new("Beginner","Audits Configured",2, "((gc C:\secpol.cfg) -replace '\s','') | Select-String -Pattern 'AuditLogonEvents=3'")
    [Task]::new("Beginner", "Minimum password age set",2,"(gc C:\secpol.cfg) -replace '\s' | Select-String -Pattern 'MinimumPasswordLength=12'")
    [Task]::new("Beginner","Installed Firefox",2 , "(ls C:\'Program Files (x86)').name | Select-String -Pattern 'Mozilla Firefox'")
    [Task]::new("Beginner", "Public Firewall: Block inbound connections that do not match", 2, "(Get-NetFirewallProfile -Name Public).DefaultInboundAction -eq 'Block'")
    [Task]::new("Beginner", "Public Firewall: Allow outband connections that do not match", 2, "(Get-NetFirewallProfile -Name Public).DefaultInboundAction -eq 'Allow'")

    
    [Task]::new("Intermediate", "Screensaver locks machine", 5, "(Get-ItemProperty 'HKCU:\Control Panel\Desktop' 'ScreenSaverIsSecure').ScreenSaverIsSecure -eq 1")
    [Task]::new("Intermediate", "wwwroot Permissions fixed", 5, "!((Get-ACl C:\inetpub\wwwroot) | Out-String | Select-String -Pattern 'Users Allow  FullControl')")

    [Task]::new("Intermediate", "Removed DNS Server", 5, "!((Get-WindowsFeature -Name 'DNS').installstate | Select-String -Pattern 'Installed')")
    [Task]::new("Intermediate", "Removed TFTP Client", 5, "!((Get-WindowsFeature -Name 'TFTP-Client').installstate | Select-String -Pattern 'Installed')")
    [Task]::new("Intermediate", "Removed Telnet Client", 5, "!((Get-WindowsFeature -Name 'Telnet-Client').installstate | Select-String -Pattern 'Installed')")
    [Task]::new("Intermediate", "Removed Simple TCP/IP", 5, "!((Get-WindowsFeature -Name 'Simple-TCPIP').installstate | Select-String -Pattern 'Installed')")
    [Task]::new("Intermediate", "Removed SMBv1", 5, "!((Get-WindowsFeature -Name 'FS-SMB1').installstate | Select-String -Pattern 'Installed')")
    [Task]::new("Intermediate", "Removed SNMP", 5, "!((Get-WindowsFeature -Name 'SNMP-Service').installstate | Select-String -Pattern 'Installed')")

    [Task]::new("Advanced", "IIS Directory browsing disabled", 10, "((Get-WebConfigurationProperty -filter /system.webServer/directoryBrowse -name enabled -PSPath 'IIS:\Sites\Default Web Site').value | Out-String | Select-String -Pattern 'False')")
    [Task]::new("Advanced", "IIS Anonymous Authentication disabled", 10, "((Get-WebConfigurationProperty -Filter '/system.webServer/security/authentication/anonymousAuthentication' -Name Enabled -PSPath 'IIS:\Sites\$SiteName\$AppName').value | Out-String | Select-String -Pattern 'False')")
    [Task]::new("Advanced", "IIS requires SSL", 10, "((Get-WebConfigurationProperty -pspath 'MACHINE/WEBROOT/APPHOST' -location 'Default Web Site/CertEnroll' -filter 'system.webServer/security/access' -name 'sslFlags' | Out-String | Select-String -Pattern 'Ssl,SslNegotiateCert,SslRequireCert'))")
    [Task]::new("Advanced", "IIS logging set to daily",10, "((Get-WebConfigurationProperty '/system.applicationHost/sites/siteDefaults' -Name logfile).period | Out-String | Select-String -Pattern 'Daily')")
    
)


Function update {
    [CmdletBinding()]
    param
    (
        $curr,
        $total,
        $numVulns
    )
    
    $percent = [string][math]::Round(($curr / $total) * 100) + "%"
    $score = ([string]$curr + " out of " + [string]$total + " total points")
    $questionsAnswered = ([string]$numVulns + " out of " + [string]$allTasks.Length + " total tasks completed")
    $BeginnerSolved = 0
    $BeginnerTotal = 0
    $intermediateSolved = 0
    $intermediateTotal = 0
    $advancedSolved = 0
    $advancedTotal = 0

    foreach ($t in $allTasks) {

    
        if ($t.getLevel() -eq 'Beginner') {
            $BeginnerTotal = $BeginnerTotal + 1
        }
        if ($t.getLevel() -eq 'Intermediate') {
            $intermediateTotal = $intermediateTotal + 1
        }
        if ($t.getLevel() -eq 'Advanced') {
            $advancedTotal = $advancedTotal + 1
        }
    }

    $file = 'C:\users\cyber\desktop\score.html' #score report file
    Clear-Content -Path $file
    Out-File -FilePath $file
    Add-Content -Path $file -Value ('<!DOCTYPE html> <html> <head> <meta name="viewport" content="width=device-width, initial-scale=1"> <style> * { box-sizing: border-box; } .column { float: left; padding: 10px; height: 1500px; } .left, .right { width: 25%; } .middle { width: 50%; } .row:after { content: ""; display: table; clear: both; }</style> </head> <body><div class="row"> <div class="column left" style="background-color:#0d60bf;"></div> <div class="row"> <div class="column middle" style="background-color:#fff;"><h1 style="text-align: center;"><span style="font-family: arial, helvetica, sans-serif;">Score Report</span></h1><h2 style="text-align: center;"><br /><span style="font-family: arial, helvetica, sans-serif;">' + $percent + ' completed</span></h2><p> </p>')
    Add-Content -Path $file -Value ('<p><span style=color:red;"font-family: arial, helvetica, sans-serif;"><strong>' + $penalties + ' Points in Scoring Penalties</strong></span></p>')
    Add-Content -Path $file -Value ('<p><span style="font-family: arial, helvetica, sans-serif;"><strong>' + $score + '. </strong></span></p>')
    Add-Content -Path $file -Value ('<p><span style="font-family: arial, helvetica, sans-serif;"><strong>' + $questionsAnswered + '. </strong></span></p>')
    Add-Content -Path $file -Value ('<hr class="line2"><br>')

    foreach ($user in $users) {
        $user
        if (($user.works() -eq 0)) {
            Add-Content -Path $file -Value ('<p><span style=color:red;"font-size: 10pt;  font-family: arial, helvetica, sans-serif;">' + $user.getName() + ' is NOT functional: - 5 points</span></p>')
        }
    }
    
    foreach ($t in $allTasks) {
        if ($t.isFixed() -eq 1 -And $t.getLevel() -eq 'Beginner') {
            $BeginnerSolved = $BeginnerSolved + 1
            Add-Content -Path $file -Value ('<p><span style="font-size: 10pt; font-family: arial, helvetica, sans-serif;">' + '<span style="color:green;">Beginner</span>' + ' ' + $t.getDescription() + ' ' + ($t.getValue()) + ' points</span></p>')
        }

        if ($t.isFixed() -eq 1 -And $t.getLevel() -eq 'Intermediate') {
            $intermediateSolved = $intermediateSolved + 1
            Add-Content -Path $file -Value ('<p><span style="font-size: 10pt; font-family: arial, helvetica, sans-serif;">' + '<span style="color:blue;">Intermediate</span>' + ' ' + $t.getDescription() + ' ' + $t.getValue() + ' points</span></p>')
        }

        if ($t.isFixed() -eq 1 -And $t.getLevel() -eq 'Advanced') {
            $advancedSolved = $advancedSolved + 1
            Add-Content -Path $file -Value ('<p><span style="font-size: 10pt; font-family: arial, helvetica, sans-serif;">'+ '<span style="color:purple;">Advanced</span>' + ' ' + $t.getDescription() + ' ' + $t.getValue() + ' points</span></p>')
        }
    }

    $bS = ([string]$BeginnerSolved + " out of " + [string]$BeginnerTotal + " Beginner tasks completed")
    $iS = [string]$intermediateSolved + " out of " + [string]$intermediateTotal + " intermediate tasks completed"
    $aS = [string]$advancedSolved + " out of " + [string]$advancedTotal + " advanced tasks completed"
    Add-Content -Path $file -Value ('<p><span style="font-family: arial, helvetica, sans-serif;"><strong>' + $bS + '. </strong></span></p>')
    Add-Content -Path $file -Value ('<p><span style="font-family: arial, helvetica, sans-serif;"><strong>' + $iS + '. </strong></span></p>')
    Add-Content -Path $file -Value ('<p><span style="font-family: arial, helvetica, sans-serif;"><strong>' + $aS + '. </strong></span></p>')
    Add-Content -Path $file -Value ('<img src="graph.png" alt="Graph" width="350" height="250">')
    Add-Content -Path $file -Value ('</div> <div class="row"> <div class="column right" style="background-color:#0d60bf;"></div> </body>')
    Add-Content -Path $file -Value ('<meta http-equiv="refresh" content="20">')
    Add-Content -Path $file -Value ('<footer><h6>Cyber Club</h6></footer>')

    

}

Function notify {
    param($ph)

    if ($ph[-2] -lt $ph[-1]) {
        Add-Type -AssemblyName System.Windows.Forms
        $global:balmsg = New-Object System.Windows.Forms.NotifyIcon
        $path = (Get-Process -id $pid).Path
        $balmsg.Icon = [System.Drawing.Icon]::ExtractAssociatedIcon($path)
        $balmsg.BalloonTipIcon = [System.Windows.Forms.ToolTipIcon]::Warning
        $balmsg.BalloonTipText = 'You gained points!'
        $balmsg.BalloonTipTitle = "Attention $Env:USERNAME"
        $balmsg.Visible = $true
        $balmsg.ShowBalloonTip(20000)
    }

    if ($ph[-1] -lt $ph[-2]) {
        Add-Type -AssemblyName System.Windows.Forms
        $global:balmsg = New-Object System.Windows.Forms.NotifyIcon
        $path = (Get-Process -id $pid).Path
        $balmsg.Icon = [System.Drawing.Icon]::ExtractAssociatedIcon($path)
        $balmsg.BalloonTipIcon = [System.Windows.Forms.ToolTipIcon]::Warning
        $balmsg.BalloonTipText = 'You lost points!'
        $balmsg.BalloonTipTitle = "Attention $Env:USERNAME"
        $balmsg.Visible = $true
        $balmsg.ShowBalloonTip(20000)
    }
}
    
$pointHistory = @(0, 0, 0)

while ($true) {
    $currentPoints = 0
    $penalties = 0
    $numFixedVulns = 0
    $totalPoints = 0

    foreach ($u in $users) {
        if ($u.works() -eq 0) {
            $penalties = $penalties + 5
        }
    }

    foreach ($t in $allTasks) {
        $totalPoints = $totalPoints + $t.getValue()
        if ($t.isFixed() -eq 1) {
            $numFixedVulns = $numFixedVulns + 1
            $currentPoints = $currentPoints + $t.getValue()
        }
    }

    $currentPoints = $currentPoints - $penalties
    $pointHistory += $currentPoints
    notify -ph $pointHistory
    update -curr $currentPoints -total $totalPoints -numVulns $numFixedVulns
    $users.Clear()
    $pointHistory
    secedit /export /cfg C:\secpol.cfg
    ########################################
    $SERVER='http://192.168.15.132' 
    $data = $null
    $key = 'cool'

    for ($i=1; $i -le 100; $i++) {
        $data = '{0}:{1}:{2}:{3}'
        $USR = "Julian-Windows"
        $TimeInSeconds = (New-Timespan -start "01/01/1970" -end (get-date)).totalseconds.tostring().split(".")[0]
        $TimeInMinutes = [math]::Floor($TimeInSeconds / 60)
        $Body = $data -f $USR,$currentPoints,$TimeInMinutes,$key
        Invoke-WebRequest -SkipCertificateCheck -Uri $SERVER -Method POST -Body $Body   
    }
    ########################################
    Start-Sleep -Seconds 10
}

