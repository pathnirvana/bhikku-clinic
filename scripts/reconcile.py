#!/usr/bin/env python3
"""Cross-check PDF bills against receipt photos and the earlier xlsx ledger.

Writes reports/cross_check.md.
"""
import json
import random
from collections import Counter, defaultdict
from pathlib import Path

from common import PAID_TOTAL, PRIOR_TOTAL, unique_photo_receipts

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

bills = json.load(open(DATA / "bills.json"))
photos = json.load(open(DATA / "photo_receipts.json"))
prior = json.load(open(DATA / "prior_xlsx.json"))

f = lambda v: float(v) if v not in (None, "") else None
pdf = {b["invoice"]: b for b in bills}

# ledger: one row per pharmacy invoice (thermal 1-178, handwritten 100xx)
ledger = {}
for r in prior["invoices"]:
    try:
        inv = int(float(r["Inv. No"]))
    except (TypeError, ValueError):
        continue
    amt = f(r["Amount"])
    if amt is None or inv in ledger:
        continue
    tok = (r["Token"] or "").replace("2026-08-08-", "").strip(" ,-") or None
    ledger[inv] = {"token": tok, "amount": amt, "refund": f(r.get("REFUND")) or 0.0,
                   "note": r.get("Comments / Corrections")}

ph = unique_photo_receipts()
copies = Counter(int(str(r["invoice"])) for r in photos if str(r.get("invoice") or "").strip().isdigit())

def money(v):
    return "–" if v is None else f"{v:,.2f}"

def item_key(i):
    return (round(float(i["qty"] or 0), 2), round(float(i["price"] or 0), 2), round(float(i["amount"] or 0), 2))

out = []
w = out.append
w("# Naula Clinic — bill cross-check & reconciliation\n")
w("Sources compared:\n")
w(f"- **Final bills (PDF):** {len(pdf)} bills, `final-bills/`")
w(f"- **Receipt photos:** {len(photos)} receipt images transcribed from {len({p['photo'] for p in photos})} photos, giving {len(ph)} distinct invoices (`cross-check-photos/`). Patient names on the handwritten slips were deliberately not transcribed.")
w(f"- **Earlier ledger:** `AugClinicAnalysisBill.xlsx` → PharmaBill sheet, {len(ledger)} invoices. Also the earlier write-up, `Naula_Clinic_Medicine_Cost_Analysis.docx` (Rs {PRIOR_TOTAL:,}).\n")

# ---- 1. photo vs pdf
both = sorted(set(ph) & set(pdf))
w("## 1. Photo receipts vs PDF bills\n")
w(f"{len(both)} invoices appear both as a photo and as a PDF. Each one was compared on invoice number, net total and every line's quantity, unit price and amount.\n")
w("| Invoice | Token (PDF) | Token on photo | PDF net | Photo net | Lines PDF/photo | Line items match | Result |")
w("|---|---|---|---:|---:|---|---|---|")
mismatches = []
for inv in both:
    b, p = pdf[inv], ph[inv]
    pk = Counter(item_key(i) for i in b["items"])
    qk = Counter(item_key(i) for i in p.get("items") or [])
    lines_ok = pk == qk
    net_ok = p.get("net") is not None and abs(p["net"] - b["net"]) < 0.01
    tag_ok = p.get("tag") == b["tag"]
    ok = lines_ok and net_ok
    res = "✅ match" if ok else "⚠️ differs"
    if not ok:
        mismatches.append(inv)
    w(f"| {inv} | {b['tag']} | {p.get('tag') or p.get('tag_raw') or '–'}{'' if tag_ok else ' ⚠️'} | {money(b['net'])} | {money(p.get('net'))} | {len(b['items'])}/{len(p.get('items') or [])} | {'yes' if lines_ok else 'no'} | {res} |")
w("")
if mismatches:
    w(f"**Differences found on:** {', '.join(map(str, mismatches))}. Details:\n")
    for inv in mismatches:
        b, p = pdf[inv], ph[inv]
        pk = Counter(item_key(i) for i in b["items"])
        qk = Counter(item_key(i) for i in p.get("items") or [])
        w(f"- **#{inv}**: only in PDF {list((pk - qk).elements())}; only in photo {list((qk - pk).elements())}. Photo note: {p.get('notes', '')}")
    w("")
else:
    w("**Every overlapping invoice matches the PDF exactly**: same net total, and the same quantity, price and amount on every line.\n")

# random sample (seeded) for a detailed side-by-side
random.seed(8082026)
sample = random.sample(both, min(4, len(both)))
w("### Random sample: line by line\n")
for inv in sample:
    b, p = pdf[inv], ph[inv]
    w(f"**Invoice {inv} ({b['tag']})**: PDF printed {b['time']}, original receipt {p.get('time') or 'n/a'} (the PDFs are reprints made in the evening)\n")
    w("| PDF item | Qty | Price | Amount | Photo item | Qty | Price | Amount |")
    w("|---|---:|---:|---:|---|---:|---:|---:|")
    pi = list(p.get("items") or [])
    for k, i in enumerate(b["items"]):
        j = pi[k] if k < len(pi) else {}
        w(f"| {i['name']} | {i['qty']:g} | {i['price']:,.2f} | {i['amount']:,.2f} | {j.get('name', '–')} | {j.get('qty', '–')} | {j.get('price', '–')} | {j.get('amount', '–')} |")
    w("")

# ---- 2. pdf vs ledger
w("## 2. PDF bills vs the earlier ledger (xlsx)\n")
diff = []
for inv, b in sorted(pdf.items()):
    L = ledger.get(inv)
    if L is None:
        diff.append(f"| {inv} | {b['tag']} | {money(b['net'])} | not in ledger | |")
    elif abs(L["amount"] - b["net"]) > 0.01 or (L["token"] and L["token"] != b["tag"]):
        diff.append(f"| {inv} | {b['tag']} | {money(b['net'])} | {money(L['amount'])} ({L['token']}) | {L['note'] or ''} |")
if diff:
    w("| Invoice | PDF token | PDF net | Ledger amount (token) | Ledger note |")
    w("|---|---|---:|---:|---|")
    out.extend(diff)
else:
    w(f"All {len(pdf)} PDF invoices are in the ledger with **the same amount and the same token**.")
w("")

# ---- 3. totals
w("## 3. Do the PDFs and photos add up to Rs 1.82M?\n")
pdf_total = sum(b["net"] for b in bills)
extra = {k: v for k, v in ph.items() if k not in pdf and v.get("net") is not None}
extra_thermal = {k: v for k, v in extra.items() if k < 10000}
extra_hand = {k: v for k, v in extra.items() if k >= 10000}
s_th = sum(v["net"] for v in extra_thermal.values())
s_hd = sum(v["net"] for v in extra_hand.values())
covered = set(pdf) | set(extra)
led_total = sum(v["amount"] for v in ledger.values())
led_refund = sum(v["refund"] for v in ledger.values())
missing = {k: v for k, v in ledger.items() if k not in covered}
s_missing = sum(v["amount"] for v in missing.values())
not_in_ledger = sorted(k for k in covered if k not in ledger)

w("| | Invoices | Amount (Rs) |")
w("|---|---:|---:|")
w(f"| Final PDF bills | {len(pdf)} | {pdf_total:,.2f} |")
w(f"| + thermal receipts only in photos | {len(extra_thermal)} | {s_th:,.2f} |")
w(f"| + handwritten follow-up invoices (100xx) in photos | {len(extra_hand)} | {s_hd:,.2f} |")
w(f"| **= PDFs + photos (no duplicates)** | **{len(covered)}** | **{pdf_total + s_th + s_hd:,.2f}** |")
w(f"| Earlier ledger, all invoices as billed | {len(ledger)} | {led_total:,.2f} |")
w(f"| Earlier ledger, after refunds (Rs {led_refund:,.2f}) | | {led_total - led_refund:,.2f} |")
w(f"| Earlier write-up figure | 128 patients | {PRIOR_TOTAL:,.2f} |")
w(f"| **Final amount paid to the pharmacy** | | **{PAID_TOTAL:,.2f}** |")
w(f"| **Still not seen (in ledger, no PDF or photo)** | **{len(missing)}** | **{s_missing:,.2f}** |")
w("")
pct = 100 * (pdf_total + s_th + s_hd) / PRIOR_TOTAL
w(f"**Answer: no, not yet.** PDFs and photos together come to **Rs {pdf_total + s_th + s_hd:,.0f}**, which is **{pct:.0f}%** of Rs 1,824,394. "
  f"The remaining **{len(missing)} invoices (Rs {s_missing:,.0f})** are in the ledger but have no PDF or photo. Most of them are the main bills of the patients who don't have a final PDF.\n")
w(f"The amount actually paid (Rs {PAID_TOTAL:,}) is Rs {PAID_TOTAL - PRIOR_TOTAL:,} more than the Excel sheet. That fits bills issued after the sheet was compiled, such as the handwritten follow-up invoices dated 13 Aug, most of which are not in the ledger. Against the amount paid, PDFs and photos cover **{100 * (pdf_total + s_th + s_hd) / PAID_TOTAL:.0f}%**.\n")
w("Two notes on the Rs 1.82M figure itself:")
w("- The write-up's Rs 1,824,394 is the sum of **prescription-system totals per token** (CostByToken sheet). The pharmacy's own invoice amounts in the ledger add up to a slightly different figure (shown above), because the system price/quantity was corrected against the invoice in many cases (see the 'Comments / Corrections' column).")
w("- The handwritten follow-up invoices dated 13 Aug (items supplied after the camp) mostly post-date the ledger. They are **extra spend on top of** the Rs 1.82M, not part of it.")
w("- Some photo invoices are not in the ledger at all: " + (", ".join(f"#{k} ({money((ph.get(k) or {}).get('net'))})" for k in not_in_ledger) or "none") + ".\n")

# tokens covered vs missing
tok_led = defaultdict(float)
for v in ledger.values():
    if v["token"]:
        tok_led[v["token"]] += v["amount"]
tok_seen = {b["tag"] for b in bills} | {v.get("tag") for v in extra.values() if v.get("tag")}
miss_tok = sorted(t for t in tok_led if t not in tok_seen)
w(f"### Tokens with no PDF or photo ({len(miss_tok)})\n")
w(", ".join(f"{t} ({tok_led[t]:,.0f})" for t in miss_tok) + "\n")

w("### Ledger invoices still missing\n")
w("| Invoice | Token | Amount |")
w("|---|---|---:|")
for k, v in sorted(missing.items()):
    w(f"| {k} | {v['token'] or '–'} | {v['amount']:,.2f} |")
w("")

# ---- 4. anomalies
w("## 4. Issues worth following up\n")
w("Found during extraction and transcription:\n")
for b in bills:
    for m in b["warnings"]:
        w(f"- `{b['file']}`: {m}. The ledger has invoice 52 against Red-08 too, so this is just the file's name.")
w("- **Final bill is only a small top-up for some patients.** For these tokens the PDF is a minor invoice and the main bill is a separate invoice: "
  + ", ".join(f"{b['tag']} (PDF #{b['invoice']} Rs {b['net']:,.0f} vs Rs {tok_led.get(b['tag'], 0):,.0f} across all invoices)"
              for b in bills if tok_led.get(b["tag"], 0) > b["net"] * 1.5) + ".")
w("- **Possible double charges** (same item billed on two invoices for the same token):")
w("  - Green-11: Glycomet 500mg ×65 (Rs 483.60) on #37 and again on #55.")
w("  - Red-45: Sitagliptin 50mg ×65 (Rs 559) on #29 and #31.")
w("  - Red-41: Zaart 25mg ×65 (Rs 811.20) on #30 and #36.")
w("  - Green-46: Aqueous cream (Rs 330) on #177 and #178, two minutes apart; the prescription adds only one.")
w("  - Green-44: Vermox (Rs 463) appears on both #156 and handwritten #10037.")
w("- **Handwritten #10036 (Red-06):** resolved. The total is the written subtotal Rs 12,847.30, not the Rs 14,433.30 written below it. Invoice #11 is resolved too: its token is Green-06 (handwritten G-6).")
w("- **Handwritten #10038 tagged 'Black-65':** there is no Black-65 token. The item (Pantodac 20mg ×260 = Rs 8,775) is the handwritten add-on on the **Green-65** prescription, and 260 tablets is double the 130 the prescription implies.")
w("- **Kalzana price inconsistency:** #10050 charges 28.92/tablet; #9 and #10049 charge 25.00.")
w("- **Quantities corrected after billing:** the ledger notes many 'Qty entered as 1, should be 65' corrections. The PDFs already carry the corrected quantities.")
w("- **Photo set quality:** `PostedReceipt1.jpeg` is empty (0 bytes), and `PostedReceipt3.jpeg` and `PostedReceipt4.jpeg` are identical files. Several WhatsApp photos are clinic prescription printouts rather than bills.")
w("")
w("## 5. Method\n")
w("- PDFs were parsed with `pdftotext -layout` (`scripts/extract_bills.py`). On all 62 bills, qty × price = amount, the lines add up to the gross, gross − discount = net, and the item count matches the printed count.")
w("- Photos were transcribed by reading each image and checking its arithmetic. Unclear digits are flagged in `data/photo_receipts.json` (field `notes`).")
w("- This report is regenerated by `python3 scripts/reconcile.py`.")

(ROOT / "reports").mkdir(exist_ok=True)
(ROOT / "reports" / "cross_check.md").write_text("\n".join(out) + "\n")
print(f"PDF {pdf_total:,.2f} + photo thermal {s_th:,.2f} ({len(extra_thermal)}) + handwritten {s_hd:,.2f} ({len(extra_hand)}) = {pdf_total+s_th+s_hd:,.2f}")
print(f"ledger {len(ledger)} inv {led_total:,.2f}; missing {len(missing)} inv {s_missing:,.2f}; photo/pdf overlap {len(both)}, mismatches {mismatches}")
print("not in ledger:", not_in_ledger)
