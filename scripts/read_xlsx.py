#!/usr/bin/env python3
"""Read the earlier analysis workbook (stdlib only) into JSON for cross-checking."""
import json
import re
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
XLSX = ROOT / "cross-check-documents" / "AugClinicAnalysisBill.xlsx"
OUT = ROOT / "data"


def col_idx(ref):
    letters = re.match(r"[A-Z]+", ref).group()
    n = 0
    for ch in letters:
        n = n * 26 + ord(ch) - 64
    return n - 1


def sheet_rows(z, n, strings):
    x = z.read(f"xl/worksheets/sheet{n}.xml").decode()
    rows = []
    for r in re.findall(r"<row [^>]*>(.*?)</row>", x, re.S):
        row = {}
        for attrs, body in re.findall(r"<c ([^>]*?)(?:/>|>(.*?)</c>)", r, re.S):
            ref = re.search(r'r="([A-Z]+\d+)"', attrs).group(1)
            v = re.search(r"<v>(.*?)</v>", body or "")
            v = v.group(1) if v else None
            if v is not None and 't="s"' in attrs:
                v = strings[int(v)]
            row[col_idx(ref)] = v
        rows.append([row.get(i) for i in range(max(row) + 1)] if row else [])
    return rows


def main():
    z = zipfile.ZipFile(XLSX)
    sst = z.read("xl/sharedStrings.xml").decode()
    strings = [re.sub(r"<[^>]+>", "", s) for s in re.findall(r"<si>(.*?)</si>", sst, re.S)]
    unesc = lambda s: s.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">") if isinstance(s, str) else s
    strings = [unesc(s) for s in strings]

    pharma = sheet_rows(z, 1, strings)
    tokens = sheet_rows(z, 2, strings)
    lines = sheet_rows(z, 3, strings)

    def fl(v):
        try:
            return float(v)
        except (TypeError, ValueError):
            return None

    hdr = pharma[1]
    invoices = [dict(zip([h.strip() if h else f"c{i}" for i, h in enumerate(hdr)], r))
                for r in pharma[2:] if r and fl(r[0] if r else None)]
    tok = [{"token": r[1], "total": fl(r[4] if len(r) > 4 else None)} for r in tokens[1:] if r and r[0] == "HEADER"]
    lh = lines[0]
    ln = [dict(zip(lh, r)) for r in lines[1:] if r and r[0] == "DETAIL"]
    for d in ln:
        for k in ("Quantity", "UnitPrice", "LineTotalCost", "PatientTotalCost"):
            d[k] = fl(d.get(k))

    OUT.mkdir(exist_ok=True)
    json.dump({"invoices": invoices, "tokens": tok, "lines": ln},
              open(OUT / "prior_xlsx.json", "w"), indent=1)
    print(f"invoices rows {len(invoices)}, tokens {len(tok)} (sum {sum(t['total'] or 0 for t in tok):,.2f}), lines {len(ln)}")


if __name__ == "__main__":
    main()
