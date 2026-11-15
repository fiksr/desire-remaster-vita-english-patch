# DESIRE remaster ver. — English Translation Patch for PS Vita & Vita3K

**Title ID:** `PCSG00959`  
**Platform:** PlayStation Vita / Vita3K (Windows, Android, Linux, macOS, Steam Deck)  
**Patch Version:** 1.0 (100% Script Translation + Localized UI, Config, Nameplates & Action Buttons)

---

## Features (v1.0)
- **100% Scenario Dialogue Coverage:** All `136` Vita `.bin` scenario scripts (`22,504` dialogue lines) translated — `18,583` matched from the official PC-98 English release plus `3,843` Saturn/remaster-exclusive lines translated cleanly.
- **Native Engine Wrapping:** Uses Vita native `[n]` line breaks and automatic `[w080][h080]` / `[w070][h070]` / `[w065][h065]` font scaling with a `42`-character line limit so dialogue fits cleanly inside the remaster text box without mid-word wrapping or clipping.
- **Localized Action & Investigation Buttons:**
  - `cmd1.png`: Main verbs (`LOOK / EXAMINE`, `TALK`, `THINK`, `MOVE`) and all sub-actions in Normal & Hover states.
  - `cmd2_1.png`, `cmd2_2.png`, `cmd3.png`: All `213` investigation, topic, and character command buttons.
  - `dialog.png`: `YES` / `NO` confirmation buttons and `"Don't show again"` checkbox labels.
- **Localized Settings, System & Nameplates:**
  - `config00.png`, `config01.png`, `config03.png`: Full HD settings menu, toggles, sliders, and controller footer (`Switch Tab`, `Reset Defaults`, `Voice Test`, `Back`, `Mute`).
  - `system_01.png`, `system_01_new.png`, `system_01_save.png`: Backlog & system navigation prompts (`Prev Page`, `Next Page`, `Play Voice`, `Quick Load`, `Back`).
  - `name_list1.png`: All `34` speaker nameplate slots (`Albert`, `Makoto`, `Tina`, `Kazumi`, `Sylvia`, `Christie`, `Sheryl`, `Reiko`, `Professor Stella`, etc.).
  - `10_ev/rasen1.png`–`rasen7.png`: Opening spiral sequence text images.

---

## Installation

### Option A: Update v1.01 (`data1.psarc`) — Recommended (No Tools Needed)
Download **`DESIRE_Remaster_Vita_English_Patch_v1.0_data1_rePatch.zip`** from the Releases page.

- **Vita3K (Windows / Android / Linux / macOS / Steam Deck):**
  1. Install the base Japanese game (`PCSG00959`) and **Update 1.01** in Vita3K.
  2. Extract `PCSG00959/data/data1.psarc` and copy `data1.psarc` into `<Vita3K_ux0>/app/PCSG00959/data/data1.psarc` (replacing the existing `data1.psarc`).
- **Real PS Vita (`rePatch`):**
  1. Ensure **Update 1.01** is installed and the **rePatch** kernel plugin (`rePatch.skprx` / `rePatch_reloaded`) is active.
  2. Copy `PCSG00959/data/data1.psarc` to `ux0:rePatch/PCSG00959/data/data1.psarc` via FTP or USB.

### Option B: Base Game v1.00 (`Apply_Patch.bat` / `patcher.py`)
If you only have Base v1.00 without Update 1.01 installed:
1. Download **`DESIRE_Remaster_Vita_English_Patch_v1.0.zip`** and extract it.
2. Copy your decrypted `data.psarc` (`~1.12 GB`) into the extracted folder.
3. Run `Apply_Patch.bat` (Windows) or `./apply_patch.sh` (Linux/macOS) to produce `data_patched.psarc`.
4. Rename `data_patched.psarc` to `data.psarc` and place it in `<Vita3K_ux0>/app/PCSG00959/data/data.psarc` (Vita3K) or `ux0:rePatch/PCSG00959/data/data.psarc` (Real Vita).

---

## Legal / Credits
This repository contains **zero copyrighted game assets** — only localization patches and open-source PSARC injection tools. You must supply your own legally dumped copy of *DESIRE remaster ver.* (`PCSG00959`).
