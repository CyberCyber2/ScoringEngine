$SERVER='http://10.4.2.29' 
$possible_users = @("joe", "bob", "tim")
$data = $null
$randSCR = $null
$randUSR = $null
$key = 'cool'

for ($i=1; $i -le 100; $i++) {
    $randUSR = Get-Random -Minimum 0 -Maximum 2
    $randSCR = Get-Random -Minimum -"1" -Maximum 4
    $data = '{0}:{1}:{2}:{3}'
    $USR = $possible_users[$randUSR].toString()
    $SCR = $randSCR + (Get-Random -Minimum -"2" -Maximum 3)
    $TimeInSeconds = (New-Timespan -start "01/01/1970" -end (get-date)).totalseconds.tostring().split(".")[0]
    $TimeInMinutes = [math]::Floor($TimeInSeconds / 60)
    $Body = $data -f $USR,$SCR,$TimeInMinutes,$key
    Invoke-WebRequest -SkipCertificateCheck -Uri $SERVER -Method POST -Body $Body   
    sleep 5 
}
