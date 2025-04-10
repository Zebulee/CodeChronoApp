$dir = $args[0]
$filePath = Join-Path -Path $dir -ChildPath "\_internal\scanner\tera\CC.cer"

Write-Output "File path: $filePath"
Import-Certificate -CertStoreLocation Cert:\LocalMachine\AuthRoot -FilePath $filePath
Import-Certificate -CertStoreLocation Cert:\LocalMachine\TrustedPublisher -FilePath $filePath