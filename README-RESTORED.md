# Fleet Commander - Classic Edition
**Restored**: 2026-03-25
**Status**: ✓ Working
**Historical**: One of the first script entities

---

## Quick Start

```bash
fleet-classic
```

---

## What It Does

**Multi-Repo Git Manager** for Mobile (Termux) + Laptop
- Auto-detects environment (Pixel 8a or Laptop)
- Manages multiple repos in `/home/sauron/Q/runexusiam/`
- Shows status dashboard (dirty, ahead, behind)
- One-command sync across all repos
- Git history viewer
- Auto-commit with timestamps

---

## Directory Structure

```
/home/sauron/
├── fleet-commander/      (this repo)
│   ├── fleet_ops.py      (main script)
│   └── README-RESTORED.md
└── Q/
    └── runexusiam/       (managed repos go here)
```

---

## Usage

### Dashboard View
```bash
fleet-classic
```

Shows:
- All repos in ROOT_DIR
- Branch status
- Uncommitted changes
- Ahead/behind origin

### Menu Options
1. **Sync All** - Commits, pulls, pushes all dirty repos
2. **History** - View last 5 commits per repo
3. **Setup Alias** - Adds 'fleet' to .bashrc (optional)
4. **Exit**

---

## Features

### Auto-Detection
- Termux: Uses `/storage/emulated/0/pixel8a/unexusi/`
- Laptop: Uses `/home/sauron/Q/runexusiam/`

### Smart Sync
- Only commits if dirty
- Only pulls if behind
- Only pushes if ahead or dirty
- Shows file-level details

### Git History
- Last 5 commits per repo
- Timestamps + author
- Current branch indicator

---

## Configuration

**ROOT_DIR**: `/home/sauron/Q/runexusiam/`
To manage different repos, put them in this directory.

**Example**:
```bash
cd ~/Q/runexusiam/
git clone <your-repo>
fleet-classic  # Will now show in dashboard
```

---

## Restoration Notes

**Fixed**: Created missing `/home/sauron/Q/runexusiam/` directory
**Alias**: `fleet-classic` (preserves original)
**Next**: Modern `fleet` with Gemini automation integration

---

## Historical Significance

This script represents early automation thinking:
- Multi-device awareness
- GitPython-based operations
- Interactive TUI dashboard
- One-command fleet management

**Preserved as**: Classic edition alongside modern rebuild

---

🛸 **Original Fleet Commander - Restored and Ready**
