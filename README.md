# Naula Bhikku Clinic — medicine dashboard

Dashboard of the medicines dispensed at the Bhikku Clinic Medical Camp, Naula, Sri Lanka (8 Aug 2026). The medicines were donor funded.

- `docs/` — the dashboard (GitHub Pages serves this folder). Open `docs/index.html` through any static server.
- `reports/cross_check.md` — PDF vs photo vs ledger reconciliation.

## Rebuild

```sh
python3 scripts/extract_bills.py   # final-bills/*.pdf -> data/bills.json, data/bill_items.csv
python3 scripts/read_xlsx.py       # earlier ledger -> data/prior_xlsx.json
python3 scripts/build_data.py      # -> docs/data.json (anonymised tokens only)
python3 scripts/reconcile.py       # -> reports/cross_check.md
```

Needs `pdftotext` (poppler) and Python 3 (standard library only). `data/medicine_map.csv` is hand-curated: bill name → generic, drug class and the condition it is usually prescribed for.
