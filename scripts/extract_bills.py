#!/usr/bin/env python3
"""Extract structured data from the pharmacy PDF bills in final-bills/.

Outputs data/bills.json (one record per bill, items nested) and
data/bill_items.csv (one row per line item).
"""
import csv
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "final-bills"
OUT = ROOT / "data"

FNAME_RE = re.compile(r"^(\d+)\s+(\w+)\s+(\d+)\.pdf$", re.I)
ITEM_RE = re.compile(r"^\s*([\d,.]+)\s+x\s+([\d,.]+)\s+([\d,.]+)\s*$")
TOTAL_RE = re.compile(r"^\s*(GROSS TOTAL|DISCOUNT|NET TOTAL|CASH TEN_RD|CASH BALANCE)\s+([\d,.-]+)\s*$")
HEADER_SKIP = ("THE NEW PHARMACY", "NO:86", "TP:", "Des ", ":")


def num(s):
    return float(s.replace(",", ""))


def parse(path):
    text = subprocess.run(["pdftotext", "-layout", str(path), "-"],
                          capture_output=True, text=True, check=True).stdout
    m = FNAME_RE.match(path.name)
    if not m:
        raise ValueError(f"unexpected filename: {path.name}")
    seq, colour, n = m.groups()
    colour = colour.capitalize()
    bill = {
        "file": path.name,
        "file_seq": int(seq),
        "colour": colour,
        "tag_no": int(n),
        "tag": f"{colour}-{int(n):02d}",
        "date": None, "time": None, "invoice": None, "body_tag": None,
        "items": [], "warnings": [],
    }
    totals = {}
    pending = []  # name lines awaiting a qty/price line
    in_items = False
    for line in text.splitlines():
        s = line.strip()
        if not s:
            continue
        if (mm := re.search(r"Date\s+(\S+)\s+Invoice #\s+(\d+)", s)):
            bill["date"], bill["invoice"] = mm.group(1), int(mm.group(2))
            continue
        if (mm := re.search(r"Time\s*:\s*(\S+)", s)):
            bill["time"] = mm.group(1)
            continue
        if (mm := re.search(r"tnp@thenewpharmacy\.com\s+(.+)$", s)):
            bill["body_tag"] = mm.group(1).strip()
            continue
        if s.startswith("Des "):
            in_items = True
            continue
        if (mm := TOTAL_RE.match(line)):
            totals[mm.group(1)] = num(mm.group(2))
            in_items = False
            continue
        if (mm := re.search(r"\[(\d+) item\(s\)", s)):
            bill["item_count"] = int(mm.group(1))
            continue
        if not in_items:
            continue
        if (mm := ITEM_RE.match(line)):
            qty, price, amount = map(num, mm.groups())
            name = " ".join(pending).strip()
            pending = []
            bill["items"].append({"name": name, "qty": qty, "price": price, "amount": amount})
            if abs(qty * price - amount) > 0.05:
                bill["warnings"].append(f"{name}: {qty} x {price} != {amount}")
        elif not s.startswith(HEADER_SKIP):
            pending.append(s)

    bill["gross"] = totals.get("GROSS TOTAL")
    bill["discount"] = totals.get("DISCOUNT")
    bill["net"] = totals.get("NET TOTAL")
    bill["cash_tendered"] = totals.get("CASH TEN_RD")
    bill["balance"] = totals.get("CASH BALANCE")

    w = bill["warnings"]
    if pending:
        w.append(f"unparsed lines: {pending}")
    s_amt = round(sum(i["amount"] for i in bill["items"]), 2)
    if bill["gross"] is None or abs(s_amt - bill["gross"]) > 0.05:
        w.append(f"sum of items {s_amt} != gross {bill['gross']}")
    if None not in (bill["gross"], bill["discount"], bill["net"]) and \
            abs(bill["gross"] - bill["discount"] - bill["net"]) > 0.05:
        w.append("gross - discount != net")
    if bill.get("item_count") != len(bill["items"]):
        w.append(f"item count {bill.get('item_count')} != parsed {len(bill['items'])}")
    if bill["invoice"] != bill["file_seq"]:
        w.append(f"filename number {bill['file_seq']} != invoice #{bill['invoice']}")
    return bill


def main():
    bills = sorted((parse(p) for p in SRC.glob("*.pdf")), key=lambda b: b["invoice"])
    OUT.mkdir(exist_ok=True)
    (OUT / "bills.json").write_text(json.dumps(bills, indent=1))
    with open(OUT / "bill_items.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["invoice", "tag", "colour", "date", "time", "name", "qty", "price", "amount"])
        for b in bills:
            for i in b["items"]:
                w.writerow([b["invoice"], b["tag"], b["colour"], b["date"], b["time"],
                            i["name"], i["qty"], i["price"], i["amount"]])
    n_items = sum(len(b["items"]) for b in bills)
    print(f"{len(bills)} bills, {n_items} items, NET total {sum(b['net'] for b in bills):,.2f}")
    for b in bills:
        for msg in b["warnings"]:
            print(f"  WARN {b['file']}: {msg}", file=sys.stderr)


if __name__ == "__main__":
    main()
