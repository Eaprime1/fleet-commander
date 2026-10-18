# Fleet Commander Restoration Plan
**Date**: 2026-03-25
**Approach**: Fix Original + Build Fresh

---

## Phase 1: Restore Original Script Entity ✓

**Historical Significance**: One of the first script entities
**Purpose**: Multi-repo git manager (mobile + laptop)
**Status**: Needs path fix

### Fix:
1. Update ROOT_DIR to working directory
2. Create expected directory structure
3. Test original functionality
4. Alias: `fleet-classic`

---

## Phase 2: Build Fresh with Gemini Pattern

**Foundation**: `.github/workflows/gemini-*.yml` automation
**Integration**: Fleet Commander multi-repo sync
**Modern**: GitHub Actions + Python + TOML configs
**Alias**: `fleet`

---

## Both Will Coexist:
- `fleet-classic` - Original entity (historical, working)
- `fleet` - Modern build (Gemini-integrated)
