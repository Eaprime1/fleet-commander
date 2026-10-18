# Fleet Commander - Modern Edition
**Created**: 2026-03-26
**Status**: ✓ Active
**Integration**: Gemini Automation Pattern

---

## Quick Start

```bash
fleet status              # Dashboard view
fleet sync                # Sync all repos
fleet triage              # Find repos needing attention
```

---

## What's New

**Modern Edition adds:**
- JSON output for automation (`--format json`)
- Health-based triage system
- GitHub Actions integration
- Gemini automation ready
- Clean OOP architecture
- Coexists with classic edition

---

## Architecture

### Local CLI

**fleet_modern.py** - Python 3 script with three commands:

1. **status** - Show all repos with health indicators
   ```bash
   fleet status              # Human-readable
   fleet status --format json  # Machine-readable
   ```

2. **sync** - Commit, pull, push all repos
   ```bash
   fleet sync
   fleet sync -m "Custom message"
   ```

3. **triage** - Identify repos needing attention
   ```bash
   fleet triage
   fleet triage --format json
   ```

### Health System

Each repo gets a health status:
- **SYNCED** ✅ - Clean, up to date
- **DIRTY** ⚠️  - Uncommitted changes
- **AHEAD** ⬆️  - Local commits not pushed
- **BEHIND** ⬇️  - Remote commits not pulled

### GitHub Actions Integration

**Workflow**: `.github/workflows/fleet-auto-sync.yml`

**Triggers**:
- Manual dispatch (any time)
- Daily schedule (2 AM UTC)
- Push to main (self-updating)

**Features**:
- Triages entire fleet
- Syncs all repos
- Uploads triage report as artifact
- Uses custom commit messages

---

## Directory Structure

```
~/fleet-commander/
├── fleet_ops.py                  (classic - interactive TUI)
├── fleet_modern.py               (modern - CLI + automation)
├── .github/workflows/
│   └── fleet-auto-sync.yml       (GitHub Actions)
├── README-RESTORED.md            (classic docs)
└── README-MODERN.md              (this file)
```

---

## Gemini Integration Pattern

Modern Fleet uses the same automation pattern as PrimeHaven:

1. **Dispatch** - GitHub events trigger workflows
2. **Triage** - Intelligent assessment of repo states
3. **Action** - Automated sync or manual review
4. **Telemetry** - Track decisions and outcomes

**Example Gemini workflow** (future enhancement):
```yaml
- name: 'Gemini triage analysis'
  uses: 'google-github-actions/run-gemini-cli@v0'
  with:
    prompt: |
      Analyze this fleet triage report and recommend:
      1. Which repos to sync immediately
      2. Which need manual review
      3. Any patterns in the fleet health
```

---

## Classic vs Modern

| Feature | Classic (`fleet-classic`) | Modern (`fleet`) |
|---------|--------------------------|------------------|
| Interface | Interactive TUI | Command-line args |
| Output | Human-friendly dashboard | Human + JSON |
| Automation | Manual execution | GitHub Actions ready |
| Architecture | Procedural | Object-oriented |
| Use case | Interactive management | CI/CD automation |

**Both are valid!** Use classic for hands-on work, modern for automation.

---

## Usage Examples

### Local Development

```bash
# Morning routine
fleet status          # Check fleet health
fleet triage          # See what needs attention
fleet sync            # Sync everything

# Quick check
fleet status --format json | jq '.repos[] | select(.status.health != "SYNCED")'
```

### GitHub Actions

```bash
# Trigger manual sync
gh workflow run fleet-auto-sync.yml

# View latest triage report
gh run download <run-id> -n fleet-triage-<run-id>
```

### Integration with other tools

```python
import json
import subprocess

# Get fleet status programmatically
result = subprocess.run(
    ["fleet", "status", "--format", "json"],
    capture_output=True,
    text=True
)
fleet_data = json.loads(result.stdout)

# Filter for repos needing attention
dirty_repos = [
    r for r in fleet_data["repos"]
    if r["status"]["health"] in ["DIRTY", "BEHIND"]
]
```

---

## Configuration

**ROOT_DIR**: Same as classic edition
- Laptop: `/home/sauron/Q/runexusiam/`
- Termux: `/storage/emulated/0/pixel8a/unexusi/`

**Auto-detection**: Reads `PREFIX` environment variable (Termux) or defaults to laptop.

---

## Requirements

**Python**: 3.7+
**Dependencies**: GitPython

```bash
pip install GitPython
```

---

## Future Enhancements

Potential additions (not yet implemented):

1. **Gemini-powered triage** - AI analysis of repo states
2. **Conflict resolution** - Smart merge strategies
3. **Dependency tracking** - Understand repo relationships
4. **Health history** - Track fleet health over time
5. **Notifications** - Alert on critical issues
6. **Multi-fleet support** - Manage multiple root directories

---

## Historical Context

Fleet Commander represents the evolution of multi-repo management:

**Classic** (2024-2025) - Early script entity, interactive management
**Modern** (2026) - Automation-ready, GitHub Actions integrated
**Future** - Gemini-augmented, self-organizing fleets

The pattern: Start human-driven, add automation layer, integrate AI decision-making.

---

## Testing

```bash
# Test status
fleet status

# Test JSON output
fleet status --format json | python3 -m json.tool

# Test triage
fleet triage

# Dry run sync (classic has this, modern doesn't yet)
# For now: check status before syncing
fleet triage
# Review, then:
fleet sync
```

---

## Troubleshooting

**"GitPython not available"**
```bash
pip install GitPython
```

**"Directory not found"**
```bash
mkdir -p ~/Q/runexusiam/
```

**GitHub Actions fails**
- Check repo secrets are configured
- Verify workflow has `contents: write` permission
- Review Actions logs for details

---

🚀 **Modern Fleet Commander - Automation Ready**
