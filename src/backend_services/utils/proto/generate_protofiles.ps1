Write-Output "Generating python proto files"

$dir = "src/backend_services/utils"

# Add all service folders here to generate proto files
$services = @("account")

foreach ($service in $services) {
    $rpc_dir = $dir + "/rpc/" + $service
    $proto_dir = $dir + "/proto/" + $service

    Get-ChildItem -Path $rpc_dir -Filter *.proto | ForEach-Object {
        $protoFile = $_.Name
        $command = "python -m grpc_tools.protoc -I `"./$rpc_dir`" --pyi_out=`"./$proto_dir`" --python_out=`"./$proto_dir`" --grpc_python_out=`"./$proto_dir`" `"./$rpc_dir/$protoFile`""

        Write-Host "Running: $command" -ForegroundColor Yellow

        python -m grpc_tools.protoc -I ./$rpc_dir --pyi_out=./$proto_dir --python_out=./$proto_dir --grpc_python_out=./$proto_dir ./$rpc_dir/$protoFile
    }
}

Write-Output "Execution policy now restricted"
# Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Restricted
