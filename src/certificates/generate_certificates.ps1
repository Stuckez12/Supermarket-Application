Write-Output "Generating Certificates and Private Keys"

$certificate_lifetime_days = 365
$certificate_directory = "./src/certificates"

$config_directory = "./openssl.cnf"

# Add all service folders here to generate proto files
$services  = @("account", "gateway")

$certificate_folder = $certificate_directory + "/certificate"
$pkey_folder = $certificate_directory + "/private_key"

## Create folder for certificates and private keys
if (-not (Test-Path $certificate_folder)) { New-Item -ItemType Directory -Path $certificate_folder | Out-Null }
if (-not (Test-Path $pkey_folder)) { New-Item -ItemType Directory -Path $pkey_folder | Out-Null }

foreach ($service in $services) {
    openssl req -x509 -nodes -days $certificate_lifetime_days -newkey rsa:2048 -keyout ($pkey_folder + "/$service.pem") -out ($certificate_folder + "/$service.pem") -config $config_directory -extensions v3_req *> $null
    Write-Output "Generated $service Certificate and Private Key"
}

Write-Output "Generation completed"

# Automatically reset execution policy to restricted incase user forgets to do so
# This means the user must manually set execution to be allowed but only for one file (if executed)
Write-Output "Execution policy now restricted"
# Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Restricted
