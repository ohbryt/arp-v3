# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## AI Content Pipeline (Dr. OCM)

**Workflow location:** `~/openclaw/workspace/ai-content-workflow/`

**TinyFish API Key:** `sk-tinyfish-d85Piw8gdzmnX4w9E5g2_vlJrSfVe7xe`

**Auto-use criteria:**
- Research request on new topic → TinyFish web scraping first
- Drug/therapy pipeline analysis → FXR, PPAR, GLP-1, THR-β etc. web scrape
- Market analysis, clinical trials → auto-collect → content generation

**Usage:**
```bash
python3 scripts/run_tinyfish_research.py --topic "주제"
python3 scripts/generate_content.py --topic "주제" --format blog|seminar|thread
```

## MERFISH Skin Atlas Data

**Data location:** `~/openclaw/workspace/skin_atlas_analysis/output/merfish.h5ad` (3.1GB)
**Key findings:** TGFB2 ↓-13.8, PDGFA ↓-14.3, TGFB1 ↓-11.8, FGF7 ↓-12.6
**Use for:** Anti-aging cosmetics R&D, skincare target discovery

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.
