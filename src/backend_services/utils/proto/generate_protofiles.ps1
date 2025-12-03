Write-Output "Generating python proto files"

$dir = "src/backend_services/"

# Add all service folders here to generate proto files
$services = @("account")

foreach ($service in $services) {
    $rpc_dir = $dir + $service + "/rpc"
    $proto_dir = $dir + $service + "/proto"

    Get-ChildItem -Path $rpc_dir -Filter *.proto | ForEach-Object {
        $protoFile = $_.Name
        $command = "python -m grpc_tools.protoc -I `"./$rpc_dir`" --pyi_out=`"./$proto_dir`" --python_out=`"./$proto_dir`" --grpc_python_out=`"./$proto_dir`" `"./$rpc_dir/$protoFile`""

        Write-Host "Running: $command" -ForegroundColor Yellow

        python -m grpc_tools.protoc -I ./$rpc_dir --pyi_out=./$proto_dir --python_out=./$proto_dir --grpc_python_out=./$proto_dir ./$rpc_dir/$protoFile
    }
}

Write-Output "Execution policy now restricted"
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Restricted
