# Naula Clinic — bill cross-check & reconciliation

Sources compared:

- **Final bills (PDF):** 62 bills, `final-bills/`
- **Receipt photos:** 55 receipt images transcribed from 33 photos, giving 52 distinct invoices (`cross-check-photos/`). Patient names on the handwritten slips were deliberately not transcribed.
- **Earlier ledger:** `AugClinicAnalysisBill.xlsx` → PharmaBill sheet, 182 invoices. Also the earlier write-up, `Naula_Clinic_Medicine_Cost_Analysis.docx` (Rs 1,824,394).

## 1. Photo receipts vs PDF bills

19 invoices appear both as a photo and as a PDF. Each one was compared on invoice number, net total and every line's quantity, unit price and amount.

| Invoice | Token (PDF) | Token on photo | PDF net | Photo net | Lines PDF/photo | Line items match | Result |
|---|---|---|---:|---:|---|---|---|
| 9 | Red-06 | Red-06 | 12,848.25 | 12,848.25 | 10/10 | yes | ✅ match |
| 10 | Green-05 | Green-05 | 12,958.60 | 12,958.60 | 6/6 | yes | ✅ match |
| 15 | Green-07 | Green-07 | 51,644.85 | 51,644.85 | 11/11 | yes | ✅ match |
| 17 | Red-21 | Red-21 | 2,039.50 | 2,039.50 | 3/3 | yes | ✅ match |
| 21 | Red-29 | Red-29 | 5,475.00 | 5,475.00 | 4/4 | yes | ✅ match |
| 30 | Red-41 | Red-41 | 33,950.65 | 33,950.65 | 12/12 | yes | ✅ match |
| 31 | Red-45 | Red-45 | 559.00 | 559.00 | 1/1 | yes | ✅ match |
| 37 | Green-11 | Green-11 | 17,415.45 | 17,415.45 | 7/7 | yes | ✅ match |
| 53 | Red-07 | Red-07 | 7,410.00 | 7,410.00 | 2/2 | yes | ✅ match |
| 109 | Green-32 | Green-32 | 24,350.80 | 24,350.80 | 7/7 | yes | ✅ match |
| 113 | Green-48 | Green-48 | 5,673.10 | 5,673.10 | 3/3 | yes | ✅ match |
| 138 | Green-54 | Green-54 | 33,952.30 | 33,952.30 | 9/9 | yes | ✅ match |
| 146 | Red-35 | Red-35 | 39,190.45 | 39,190.45 | 10/10 | yes | ✅ match |
| 151 | Green-65 | Green-65 | 18,452.15 | 18,452.15 | 9/9 | yes | ✅ match |
| 154 | Green-59 | Green-59 | 23,560.94 | 23,560.94 | 9/9 | yes | ✅ match |
| 155 | Green-58 | Green-58 | 8,434.65 | 8,434.65 | 5/5 | yes | ✅ match |
| 156 | Green-44 | Green-44 | 17,013.99 | 17,013.99 | 8/8 | yes | ✅ match |
| 171 | Green-46 | Green-46 | 21,138.65 | 21,138.65 | 6/6 | yes | ✅ match |
| 173 | Green-67 | Green-67 | 61,636.35 | 61,636.35 | 15/15 | yes | ✅ match |

**Every overlapping invoice matches the PDF exactly**: same net total, and the same quantity, price and amount on every line.

### Random sample: line by line

**Invoice 10 (Green-05)**: PDF printed 8:05:47PM, original receipt 10:20:51 AM (the PDFs are reprints made in the evening)

| PDF item | Qty | Price | Amount | Photo item | Qty | Price | Amount |
|---|---:|---:|---:|---|---:|---:|---:|
| OLEANZ 5MG OLANZAPINE TABLET | 130 | 19.87 | 2,583.10 | OLEANZ 5MG TABLET | 130 | 19.87 | 2583.1 |
| ROSTIN 10MG ROSUVASTATIN TABLET | 65 | 30.00 | 1,950.00 | ROSTIN 10MG TABLET | 65 | 30.0 | 1950.0 |
| DEPLUS 1000 ** VITAMIN D TABLET | 65 | 39.50 | 2,567.50 | DEPLUS 1000 ** TABLET | 65 | 39.5 | 2567.5 |
| NEUROBION VITAMIN B1+B6 +B12 TABLET | 65 | 58.00 | 3,770.00 | NEUROBION TABLET | 65 | 58.0 | 3770.0 |
| MELO 3 MELATONIN 3MG TABLET | 65 | 25.00 | 1,625.00 | MELO 3 TABLET | 65 | 25.0 | 1625.0 |
| VERMOX 100MG MEBENDAZOLE 6-S | 1 | 463.00 | 463.00 | VERMOX 100MG 6-S | 1 | 463.0 | 463.0 |

**Invoice 146 (Red-35)**: PDF printed 8:33:27PM, original receipt 6:00:56 PM (the PDFs are reprints made in the evening)

| PDF item | Qty | Price | Amount | Photo item | Qty | Price | Amount |
|---|---:|---:|---:|---|---:|---:|---:|
| GLUCOPHAGE XR 500MG METFORMION | 130 | 15.29 | 1,987.70 | GLUCOPHAGE XR 500MG TABLET | 130 | 15.29 | 1987.7 |
| FERUP ** FERROUS FUMARATE CAPSULE | 65 | 22.00 | 1,430.00 | ?ERUP ** CAPSULE (first letter obscured, possibly FERUP) | 65 | 22.0 | 1430.0 |
| DEPLUS 1000 ** VITAMIN D TABLET | 65 | 39.50 | 2,567.50 | DEPLUS 1000 ** TABLET | 65 | 39.5 | 2567.5 |
| LEFRA-10MG LEFLUNOMIDE TABLET | 130 | 79.98 | 10,397.40 | LEFRA-10MG TABLET | 130 | 79.98 | 10397.4 |
| CARTICARE CS CLUCOSAMINE & | 65 | 120.00 | 7,800.00 | CARTICARE CS TABLET | 65 | 120.0 | 7800.0 |
| SAZO EN 500MG SULFASALAZINE | 130 | 33.50 | 4,355.00 | SAZO EN 500MG TABLET | 130 | 33.5 | 4355.0 |
| ZOSERT 100MG SERTRALINE | 65 | 72.29 | 4,698.85 | ZOSERT 100MG TABLET | 65 | 72.29 | 4698.85 |
| T4 50MCG LEVOTHYROXINE TABLET | 65 | 12.10 | 786.50 | T4 50MCG TABLET (uncertain) | 65 | 12.1 | 786.5 |
| ATORLIP 10MG ATORVASTATIN 10MG | 65 | 10.50 | 682.50 | ATORLIP 10MG TABLET | 65 | 10.5 | 682.5 |
| OMEGA 3 FISH OIL (COSTAR) CAPSULE | 65 | 69.00 | 4,485.00 | OMEGA 3 FISH OIL (COSTAR) CAPSULE | 65 | 69.0 | 4485.0 |

**Invoice 156 (Green-44)**: PDF printed 8:21:15PM, original receipt 6:32:20 PM (the PDFs are reprints made in the evening)

| PDF item | Qty | Price | Amount | Photo item | Qty | Price | Amount |
|---|---:|---:|---:|---|---:|---:|---:|
| PANTODAC 20MG PANTOPRAZOLE | 130 | 33.75 | 4,387.50 | PANTODAC 20MG TABLET | 130 | 33.75 | 4387.5 |
| AQUEOUS CREAM AQUEOUS CREAM | 2 | 330.00 | 660.00 | AQUEOUS CREAM 100G | 2 | 330.0 | 660.0 |
| THYMOL IN SPIRIT 3% ** 30ML | 2 | 200.00 | 400.00 | THYMOL IN SPIRIT 3% ** 30ML | 2 | 200.0 | 400.0 |
| DEPLUS 2000 ** VITAMIN D TABLET | 65 | 47.00 | 3,055.00 | DEPLUS 2000 ** TABLET | 65 | 47.0 | 3055.0 |
| IROVEL 150MG IRBESARTAN TABLET | 65 | 69.54 | 4,520.10 | IROVEL 150MG TABLET | 65 | 69.54 | 4520.1 |
| VERMOX 100MG MEBENDAZOLE 6-S | 1 | 463.00 | 463.00 | VERMOX 100MG 6-S | 1 | 463.0 | 463.0 |
| ROSTIN 10MG ROSUVASTATIN TABLET | 65 | 30.00 | 1,950.00 | ROSTIN 10MG TABLET | 65 | 30.0 | 1950.0 |
| CILACAR 5MG CILNIDIPINE TABLET | 33 | 47.83 | 1,578.39 | CILACAR 5MG TABLET | 33 | 47.83 | 1578.39 |

**Invoice 155 (Green-58)**: PDF printed 8:24:10PM, original receipt 6:28:52 PM (the PDFs are reprints made in the evening)

| PDF item | Qty | Price | Amount | Photo item | Qty | Price | Amount |
|---|---:|---:|---:|---|---:|---:|---:|
| ASTROCORT CREAM 1% ** | 2 | 330.00 | 660.00 | ASTROCORT CREAM 1% ** 15G | 2 | 330.0 | 660.0 |
| CLOPIVAS 75MG CLOPIDOGREL TABLET | 65 | 15.87 | 1,031.55 | CLOPIVAS 75MG TABLET | 65 | 15.87 | 1031.55 |
| FINAST 5MG FINASTERIDE 5MG TABLET | 65 | 61.00 | 3,965.00 | FINAST 5MG TABLET | 65 | 61.0 | 3965.0 |
| ATORLIP 20MG ATORVASTATIN 20MG | 65 | 17.78 | 1,155.70 | ATORLIP 20MG TABLET | 65 | 17.78 | 1155.7 |
| ZAART 25MG LOSARTAN POTASSIUM | 130 | 12.48 | 1,622.40 | ZAART 25MG TABLET | 130 | 12.48 | 1622.4 |

## 2. PDF bills vs the earlier ledger (xlsx)

All 62 PDF invoices are in the ledger with **the same amount and the same token**.

## 3. Do the PDFs and photos add up to Rs 1.82M?

| | Invoices | Amount (Rs) |
|---|---:|---:|
| Final PDF bills | 62 | 928,454.90 |
| + thermal receipts only in photos | 12 | 101,606.64 |
| + handwritten follow-up invoices (100xx) in photos | 21 | 142,205.35 |
| **= PDFs + photos (no duplicates)** | **95** | **1,172,266.89** |
| Earlier ledger, all invoices as billed | 182 | 1,885,510.88 |
| Earlier ledger, after refunds (Rs 79,334.30) | | 1,806,176.58 |
| Earlier write-up figure | 128 patients | 1,824,394.00 |
| **Final amount paid to the pharmacy** | | **1,840,560.00** |
| **Still not seen (in ledger, no PDF or photo)** | **103** | **833,142.04** |

**Answer: no, not yet.** PDFs and photos together come to **Rs 1,172,267**, which is **64%** of Rs 1,824,394. The remaining **103 invoices (Rs 833,142)** are in the ledger but have no PDF or photo. Most of them are the main bills of the patients who don't have a final PDF.

The amount actually paid (Rs 1,840,560) is Rs 16,166 more than the Excel sheet. That fits bills issued after the sheet was compiled, such as the handwritten follow-up invoices dated 13 Aug, most of which are not in the ledger. Against the amount paid, PDFs and photos cover **64%**.

Two notes on the Rs 1.82M figure itself:
- The write-up's Rs 1,824,394 is the sum of **prescription-system totals per token** (CostByToken sheet). The pharmacy's own invoice amounts in the ledger add up to a slightly different figure (shown above), because the system price/quantity was corrected against the invoice in many cases (see the 'Comments / Corrections' column).
- The handwritten follow-up invoices dated 13 Aug (items supplied after the camp) mostly post-date the ledger. They are **extra spend on top of** the Rs 1.82M, not part of it.
- Some photo invoices are not in the ledger at all: #10036 (12,847.30), #10041 (691.00), #10042 (2,101.12), #10043 (1,285.00), #10044 (594.00), #10049 (5,557.12), #10050 (1,879.80), #10051 (5,107.20), #10052 (14,332.60), #10053 (4,530.00), #10055 (13,469.76), #10056 (2,349.00), #10057 (24,171.90), #10058 (7,108.40), #10059 (16,487.25), #10061 (7,386.60).

### Tokens with no PDF or photo (57)

Black-01 (7,102), Black-03 (20,270), Black-04 (4,101), Blue-01 (10,787), Blue-04 (7,196), Blue-05 (1,210), CASH (13,397), Green-01 (5,646), Green-14 (6,218), Green-20 (969), Green-21 (4,746), Green-22 (14,522), Green-23 (2,656), Green-26 (21,524), Green-27 (30,754), Green-28 (4,355), Green-30 (9,731), Green-38 (16,988), Green-41 (2,478), Green-42 (14,018), Green-43 (34,951), Green-45 (1,496), Green-52 (11,613), Green-56 (18,121), Green-57 (8,487), Green-60 (4,028), Green-62 (9,468), Green-63 (1,465), Green-66 (22,248), Red-01 (24,470), Red-04 (10,967), Red-10 (6,682), Red-11 (18,092), Red-12 (17,978), Red-15 (660), Red-16 (6,492), Red-17 (10,625), Red-18 (40,943), Red-20 (4,411), Red-22 (12,486), Red-25 (10,829), Red-26 (14,931), Red-27 (10,446), Red-28 (11,842), Red-30 (13,772), Red-31 (18,431), Red-32 (3,918), Red-34 (15,221), Red-37 (13,339), Red-40 (6,795), Red-44 (8,280), Red-46 (12,961), Red-47 (1,300), Red-48 (6,154), Red-49 (21,038), Red-50 (1,541), Red-52 (5,877)

### Ledger invoices still missing

| Invoice | Token | Amount |
|---|---|---:|
| 4 | – | 800.00 |
| 5 | Green-01 | 5,646.37 |
| 7 | – | 5,610.50 |
| 13 | Red-50 | 1,541.00 |
| 14 | Green-03 | 1,625.00 |
| 16 | Red-06 | 5,076.00 |
| 22 | Green-14 | 6,217.90 |
| 23 | Red-48 | 6,153.85 |
| 27 | Green-08 | 6,542.90 |
| 34 | – | 9,230.10 |
| 35 | – | 75.00 |
| 40 | Red-03 | 7,200.00 |
| 41 | Green-21 | 4,745.50 |
| 42 | Green-09 | 1,950.00 |
| 43 | Green-20 | 969.00 |
| 44 | Green-19 | 3,055.00 |
| 45 | Green-10 | 1,155.70 |
| 46 | Red-03 | 2,567.50 |
| 47 | Green-10 | 2,912.00 |
| 48 | Green-22 | 14,521.65 |
| 49 | Green-10 | 967.20 |
| 51 | Green-23 | 2,655.90 |
| 54 | Red-10 | 6,681.67 |
| 57 | Red-16 | 5,479.85 |
| 60 | Red-12 | 17,977.77 |
| 61 | Green-26 | 21,523.90 |
| 62 | Green-28 | 3,890.40 |
| 63 | Red-20 | 3,441.70 |
| 64 | Red-18 | 31,500.68 |
| 65 | Red-16 | 1,012.50 |
| 67 | Red-27 | 10,445.60 |
| 70 | Green-27 | 30,258.71 |
| 71 | Red-05 | 140.10 |
| 73 | Red-30 | 13,772.20 |
| 74 | Red-26 | 14,931.35 |
| 78 | Green-28 | 465.00 |
| 79 | Red-04 | 10,863.35 |
| 80 | Red-01 | 24,469.85 |
| 81 | Red-28 | 11,842.30 |
| 83 | Red-18 | 9,441.90 |
| 84 | – | 189.00 |
| 85 | Red-22 | 12,485.59 |
| 87 | Red-04 | 104.10 |
| 89 | Red-17 | 10,624.89 |
| 90 | Red-38 | 3,099.00 |
| 91 | Red-38 | 110.50 |
| 93 | Green-29 | 15,644.13 |
| 95 | Red-39 | 22,606.80 |
| 96 | Red-40 | 6,795.30 |
| 97 | Red-02 | 4,480.00 |
| 98 | Green-27 | 495.00 |
| 99 | Red-25 | 10,829.00 |
| 100 | – | 43.71 |
| 101 | Green-38 | 16,987.75 |
| 102 | Red-20 | 969.00 |
| 105 | Green-15 | 24,117.20 |
| 106 | Red-23 | 2,275.00 |
| 108 | Green-41 | 2,478.00 |
| 112 | Green-30 | 9,731.30 |
| 114 | Red-36 | 15,694.40 |
| 116 | Red-31 | 18,430.75 |
| 117 | Red-42 | 5,807.90 |
| 118 | Red-32 | 3,917.50 |
| 119 | Red-03 | 12,266.61 |
| 120 | Green-12 | 811.20 |
| 121 | Green-15 | 23,602.20 |
| 122 | Red-47 | 1,300.00 |
| 123 | Green-45 | 1,496.10 |
| 124 | Red-34 | 15,220.94 |
| 125 | Green-52 | 11,612.51 |
| 126 | CASH | 298.05 |
| 128 | Red-37 | 13,339.00 |
| 129 | Red-49 | 21,038.00 |
| 131 | Red-52 | 5,877.45 |
| 132 | Red-46 | 12,961.35 |
| 133 | Red-44 | 8,279.65 |
| 134 | Red-43 | 1,031.55 |
| 136 | Green-43 | 34,680.95 |
| 139 | Green-57 | 8,487.05 |
| 140 | Blue-05 | 1,210.00 |
| 141 | Blue-04 | 7,195.50 |
| 142 | Green-63 | 1,465.40 |
| 143 | Black-03 | 20,270.45 |
| 144 | Black-01 | 7,101.50 |
| 147 | Green-56 | 18,121.40 |
| 148 | Green-42 | 14,017.70 |
| 150 | Black-01 | 0.00 |
| 152 | Green-43 | 270.40 |
| 153 | Green-62 | 9,468.03 |
| 157 | Green-37 | 18,167.85 |
| 158 | Red-15 | 660.00 |
| 160 | Blue-01 | 10,787.44 |
| 161 | Green-60 | 3,373.67 |
| 162 | Black-04 | 4,041.40 |
| 168 | Black-04 | 59.45 |
| 169 | Green-66 | 22,247.80 |
| 170 | Red-11 | 18,091.65 |
| 172 | Red-14 | 5,200.00 |
| 174 | Green-60 | 654.20 |
| 10033 | – | 265.00 |
| 10034 | – | 295.00 |
| 10035 | Green-02 | 446.00 |
| 10040 | Red-13 | 156.87 |

## 4. Issues worth following up

Found during extraction and transcription:

- `55 Red 08.pdf`: filename number 55 != invoice #52. The ledger has invoice 52 against Red-08 too, so this is just the file's name.
- **Final bill is only a small top-up for some patients.** For these tokens the PDF is a minor invoice and the main bill is a separate invoice: Green-02 (PDF #6 Rs 484 vs Rs 930 across all invoices), Red-42 (PDF #19 Rs 328 vs Rs 6,136 across all invoices), Green-19 (PDF #24 Rs 200 vs Rs 3,255 across all invoices), Green-08 (PDF #25 Rs 6,543 vs Rs 13,086 across all invoices), Red-38 (PDF #26 Rs 1,682 vs Rs 4,892 across all invoices), Green-10 (PDF #33 Rs 8,168 vs Rs 13,203 across all invoices), Red-03 (PDF #39 Rs 424 vs Rs 22,458 across all invoices), Red-07 (PDF #53 Rs 7,410 vs Rs 12,486 across all invoices), Red-39 (PDF #72 Rs 3,682 vs Rs 26,288 across all invoices), Green-29 (PDF #110 Rs 1,032 vs Rs 16,676 across all invoices), Green-48 (PDF #113 Rs 5,673 vs Rs 41,147 across all invoices), Green-15 (PDF #115 Rs 330 vs Rs 48,049 across all invoices).
- **Possible double charges** (same item billed on two invoices for the same token):
  - Green-11: Glycomet 500mg ×65 (Rs 483.60) on #37 and again on #55.
  - Red-45: Sitagliptin 50mg ×65 (Rs 559) on #29 and #31.
  - Red-41: Zaart 25mg ×65 (Rs 811.20) on #30 and #36.
  - Green-46: Aqueous cream (Rs 330) on #177 and #178, two minutes apart; the prescription adds only one.
  - Green-44: Vermox (Rs 463) appears on both #156 and handwritten #10037.
- **Handwritten #10036 (Red-06):** resolved. The total is the written subtotal Rs 12,847.30, not the Rs 14,433.30 written below it. Invoice #11 is resolved too: its token is Green-06 (handwritten G-6).
- **Handwritten #10038 tagged 'Black-65':** there is no Black-65 token. The item (Pantodac 20mg ×260 = Rs 8,775) is the handwritten add-on on the **Green-65** prescription, and 260 tablets is double the 130 the prescription implies.
- **Kalzana price inconsistency:** #10050 charges 28.92/tablet; #9 and #10049 charge 25.00.
- **Quantities corrected after billing:** the ledger notes many 'Qty entered as 1, should be 65' corrections. The PDFs already carry the corrected quantities.
- **Photo set quality:** `PostedReceipt1.jpeg` is empty (0 bytes), and `PostedReceipt3.jpeg` and `PostedReceipt4.jpeg` are identical files. Several WhatsApp photos are clinic prescription printouts rather than bills.

## 5. Method

- PDFs were parsed with `pdftotext -layout` (`scripts/extract_bills.py`). On all 62 bills, qty × price = amount, the lines add up to the gross, gross − discount = net, and the item count matches the printed count.
- Photos were transcribed by reading each image and checking its arithmetic. Unclear digits are flagged in `data/photo_receipts.json` (field `notes`).
- This report is regenerated by `python3 scripts/reconcile.py`.
