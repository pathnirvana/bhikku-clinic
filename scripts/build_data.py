#!/usr/bin/env python3
"""Build docs/data.json (anonymised) with two datasets the dashboard can switch between:

- receipts: every pharmacy receipt we hold, PDF bills plus photographed receipts,
  de-duplicated by invoice number and grouped by patient token
- excel:    the earlier prescription spreadsheet (CostByPrescription sheet)
"""
import json
import sys
from collections import defaultdict

from common import DATA, PAID_TOTAL, PRIOR_TOTAL, ROOT, load_csv_map, unique_photo_receipts

DOCS = ROOT / "docs"
FIELDS = ("brand", "generic", "drug_class", "condition")

medicines, med_idx = [], {}


def med(brand, generic, drug_class, condition):
    key = (brand, generic, drug_class, condition)
    if key not in med_idx:
        med_idx[key] = len(medicines)
        medicines.append(dict(zip(FIELDS, key)))
    return med_idx[key]


def colour_of(tag):
    return tag.split("-")[0] if tag and "-" in tag else "Untagged"


def require(mapping, keys, what):
    missing = sorted(set(keys) - mapping.keys())
    if missing:
        sys.exit(f"{what} is missing {len(missing)} names: {missing}")


def build_receipts():
    bills = json.load(open(DATA / "bills.json"))
    pdf_map = load_csv_map("medicine_map.csv")
    photo_map = load_csv_map("photo_map.csv")
    require(pdf_map, {i["name"] for b in bills for i in b["items"]}, "medicine_map.csv")

    invoices = []  # (tag, invoice dict, items)
    for b in bills:
        items = [[med(*(pdf_map[i["name"]][k] for k in FIELDS)), i["qty"], i["price"], i["amount"]] for i in b["items"]]
        invoices.append((b["tag"], {"no": b["invoice"], "net": b["net"], "src": "pdf"}, items))

    pdf_nos = {b["invoice"] for b in bills}
    photos = {k: v for k, v in unique_photo_receipts().items() if k not in pdf_nos and v.get("net") is not None}
    require(photo_map, {i["name"] for r in photos.values() for i in r.get("items") or []}, "photo_map.csv")
    for inv, r in sorted(photos.items()):
        items = []
        for i in r.get("items") or []:
            m = photo_map[i["name"]]
            qty, amt = float(i.get("qty") or 0), float(i.get("amount") or 0)
            price = float(i["price"]) if i.get("price") is not None else (amt / qty if qty else amt)
            items.append([med(*(m[k] for k in FIELDS)), qty, round(price, 2), amt])
        tag = r.get("tag") or f"Untagged #{inv}"
        src = "photo (handwritten)" if r.get("format") == "handwritten" else "photo"
        invoices.append((tag, {"no": inv, "net": r["net"], "src": src}, items))

    by_tag = defaultdict(lambda: {"invoices": [], "items": []})
    for tag, inv, items in invoices:
        by_tag[tag]["invoices"].append(inv)
        by_tag[tag]["items"].extend(items)
    return [{"tag": t, "colour": colour_of(t), "net": round(sum(i["net"] for i in v["invoices"]), 2), **v}
            for t, v in sorted(by_tag.items())]


def build_excel():
    lines = json.load(open(DATA / "prior_xlsx.json"))["lines"]
    xmap = load_csv_map("excel_map.csv")
    require(xmap, {(l["GenericName"] or "").strip() for l in lines}, "excel_map.csv")
    by_tag = defaultdict(lambda: {"items": [], "net": 0.0})
    for l in lines:
        tag = l["TokenId"].replace("2026-08-08-", "")
        amt = l["LineTotalCost"] or 0.0
        by_tag[tag]["net"] += amt
        if not l["Quantity"]:
            continue  # prescribed but not issued
        m = xmap[(l["GenericName"] or "").strip()]
        brand = (l["BrandName"] or "").strip() or m["generic"]
        by_tag[tag]["items"].append([med(brand, m["generic"], m["drug_class"], m["condition"]),
                                     l["Quantity"], l["UnitPrice"] or 0.0, amt])
    return [{"tag": t, "colour": colour_of(t), "net": round(v["net"], 2), "invoices": [], "items": v["items"]}
            for t, v in sorted(by_tag.items())]


def main():
    receipts, excel = build_receipts(), build_excel()
    out = {
        "meta": {
            "clinic": "Bhikku Clinic Medical Camp",
            "place": "Naula, Matale District, Sri Lanka",
            "date": "2026-08-08",
            "pharmacy": "The New Pharmacy Holdings (Pvt) Ltd, Kurunegala",
            "paid_total": PAID_TOTAL,
            "prior_total": PRIOR_TOTAL,
            "prior_patients": 128,
        },
        "medicines": medicines,
        "datasets": {
            "receipts": {"label": "Receipts", "patients": receipts},
            "excel": {"label": "Excel sheet", "patients": excel},
        },
    }
    DOCS.mkdir(exist_ok=True)
    (DOCS / "data.json").write_text(json.dumps(out, separators=(",", ":")))
    for k, d in out["datasets"].items():
        ps = d["patients"]
        print(f"{k}: {len(ps)} patients, {sum(len(p['invoices']) for p in ps)} invoices, "
              f"{sum(len(p['items']) for p in ps)} items, Rs {sum(p['net'] for p in ps):,.2f}")
    print(f"{len(medicines)} medicine entries")


if __name__ == "__main__":
    main()
