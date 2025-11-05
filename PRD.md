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
**Format:** `YYYY` + `RRR` + `MM` + `RRR` + `RR` (14 digits total)

**Structure:**
- **Year (YYYY):** Current year (e.g., 2025)
- **Day of Year (RRR):** Day 1-366, zero-padded to 3 digits (e.g., 329 = Nov 25)
- **Month (MM):** Current month, zero-padded to 2 digits (e.g., 11)
- **Random 1 (RRR):** 3-digit random number (100-999)
- **Random 2 (RR):** 2-digit random number (00-99)

**Example:** `20253291170804`
- 2025 = Year
- 329 = Day 329 (November 25)
- 11 = Month 11
- 708 = Random component 1
- 04 = Random component 2

**Constraints:**
- ✅ Date-based prefix for chronological organization
- ✅ 810,000 unique combinations per day (900 × 900)
- ✅ Cryptographically secure random generation
- ✅ No duplicates within same session
- ✅ No duplicates across different sessions (history tracking)
- ✅ 100% uniqueness guarantee

### 4.3 Assignment & Output
- Map each order to generated tracking number (1:1)
- Create output Excel with specific column order:
  1. **주문고유코드** (from first column of input file)
  2. **송장번호** (generated tracking number)
  3. **택배사** (always = "경동택배")
  4. All remaining original columns from input file
- Preserve original data integrity
- Output filename: `가송장_생성기_output_[timestamp].xlsx`

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
2025 329 11 708 04  → Year 2025, Day 329, Month 11, Random 708-04
2025 329 11 815 92  → Year 2025, Day 329, Month 11, Random 815-92
2025 330 11 234 56  → Year 2025, Day 330, Month 11, Random 234-56
```

**Breakdown:**
- All generated on same day share date prefix (2025 + 329 + 11)
- Random components (708-04, 815-92, 234-56) ensure uniqueness
- 810,000 possible combinations per day

### B. Input/Output Excel Structure
**INPUT:**
| 주문번호 | 고객명 | 상품명 | 배송주소 |
|---------|--------|---------|----------|
| ORD001 | 김철수 | iPhone 15 | 서울시 강남구... |
| ORD002 | 이영희 | AirPods | 부산시 해운대구... |

**OUTPUT:**
| 주문고유코드 | 송장번호 | 택배사 | 고객명 | 상품명 | 배송주소 |
|--------------|----------|--------|--------|---------|----------|
| ORD001 | 20253291170804 | 경동택배 | 김철수 | iPhone 15 | 서울시 강남구... |
| ORD002 | 20253291180925 | 경동택배 | 이영희 | AirPods | 부산시 해운대구... |

**Note:** Output always starts with three fixed columns (주문고유코드, 송장번호, 택배사), followed by all other original columns.

---

**Document Version:** 1.0
**Last Updated:** 2025-10-27
**Status:** Ready for Development
