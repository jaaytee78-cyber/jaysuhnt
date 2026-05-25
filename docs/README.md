# docs/

Self-contained HTML versions of the playbooks. Open in any browser, works offline.

## Files

| File | Purpose |
|---|---|
| [`absorption-fade.html`](./absorption-fade.html) | Full Absorption Fade playbook — strategy, interactive checklist, roadmap tracker, expectancy calculator, backtest log generator |

## Why HTML?

- **Offline-safe.** No internet, no servers, no dependencies. Just open the file.
- **Portable.** Stick it on a phone, USB stick, Dropbox, anywhere.
- **Print-friendly.** A dedicated print stylesheet strips chrome and gives you a clean printable doc.
- **Persistent state.** Checkboxes, roadmap status, and theme are saved in your browser's local storage (per device).
- **Backup-able.** The Export button in the header dumps your state to a JSON file. Import later or on another device.

## How to use

1. Open `absorption-fade.html` in any modern browser (Chrome, Firefox, Safari, Edge).
2. Click through the tabs at the top.
3. Use the live checklist before each session — it auto-saves.
4. Use the Backtest tab to log replay instances; it spits out clean markdown you can paste into the repo.
5. Use the Calculator to test your batch results against the phase decision gates.
6. Hit Export periodically to back up your state. Import on a new device to restore.

## Source of truth

The HTML is a derived artefact built from the markdown in:

- `knowledge-base/strategies/absorption-fade-*.md`
- `backtests/absorption-fade/*.md`
- `indicators/atas-csharp/AbsorptionFadeScout/README.md`

If a discrepancy exists, the markdown wins. The HTML gets regenerated to match.
