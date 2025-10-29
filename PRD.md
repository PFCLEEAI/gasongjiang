# 📋 Product Requirements Document (PRD)
## 가송장 생성기 (Gyeongdong Tracking Number Generator)

---

## 1. Executive Summary

**Product Name:** 가송장 생성기
**Type:** Desktop Application (Python-based)
**Primary Function:** Generate unique Gyeongdong Express (경동택배) tracking numbers and assign them to orders from uploaded Excel files
**Target Users:** E-commerce fulfillment operators, Amazon resellers
**Key Benefit:** Automate tracking number generation with guaranteed uniqueness and randomization

---

## 2. Problem Statement

Currently, users manually manage tracking number assignment:
- ❌ Time-consuming manual entry
- ❌ Risk of duplicate tracking numbers
- ❌ Inconsistent formatting
- ❌ Different numbers across users (hard to sync)
- ❌ Manual Excel updates required

**Solution:** Automated tracking number generation with intelligent uniqueness checks

---

## 3. Product Overview

### What It Does
Users upload an Excel file with order data → Software generates unique tracking numbers → Software creates output Excel with assigned numbers

### Key Features

| Feature | Description | Priority |
|---------|-------------|----------|
| 📤 **Upload Excel** | Accept .xls/.xlsx files with order data | MUST HAVE |
| 🔢 **Generate 가송장 번호** | Create 14-digit tracking numbers | MUST HAVE |
| 🔒 **Ensure Uniqueness** | No duplicate numbers across all sessions | MUST HAVE |
| 🎲 **Randomize Numbers** | Every execution produces different numbers | MUST HAVE |
| 📥 **Assign Numbers** | Map generated numbers to orders | MUST HAVE |
| 💾 **Export Excel** | Create output file with all data + tracking numbers | MUST HAVE |
| 🚚 **Set 택배사** | Automatically set to "경동택배" for all rows | MUST HAVE |
| 🎨 **Modern UI** | Clean, intuitive interface with progress feedback | NICE TO HAVE |

---

## 4. Functional Requirements

### 4.1 Upload Function
- **Input Format:** .xls, .xlsx
- **Supported Columns:**
  - 주문번호 (Order ID)
  - 고객명 (Customer Name)
  - 상품명 (Product Name)
  - 배송주소 (Shipping Address)
  - Any other order-related columns
- **Max File Size:** 100MB
- **Validation:** File format check, non-empty data validation

### 4.2 Tracking Number Generation
**Format:** `YYYY` + `XXXX` + `XXXXXX` (14 digits total)

**Logic:**
- **Year Component (YYYY):** Current year (e.g., 2025)
- **Batch ID (XXXX):** Random 4-digit number unique per session
- **Sequence (XXXXXX):** Random 6-digit number (000000-999999)

**Constraints:**
- ✅ No duplicates within same session
- ✅ No duplicates across different sessions (store history)
- ✅ Fully randomized (not sequential)
- ✅ 100% unique rate

### 4.3 Assignment & Output
- Map each order to generated tracking number (1:1)
- Create output Excel with:
  - All original columns from input file
  - New column: `가송장 번호` (tracking number)
  - New column: `택배사` (always = "경동택배")
  - Preserve original data integrity
- Output filename: `가송장_생성기_output_[timestamp].xls`

### 4.4 User Interface
- **Button 1: "📂 파일 선택" (Select File)**
  - Opens file picker
  - Accepts .xls/.xlsx

- **Button 2: "🔄 송장 생성" (Generate Tracking Numbers)**
  - Generates unique numbers
  - Shows progress
  - Disabled until file uploaded

- **Button 3: "💾 Excel 다운로드" (Download Excel)**
  - Saves output file
  - Success message
  - Disabled until numbers generated

---

## 5. Non-Functional Requirements

### 5.1 Performance
- File upload: < 2 seconds (for 1000 rows)
- Number generation: < 1 second (for 1000 rows)
- Excel creation: < 2 seconds
- Total process: < 5 seconds

### 5.2 Security
- No data sent to external servers
- Locally processed only
- No authentication required
- No user tracking

### 5.3 Reliability
- ✅ 100% uniqueness guarantee (collision detection)
- ✅ Graceful error handling
- ✅ Input validation
- ✅ File integrity checks

### 5.4 Usability
- Intuitive Korean UI
- Clear error messages
- Progress indicators
- One-click operation flow

---

## 6. User Stories

### Story 1: Basic Workflow
```
As an e-commerce fulfillment operator
I want to quickly assign tracking numbers to my orders
So that I can expedite the shipping process

Acceptance Criteria:
✓ Upload Excel file with order data
✓ Generate tracking numbers with one click
✓ Download Excel with assigned numbers
✓ No manual entry required
✓ Process completes in under 5 seconds
```

### Story 2: Uniqueness Guarantee
```
As a reseller with multiple users
I want guaranteed unique tracking numbers
So that I don't have conflicts across team members

Acceptance Criteria:
✓ Each user gets completely different numbers
✓ No duplicates even if multiple users run simultaneously
✓ Collision detection prevents duplicates
✓ History prevents reuse of old numbers
```

### Story 3: Error Handling
```
As a user
I want clear error messages if something goes wrong
So that I can fix issues quickly

Acceptance Criteria:
✓ Invalid file format → Clear error message
✓ Empty file → Helpful warning
✓ File not found → Graceful recovery
✓ Generation fails → Retry option
```

---

## 7. Technical Constraints

- **Language:** Python 3.9+
- **Desktop OS:** Windows (primary), macOS (secondary)
- **UI Framework:** PySimpleGUI or PyQt5 (modern, responsive)
- **Excel Library:** openpyxl or pandas
- **No External APIs:** Fully offline
- **No Database:** Lightweight, file-based

---

## 8. Success Metrics

| Metric | Target | How to Measure |
|--------|--------|----------------|
| **Process Speed** | < 5 seconds for 1000 rows | Time each operation |
| **Uniqueness Rate** | 100% | Run 10 iterations, check duplicates |
| **User Error Rate** | < 1% | Monitor error messages |
| **File Success Rate** | 99%+ | Test with various Excel formats |
| **User Satisfaction** | > 4.5/5 | User feedback |

---

## 9. Design References

### UI Framework
- **Framework:** Tailwind CSS principles (adapted for desktop)
- **Component Library:** shadcn/ui design patterns (minimalist, clean)
- **Color Scheme:**
  - Primary: `#2563EB` (Blue - modern, professional)
  - Success: `#10B981` (Green - confirmation)
  - Warning: `#F59E0B` (Amber - alerts)
  - Error: `#EF4444` (Red - errors)
  - Background: `#F9FAFB` (Light gray - clean)
  - Text: `#1F2937` (Dark gray - readable)

### Design Principles
- **Minimalist:** Only essential elements
- **Clear CTA:** Large, obvious buttons
- **Accessible:** High contrast, readable fonts
- **Responsive:** Works on different screen sizes
- **Modern:** Clean typography, whitespace

---

## 10. Out of Scope

- ❌ User authentication
- ❌ Cloud storage integration
- ❌ Multiple tracking number formats
- ❌ Batch processing with scheduling
- ❌ Advanced reporting/analytics
- ❌ Mobile version

---

## 11. Release Schedule

| Phase | Timeline | Deliverables |
|-------|----------|--------------|
| **Phase 1** | Week 1 | Core functionality (upload, generate, export) |
| **Phase 2** | Week 2 | UI refinement, error handling, testing |
| **Phase 3** | Week 3 | Optimization, documentation, release |

---

## 12. Appendix

### A. Tracking Number Format Examples
```
2025 4661 035527  → Year 2025, Session 4661, Sequence 035527
2025 4441 017927  → Year 2025, Session 4441, Sequence 017927
2025 7491 017227  → Year 2025, Session 7491, Sequence 017227
```

### B. Input/Output Excel Structure
**INPUT:**
| 주문번호 | 고객명 | 상품명 | 배송주소 |
|---------|--------|---------|----------|
| ORD001 | 김철수 | iPhone 15 | 서울시 강남구... |
| ORD002 | 이영희 | AirPods | 부산시 해운대구... |

**OUTPUT:**
| 주문번호 | 고객명 | 상품명 | 배송주소 | 가송장 번호 | 택배사 |
|---------|--------|---------|----------|-----------|---------|
| ORD001 | 김철수 | iPhone 15 | 서울시 강남구... | 20254661035527 | 경동택배 |
| ORD002 | 이영희 | AirPods | 부산시 해운대구... | 20254441017927 | 경동택배 |

---

**Document Version:** 1.0
**Last Updated:** 2025-10-27
**Status:** Ready for Development
