#!/usr/bin/env pwsh

# Direct script mode: Python ファイルを直接実行

param(
    [switch]$Help,
    [switch]$Hello,
    [switch]$Bye
)


# スクリプトパスを設定
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ScriptPath = (Join-Path $ScriptDir "basic_example.py")


# 未知のパラメータチェック
if ($args.Count -gt 0) {
    Write-Error "Unknown parameter(s): $($args -join ', ')"
    $Help = $true
}

# ヘルプ表示
if ($Help) {
    $HelpArgs = @("run", $ScriptPath, "--help")
    & "uv" @HelpArgs
    exit 0
}

# PowerShell の出力エンコーディングを UTF-8 に設定
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

# Python の出力エンコーディングを UTF-8 に設定
$env:PYTHONIOENCODING = "utf-8"

$Arguments = @("run", $ScriptPath)
if ($Hello) { $Arguments += "--hello" }
if ($Bye) { $Arguments += "--bye" }
& "uv" @Arguments
exit $LASTEXITCODE
