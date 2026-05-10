# Citation Dashboard Status Line for Claude Code
# Reads state from $env:TEMP\cite_live_state.txt
# Falls back to model name + directory if no citation task active

$StateFile = "$env:TEMP\cite_live_state.txt"

if (Test-Path $StateFile) {
    $mtime = (Get-Item $StateFile).LastWriteTime
    $age = (Get-Date) - $mtime
    if ($age.TotalSeconds -lt 30) {
        Get-Content $StateFile -Raw
        exit 0
    }
}

# Fallback: read JSON from stdin, extract model + dir
try {
    $input = $input | Out-String
    $data = $input | ConvertFrom-Json
    $model = $data.model.display_name
    $dir = (Split-Path $data.workspace.current_dir -Leaf)
    Write-Output "$model  $dir"
} catch {
    Write-Output "Claude Code"
}
