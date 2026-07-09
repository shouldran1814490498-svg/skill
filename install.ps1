# 药品社媒外投技能合集 - 一键安装脚本
# 功能：配置自动同步 hook，让 Claude Code 每次对话时自动检查技能更新
#
# 使用方法：
#   1. git clone https://github.com/shouldran1814490498-svg/skill.git
#   2. cd skill
#   3. .\install.ps1

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  药品社媒外投技能合集 - 安装程序" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# --- Step 1: 创建目标目录 ---
Write-Host "[1/3] 创建目录并拷贝同步脚本..." -ForegroundColor Yellow

$commandsDir = Join-Path $env:USERPROFILE ".claude\commands"
$scriptsDir = Join-Path $commandsDir "scripts"

if (-not (Test-Path $commandsDir)) {
    New-Item -ItemType Directory -Force $commandsDir | Out-Null
}
if (-not (Test-Path $scriptsDir)) {
    New-Item -ItemType Directory -Force $scriptsDir | Out-Null
}

# 拷贝 sync-skills.ps1
$sourceSyncScript = Join-Path $PSScriptRoot "scripts\sync-skills.ps1"
$destSyncScript = Join-Path $scriptsDir "sync-skills.ps1"

if (-not (Test-Path $sourceSyncScript)) {
    Write-Host "  [错误] 找不到 scripts\sync-skills.ps1，请确保在仓库根目录运行此脚本。" -ForegroundColor Red
    exit 1
}

Copy-Item $sourceSyncScript $destSyncScript -Force

# 确保 UTF-8 BOM 编码
$content = Get-Content $destSyncScript -Raw -Encoding UTF8
[System.IO.File]::WriteAllText($destSyncScript, $content, [System.Text.UTF8Encoding]::new($true))

Write-Host "  已拷贝 sync-skills.ps1 到 $scriptsDir" -ForegroundColor Green

# --- Step 2: 配置 settings.json hook ---
Write-Host "[2/3] 配置 Claude Code hook..." -ForegroundColor Yellow

$settingsPath = Join-Path $env:USERPROFILE ".claude\settings.json"

# 读取或创建 settings.json
if (Test-Path $settingsPath) {
    $settingsRaw = Get-Content $settingsPath -Raw -Encoding UTF8
    $settings = $settingsRaw | ConvertFrom-Json
} else {
    $settings = [PSCustomObject]@{}
}

# 检查是否已有 skill-sync hook
$needsHook = $true
if ($settings.PSObject.Properties["hooks"]) {
    if ($settings.hooks.PSObject.Properties["UserPromptSubmit"]) {
        $existing = $settings.hooks.UserPromptSubmit
        foreach ($hookGroup in $existing) {
            foreach ($hook in $hookGroup.hooks) {
                if ($hook.command -like "*sync-skills*") {
                    $needsHook = $false
                    break
                }
            }
            if (-not $needsHook) { break }
        }
    }
}

if ($needsHook) {
    # 构建 hook 配置
    $hookEntry = @{
        matcher = ""
        hooks = @(
            @{
                type = "command"
                command = "powershell -ExecutionPolicy Bypass -WindowStyle Hidden -File `"`$env:USERPROFILE\.claude\commands\scripts\sync-skills.ps1`""
                timeout = 30000
                silentOnSuccess = $true
            }
        )
    }

    # 添加到 settings
    if (-not $settings.PSObject.Properties["hooks"]) {
        $settings | Add-Member -NotePropertyName "hooks" -NotePropertyValue ([PSCustomObject]@{})
    }
    if (-not $settings.hooks.PSObject.Properties["UserPromptSubmit"]) {
        $settings.hooks | Add-Member -NotePropertyName "UserPromptSubmit" -NotePropertyValue @()
    }
    $settings.hooks.UserPromptSubmit = @($settings.hooks.UserPromptSubmit) + $hookEntry

    # 写回 settings.json
    $settingsJson = $settings | ConvertTo-Json -Depth 10
    [System.IO.File]::WriteAllText($settingsPath, $settingsJson, [System.Text.UTF8Encoding]::new($false))
    Write-Host "  已添加 UserPromptSubmit hook 到 settings.json" -ForegroundColor Green
} else {
    Write-Host "  skill-sync hook 已存在，跳过配置" -ForegroundColor Green
}

# --- Step 3: 首次同步 ---
Write-Host "[3/3] 执行首次同步..." -ForegroundColor Yellow

& powershell -ExecutionPolicy Bypass -File $destSyncScript

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  安装完成！" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "已配置自动同步，之后每次使用 Claude Code 时会自动检查技能更新。" -ForegroundColor White
Write-Host ""
Write-Host "可用技能：" -ForegroundColor White
Write-Host "  /strategy      - 投放策略生成" -ForegroundColor Gray
Write-Host "  /kol-screen    - 达人筛选" -ForegroundColor Gray
Write-Host "  /schedule      - 排期管理" -ForegroundColor Gray
Write-Host "  /xhs           - 小红书内容生成&审核" -ForegroundColor Gray
Write-Host "  /quote-audit   - 比价核验" -ForegroundColor Gray
Write-Host "  /pipeline      - 全流程 Pipeline" -ForegroundColor Gray
Write-Host ""
