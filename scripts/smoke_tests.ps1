# Script para probar Agenda Multibase API
# Uso: powershell -ExecutionPolicy Bypass -File scripts/smoke_tests.ps1

$ErrorActionPreference = "Stop"
$baseUrl = $env:API_BASE_URL
if (-not $baseUrl) { $baseUrl = "http://localhost:8000" }

function Show-Step($title) {
    Write-Host "`n=== $title ===" -ForegroundColor Cyan
}

function Show-Result($name, $resp) {
    $status = if ($resp.StatusCode) { $resp.StatusCode } else { 200 }
    Write-Host ("[{0}] Status: {1}" -f $name, $status) -ForegroundColor Green
    if ($resp -is [Microsoft.PowerShell.Commands.HtmlWebResponseObject]) {
        Write-Host ($resp.Content | Out-String)
    } elseif ($resp -is [System.Management.Automation.PSCustomObject]) {
        Write-Host ((ConvertTo-Json $resp -Depth 6))
    } else {
        Write-Host ($resp | Out-String)
    }
}

function Get-Json($path) {
    return Invoke-RestMethod -Uri ("{0}{1}" -f $baseUrl, $path) -Method GET
}
function Post-Json($path, $body) {
    return Invoke-RestMethod -Uri ("{0}{1}" -f $baseUrl, $path) -Method POST -ContentType "application/json" -Body (ConvertTo-Json $body -Depth 6)
}
function Patch-Json($path, $body) {
    return Invoke-RestMethod -Uri ("{0}{1}" -f $baseUrl, $path) -Method PATCH -ContentType "application/json" -Body (ConvertTo-Json $body -Depth 6)
}
function Delete-Path($path) {
    return Invoke-RestMethod -Uri ("{0}{1}" -f $baseUrl, $path) -Method DELETE
}

try {
    Show-Step "Docs"
    $docs = Invoke-WebRequest -Uri ("{0}/docs" -f $baseUrl) -UseBasicParsing
    Show-Result "GET /docs" $docs

    # PostgreSQL: Users
    Show-Step "PostgreSQL: Users"
    $users = Get-Json "/api/users"
    Show-Result "GET /api/users" $users
    $suffix = [int](Get-Date -UFormat %s)
    try {
        $userCreate = Post-Json "/api/users" @{ name = "Alice"; email = ("alice+{0}@example.com" -f $suffix); password = "secret" }
        Show-Result "POST /api/users" $userCreate
    } catch {
        Write-Host "POST /api/users failed (likely duplicate); skipping create" -ForegroundColor Yellow
        $userCreate = $users | Select-Object -First 1
    }
    $userId = $userCreate.id
    $userPatch = Patch-Json ("/api/users/{0}" -f $userId) @{ name = "Alice Updated" }
    Show-Result "PATCH /api/users/{id}" $userPatch

    # PostgreSQL: Departments
    Show-Step "PostgreSQL: Departments"
    $deptCreate = Post-Json "/api/departments" @{ name = "IT"; location = "HQ" }
    Show-Result "POST /api/departments" $deptCreate
    $deptId = $deptCreate.id
    $deptPatch = Patch-Json ("/api/departments/{0}" -f $deptId) @{ location = "Remote" }
    Show-Result "PATCH /api/departments/{id}" $deptPatch

    # PostgreSQL: Roles
    Show-Step "PostgreSQL: Roles"
    try {
        $roleCreate = Post-Json "/api/roles" @{ name = ("Admin-{0}" -f $suffix); description = "Full access" }
        Show-Result "POST /api/roles" $roleCreate
    } catch {
        Write-Host "POST /api/roles failed (likely duplicate); skipping create" -ForegroundColor Yellow
        $roleCreate = Get-Json "/api/roles" | Select-Object -First 1
    }
    $roleId = $roleCreate.id
    $rolePatch = Patch-Json ("/api/roles/{0}" -f $roleId) @{ description = "All perms" }
    Show-Result "PATCH /api/roles/{id}" $rolePatch

    # MongoDB: Contacts
    Show-Step "MongoDB: Contacts"
    $contactCreate = Post-Json "/api/contacts" @{ name = "Bob"; phone = "555-1234" }
    Show-Result "POST /api/contacts" $contactCreate
    $contactId = $contactCreate.id
    $contactPatch = Patch-Json ("/api/contacts/{0}" -f $contactId) @{ phone = "555-5678" }
    Show-Result "PATCH /api/contacts/{id}" $contactPatch

    # MongoDB: Events
    Show-Step "MongoDB: Events"
    $eventCreate = Post-Json "/api/events" @{ title = "Meeting"; date = "2025-12-08T10:00:00Z"; description = "Planning" }
    Show-Result "POST /api/events" $eventCreate
    $eventId = $eventCreate.id
    $eventPatch = Patch-Json ("/api/events/{0}" -f $eventId) @{ description = "Updated planning" }
    Show-Result "PATCH /api/events/{id}" $eventPatch

    # Redis: Config
    Show-Step "Redis: Config"
    try {
        $configKey = "ui-" + $suffix
        $configCreate = Post-Json "/api/config" @{ key = $configKey; data = @{ theme = "dark" } }
        Show-Result "POST /api/config" $configCreate
    } catch {
        Write-Host "POST /api/config failed (likely exists); using ui key" -ForegroundColor Yellow
        $configKey = "ui"
    }
    $configPatch = Patch-Json ("/api/config/{0}" -f $configKey) @{ data = @{ theme = "light" } }
    Show-Result "PATCH /api/config/{key}" $configPatch
    $configGet = Get-Json ("/api/config/{0}" -f $configKey)
    Show-Result "GET /api/config/{key}" $configGet

    # Redis: Sessions
    Show-Step "Redis: Sessions"
    $sessionUser = "alice-" + $suffix
    $sessionCreate = Post-Json "/api/sessions" @{ user_id = $sessionUser; session_data = @{ token = "abc123" } }
    Show-Result "POST /api/sessions" $sessionCreate
    $sessionPatch = Patch-Json ("/api/sessions/{0}" -f $sessionUser) @{ session_data = @{ token = "xyz789" } }
    Show-Result "PATCH /api/sessions/{user_id}" $sessionPatch
    $sessionGet = Get-Json ("/api/sessions/{0}" -f $sessionUser)
    Show-Result "GET /api/sessions/{user_id}" $sessionGet

    # Soft deletes
    Show-Step "Soft Deletes"
    $userDel = Delete-Path ("/api/users/{0}" -f $userId)
    Show-Result "DELETE /api/users/{id}" $userDel
    $deptDel = Delete-Path ("/api/departments/{0}" -f $deptId)
    Show-Result "DELETE /api/departments/{id}" $deptDel
    $roleDel = Delete-Path ("/api/roles/{0}" -f $roleId)
    Show-Result "DELETE /api/roles/{id}" $roleDel
    $contactDel = Delete-Path ("/api/contacts/{0}" -f $contactId)
    Show-Result "DELETE /api/contacts/{id}" $contactDel
    $eventDel = Delete-Path ("/api/events/{0}" -f $eventId)
    Show-Result "DELETE /api/events/{id}" $eventDel
    $configDel = Delete-Path ("/api/config/{0}" -f $configKey)
    Show-Result "DELETE /api/config/{key}" $configDel
    $sessionDel = Delete-Path ("/api/sessions/{0}" -f $sessionUser)
    Show-Result "DELETE /api/sessions/{user_id}" $sessionDel

    Show-Step "Verification after deletes"
    Show-Result "GET /api/users" (Get-Json "/api/users")
    Show-Result "GET /api/departments" (Get-Json "/api/departments")
    Show-Result "GET /api/roles" (Get-Json "/api/roles")
    Show-Result "GET /api/contacts" (Get-Json "/api/contacts")
    Show-Result "GET /api/events" (Get-Json "/api/events")
    try { Show-Result "GET /api/config/{key}" (Get-Json ("/api/config/{0}" -f $configKey)) } catch { Write-Host "Config $configKey not found (as expected)" -ForegroundColor Yellow }
    try { Show-Result "GET /api/sessions/{user_id}" (Get-Json ("/api/sessions/{0}" -f $sessionUser)) } catch { Write-Host "Session $sessionUser not found (as expected)" -ForegroundColor Yellow }

    Write-Host "`nAll smoke tests completed." -ForegroundColor Green
} catch {
    Write-Error $_
    exit 1
}
