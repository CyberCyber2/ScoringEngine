$SERVER='https://10.4.2.29' 
$possible_users = @("joe", "bob", "tim")
$data = $null
$randSCR = $null
$randUSR = $null
$key = 'cool'

for ($i=1; $i -le 100; $i++) {
    $randUSR = Get-Random -Minimum 0 -Maximum 2
    $randSCR = Get-Random -Minimum "-1" -Maximum 4
    $data = $possible_users[$randUSR].toString() + ":" + $($randSCR += Get-Random -Minimum "-2" -Maximum 3) + ":" + $((New-TimeSpan -Start (Get-Date "01/01/1970") -End (Get-Date)).TotalSeconds) + ":" + $key.toString()
    Invoke-WebRequest -Uri $SERVER -Method POST -Body $data    
    sleep 5 
}
