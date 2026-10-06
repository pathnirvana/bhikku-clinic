"""Shared helpers for the build and reconcile scripts."""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
PAID_TOTAL = 1840560  # final amount paid to the pharmacy
PRIOR_TOTAL = 1824394  # Excel sheet (CostByPrescription) total


def load_csv_map(name):
    return {r["key"] if "key" in r else r["name"]: r for r in csv.DictReader(open(DATA / name))}


def unique_photo_receipts():
    """Photo receipts keyed by invoice number, keeping the most complete copy of each."""
    best = {}
    for r in json.load(open(DATA / "photo_receipts.json")):
        try:
            inv = int(str(r["invoice"]).strip())
        except (TypeError, ValueError):
            continue
        score = (r.get("net") is not None, not r.get("partial"), len(r.get("items") or []))
        if inv not in best or score > best[inv][0]:
            best[inv] = (score, r)
    out = {k: dict(v[1]) for k, v in best.items()}
    # manual corrections confirmed by checking the original receipts
    for inv, fix in json.load(open(DATA / "photo_corrections.json")).items():
        r = out[int(inv)]
        r.update({k: v for k, v in fix.items() if k != "note"})
        r["notes"] = f"CORRECTED: {fix['note']}. " + (r.get("notes") or "")
    return out
