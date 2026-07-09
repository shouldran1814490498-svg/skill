# Skill Auto-Sync Script
# 从 GitHub 远端仓库自动同步 skill 到本地 .claude/commands/
# 每次发消息时自动检查远端是否有更新

param(
    [string]$RepoUrl = "https://github.com/shouldran1814490498-svg/skill.git"
)

$commandsDir = Join-Path $env:USERPROFILE ".claude\commands"
$scriptsDir = Join-Path $commandsDir "scripts"
$tempDir = Join-Path $env:TEMP "skill-sync-$(Get-Random)"

# --- 浅克隆获取最新 ---
try {
    $null = & git clone --depth 1 --quiet $RepoUrl $tempDir 2>&1
    if (-not (Test-Path $tempDir)) { exit 0 }
} catch {
    exit 0
}

$ErrorActionPreference = "Continue"

# --- 文件映射表（用数组避免 hashtable 遍历问题） ---
$mappingList = @(
    @{ Remote = "pipeline\pipeline.md";                        Local = "pipeline.md" },
    @{ Remote = "外投策略生成skill\SKILL.md";                    Local = "strategy.md" },
    @{ Remote = "外投达人筛选skill\医生达人筛选看板_Skill.md";      Local = "kol-screen.md" },
    @{ Remote = "外投小红书内容生成&审核skill\SKILL.md";           Local = "xhs.md" },
    @{ Remote = "外投比价skill\SKILL.md";                        Local = "quote-audit.md" },
    @{ Remote = "外投排期skill\SKILL.md";                        Local = "schedule.md" },
    @{ Remote = "README.md";                                   Local = "README.md" },
    @{ Remote = "外投小红书内容生成&审核skill\README.md";          Local = "xhs-readme.md" },
    @{ Remote = "外投比价skill\README.md";                       Local = "quote-audit-readme.md" },
    @{ Remote = "外投策略生成skill\README.md";                    Local = "strategy-readme.md" }
)

$updated = @()

foreach ($item in $mappingList) {
    $remotePath = Join-Path $tempDir $item.Remote
    $localPath = Join-Path $commandsDir $item.Local

    if (Test-Path $remotePath) {
        $remoteHash = (Get-FileHash $remotePath -Algorithm MD5).Hash
        $localHash = ""
        if (Test-Path $localPath) {
            $localHash = (Get-FileHash $localPath -Algorithm MD5).Hash
        }
        if ($remoteHash -ne $localHash) {
            Copy-Item $remotePath $localPath -Force
            $updated += $item.Local
        }
    }
}

# --- 同步 scripts 目录 ---
$remoteScripts = Join-Path $tempDir "外投策略生成skill\scripts"
if (Test-Path $remoteScripts) {
    Get-ChildItem $remoteScripts -File | ForEach-Object {
        $dest = Join-Path $scriptsDir $_.Name
        $remoteHash = (Get-FileHash $_.FullName -Algorithm MD5).Hash
        $localHash = ""
        if (Test-Path $dest) {
            $localHash = (Get-FileHash $dest -Algorithm MD5).Hash
        }
        if ($remoteHash -ne $localHash) {
            Copy-Item $_.FullName $dest -Force
            $updated += "scripts/$($_.Name)"
        }
    }
}

# --- 清理 ---
try { Remove-Item $tempDir -Recurse -Force -Confirm:$false } catch {}

# --- 输出结果 ---
if ($updated.Count -gt 0) {
    Write-Host "[skill-sync] Updated: $($updated -join ', ')"
} else {
    Write-Host "[skill-sync] All skills up to date."
}
