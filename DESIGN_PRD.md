# 🎨 Design PRD
## 가송장 생성기 UI/UX Specification

---

## 1. Design Philosophy

```
Principle: "Simplicity meets purpose"
- 1 screen, 3 buttons, infinite functionality
- Zero learning curve
- One-click workflow
- Instant feedback
```

---

## 2. Design System

### 2.1 Color Palette

Based on **shadcn/ui** and **Tailwind CSS** design language:

```
┌─────────────────────────────────────────────────┐
│ PRIMARY COLORS                                  │
├─────────────────────────────────────────────────┤
│ Primary Blue      #2563EB  rgb(37, 99, 235)    │
│   Usage: CTAs, hover states, active elements  │
│   Hex: #2563EB / Tailwind: blue-600           │
├─────────────────────────────────────────────────┤
│ PRIMARY COLORS (LIGHT)                          │
├─────────────────────────────────────────────────┤
│ Light Blue       #DBEAFE  rgb(219, 238, 254)  │
│   Usage: Hover backgrounds, light states      │
│   Hex: #DBEAFE / Tailwind: blue-100           │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│ FUNCTIONAL COLORS                               │
├─────────────────────────────────────────────────┤
│ Success Green     #10B981  rgb(16, 185, 129)  │
│   Usage: Success messages, valid states       │
│   Hex: #10B981 / Tailwind: emerald-500        │
├─────────────────────────────────────────────────┤
│ Success Light    #D1FAE5  rgb(209, 250, 229)  │
│   Usage: Success backgrounds                  │
│   Hex: #D1FAE5 / Tailwind: emerald-100        │
├─────────────────────────────────────────────────┤
│ Warning Amber    #F59E0B  rgb(245, 158, 11)   │
│   Usage: Alerts, warnings                     │
│   Hex: #F59E0B / Tailwind: amber-500          │
├─────────────────────────────────────────────────┤
│ Warning Light    #FEF3C7  rgb(254, 243, 199)  │
│   Usage: Warning backgrounds                  │
│   Hex: #FEF3C7 / Tailwind: amber-100          │
├─────────────────────────────────────────────────┤
│ Error Red        #EF4444  rgb(239, 68, 68)    │
│   Usage: Errors, critical states              │
│   Hex: #EF4444 / Tailwind: red-500            │
├─────────────────────────────────────────────────┤
│ Error Light      #FEE2E2  rgb(254, 226, 226)  │
│   Usage: Error backgrounds                    │
│   Hex: #FEE2E2 / Tailwind: red-100            │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│ NEUTRAL COLORS                                  │
├─────────────────────────────────────────────────┤
│ Background      #FFFFFF  rgb(255, 255, 255)   │
│   Usage: Main background                      │
│   Hex: #FFFFFF / Tailwind: white              │
├─────────────────────────────────────────────────┤
│ Surface Light   #F9FAFB  rgb(249, 250, 251)   │
│   Usage: Card/panel backgrounds               │
│   Hex: #F9FAFB / Tailwind: gray-50            │
├─────────────────────────────────────────────────┤
│ Border Color    #E5E7EB  rgb(229, 231, 235)   │
│   Usage: Borders, dividers                    │
│   Hex: #E5E7EB / Tailwind: gray-200           │
├─────────────────────────────────────────────────┤
│ Text Primary    #1F2937  rgb(31, 41, 55)      │
│   Usage: Main text, headings                  │
│   Hex: #1F2937 / Tailwind: gray-800           │
├─────────────────────────────────────────────────┤
│ Text Secondary  #6B7280  rgb(107, 114, 128)   │
│   Usage: Secondary text, hints                │
│   Hex: #6B7280 / Tailwind: gray-500           │
├─────────────────────────────────────────────────┤
│ Text Tertiary   #9CA3AF  rgb(156, 163, 175)   │
│   Usage: Disabled text, placeholders          │
│   Hex: #9CA3AF / Tailwind: gray-400           │
└─────────────────────────────────────────────────┘
```

### 2.2 Typography

**Font Family:**
- Primary: `-apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", sans-serif`
- Fallback: Arial, sans-serif

```
┌──────────────────────────────────────┐
│ HEADING STYLES                       │
├──────────────────────────────────────┤
│ H1: 28px, Bold (700), Line-height 1.2│
│     Color: #1F2937 (gray-800)       │
│     Usage: Main title                │
├──────────────────────────────────────┤
│ H2: 24px, Bold (700), Line-height 1.3│
│     Color: #1F2937 (gray-800)       │
│     Usage: Section headers           │
├──────────────────────────────────────┤
│ H3: 20px, Semi-bold (600)            │
│     Color: #1F2937 (gray-800)       │
│     Usage: Subheaders               │
├──────────────────────────────────────┤
│ Body: 14px, Regular (400)            │
│       Color: #6B7280 (gray-600)     │
│       Usage: Body text               │
├──────────────────────────────────────┤
│ Label: 12px, Medium (500)            │
│        Color: #374151 (gray-700)    │
│        Usage: Labels, captions      │
├──────────────────────────────────────┤
│ Code: 12px, Monospace (Courier New)  │
│       Color: #1F2937 (gray-800)     │
│       Usage: Tracking numbers       │
└──────────────────────────────────────┘
```

### 2.3 Spacing System

Based on **Tailwind** 4px grid:

```
xs  = 4px   (gap-1)
sm  = 8px   (gap-2)
md  = 16px  (gap-4)
lg  = 24px  (gap-6)
xl  = 32px  (gap-8)
2xl = 48px  (gap-12)
```

**Application:**
- Padding: md (16px)
- Button spacing: sm (8px)
- Section spacing: lg (24px)
- Card spacing: md (16px)

### 2.4 Border Radius

```
None      = 0px       (square)
sm        = 4px       (minimal curve)
md        = 8px       (standard, default for most elements)
lg        = 12px      (generous curve)
full      = 9999px    (perfect circle)
```

**Application:**
- Buttons: `md` (8px)
- Input fields: `md` (8px)
- Cards/panels: `lg` (12px)
- Icons: `full` (circular)

### 2.5 Shadows

Based on **shadcn** shadow system:

```
sm    = 0 1px 2px 0 rgba(0,0,0,0.05)
md    = 0 4px 6px -1px rgba(0,0,0,0.1)
lg    = 0 10px 15px -3px rgba(0,0,0,0.1)
xl    = 0 20px 25px -5px rgba(0,0,0,0.1)
```

**Application:**
- Default state: `md`
- Hover state: `lg`
- Elevated panels: `lg`
- Dropdowns: `md`

---

## 3. Component Library (shadcn-inspired)

### 3.1 Button Component

**States:**
- Default
- Hover
- Active/Pressed
- Disabled
- Loading

**Variants:**

```yaml
Primary (CTA):
  Background: #2563EB (blue-600)
  Text: #FFFFFF (white)
  Hover: #1D4ED8 (blue-700)
  Active: #1E40AF (blue-800)
  Border: none
  Shadow: md

Secondary:
  Background: #F3F4F6 (gray-100)
  Text: #1F2937 (gray-800)
  Hover: #E5E7EB (gray-200)
  Border: 1px #E5E7EB (gray-200)

Danger:
  Background: #EF4444 (red-500)
  Text: #FFFFFF (white)
  Hover: #DC2626 (red-600)
  Border: none
```

**Code Implementation (PyQt5 QSS):**

```qss
QPushButton {
    background-color: #2563EB;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 12px 20px;
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
}

QPushButton:hover {
    background-color: #1D4ED8;
    border: none;
}

QPushButton:pressed {
    background-color: #1E40AF;
}

QPushButton:disabled {
    background-color: #9CA3AF;
    color: #D1D5DB;
}
```

### 3.2 Input Field Component

**States:**
- Default
- Focus
- Filled
- Error
- Disabled

**Code Implementation (PyQt5):**

```qss
QLineEdit {
    border: 1px solid #E5E7EB;
    border-radius: 8px;
    padding: 10px 12px;
    font-size: 14px;
    background-color: #FFFFFF;
    color: #1F2937;
}

QLineEdit:focus {
    border: 2px solid #2563EB;
    outline: none;
    background-color: #F0F7FF;
}

QLineEdit:disabled {
    background-color: #F9FAFB;
    color: #9CA3AF;
}
```

### 3.3 Progress Bar Component

**Usage:** Show loading/generation progress

```qss
QProgressBar {
    border: 1px solid #E5E7EB;
    border-radius: 8px;
    background-color: #F3F4F6;
    height: 6px;
    text-align: center;
}

QProgressBar::chunk {
    background-color: #2563EB;
    border-radius: 6px;
}
```

### 3.4 Label Component

**Typography variants:**
- Heading: 18px, bold
- Body: 14px, regular
- Caption: 12px, medium
- Code: 12px, monospace

```qss
/* Heading */
QLabel.heading {
    font-size: 18px;
    font-weight: bold;
    color: #1F2937;
}

/* Body */
QLabel.body {
    font-size: 14px;
    color: #6B7280;
}

/* Status */
QLabel.status {
    font-size: 14px;
    color: #10B981;
}
```

### 3.5 Message Box Component

**Success Message:**
```
Background: #D1FAE5 (emerald-100)
Text: #065F46 (emerald-900)
Border: 1px solid #6EE7B7 (emerald-300)
Icon: ✅
```

**Error Message:**
```
Background: #FEE2E2 (red-100)
Text: #7F1D1D (red-900)
Border: 1px solid #FCA5A5 (red-300)
Icon: ❌
```

**Warning Message:**
```
Background: #FEF3C7 (amber-100)
Text: #78350F (amber-900)
Border: 1px solid #FCD34D (amber-300)
Icon: ⚠️
```

---

## 4. Layout & Wireframe

### 4.1 Main Screen Layout

```
┌─────────────────────────────────────────────────────┐
│                                                     │
│  가송장 생성기 (경동택배)                            │ ← H1, margin-bottom: lg
│                                                     │
├─────────────────────────────────────────────────────┤
│                                                     │
│  📂 파일을 선택하세요                               │ ← Status label, gray-600
│  (또는 "✅ 파일 로드됨: 100 개 주문")              │
│                                                     │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌───────────────────────────────────────────────┐ │
│  │ ▓▓▓▓▓▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ │ │ ← Progress bar (hidden until generating)
│  │ 50 / 100 개 생성 중...                       │ │
│  └───────────────────────────────────────────────┘ │
│                                                     │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐│
│  │ 📂 파일 선택 │ │ 🔄 송장 생성 │ │ 💾 Excel   ││
│  │              │ │ (disabled)   │ │ 다운로드    ││
│  │ Primary      │ │ Secondary    │ │ (disabled) ││
│  └──────────────┘ └──────────────┘ └──────────────┘│
│                                                     │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### 4.2 Responsive Design

**Desktop (800x600 minimum):**
- 3 buttons in horizontal row
- Full visibility of all elements
- Comfortable spacing

**Tablet (600x800):**
- Buttons may wrap to 2 rows if needed
- Adjusted padding

**Not optimized for:**
- Mobile (under 600px)
- Touch interface (designed for mouse/trackpad)

---

## 5. User Interaction Flows

### 5.1 Initial State

```
┌──────────────────────┐
│ Application Opened   │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────────────────────────────┐
│ State:                                       │
│ - Status: "📂 파일을 선택하세요"            │
│ - Button 1: ENABLED (upload)                │
│ - Button 2: DISABLED (generate)             │
│ - Button 3: DISABLED (download)             │
│ - Progress: HIDDEN                          │
└──────────────────────────────────────────────┘
```

### 5.2 After File Upload

```
┌──────────────────────┐
│ User clicks "파일 선택"│
└──────┬───────────────┘
       │
       ▼
┌──────────────────────────────────────────────┐
│ File Dialog Opens → User selects .xlsx file  │
└──────┬───────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────────┐
│ Validation:                                  │
│ ✓ File format valid                        │
│ ✓ File not empty                           │
│ ✓ Columns detected                         │
└──────┬───────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────────┐
│ State:                                       │
│ - Status: "✅ 파일 로드됨: 150 개 주문"      │
│ - Button 1: ENABLED                        │
│ - Button 2: ENABLED ← Changed!             │
│ - Button 3: DISABLED                       │
│ - Progress: HIDDEN                         │
└──────────────────────────────────────────────┘
```

### 5.3 During Number Generation

```
┌──────────────────────┐
│ User clicks "송장 생성"│
└──────┬───────────────┘
       │
       ▼
┌──────────────────────────────────────────────┐
│ UI Update:                                   │
│ - Button 2: DISABLED (prevent double-click) │
│ - Progress: VISIBLE                        │
│ - Status: "50 / 150 개 생성 중..."          │
└──────┬───────────────────────────────────────┘
       │
       ▼ (Processing)
       │ (1-2 seconds)
       │
       ▼
┌──────────────────────────────────────────────┐
│ Completion:                                  │
│ - Status: "✅ 150 개 송장번호 생성 완료"    │
│ - Progress: HIDDEN                         │
│ - Button 2: DISABLED (task complete)       │
│ - Button 3: ENABLED ← Changed!             │
└──────────────────────────────────────────────┘
```

### 5.4 After Excel Export

```
┌──────────────────────┐
│ User clicks "Excel 다운로드"│
└──────┬───────────────┘
       │
       ▼
┌──────────────────────────────────────────────┐
│ Save Dialog Opens                            │
│ Filename: 가송장_생성기_20251027_153045.xlsx│
└──────┬───────────────────────────────────────┘
       │
       ▼ (Processing)
       │ (1-2 seconds)
       │
       ▼
┌──────────────────────────────────────────────┐
│ Success Message:                             │
│ ✅ 파일 저장됨: /Downloads/가송장_생성기...  │
└──────┬───────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────────┐
│ Reset:                                       │
│ - Return to Initial State                   │
│ - Clear file data                          │
│ - Clear generated numbers                  │
└──────────────────────────────────────────────┘
```

---

## 6. Visual Design Details

### 6.1 Window Design

```
┌─────────────────────────────────────────────────┐
│ ✕ 가송장 생성기                    _ □ ✕       │ ← Title bar (system)
├─────────────────────────────────────────────────┤
│                                                 │
│  Padding: 32px (horizontal), 24px (vertical)   │
│                                                 │
│  ┌──────────────────────────────────────────┐  │
│  │ 가송장 생성기 (경동택배)                 │  │
│  │ (H1, 28px, Bold, #1F2937)                │  │
│  │ Margin-bottom: 24px                      │  │
│  └──────────────────────────────────────────┘  │
│                                                 │
│  ┌──────────────────────────────────────────┐  │
│  │ 📂 파일을 선택하세요                      │  │
│  │ (Body, 14px, #6B7280)                    │  │
│  │ Margin-bottom: 16px                      │  │
│  └──────────────────────────────────────────┘  │
│                                                 │
│  ┌──────────────────────────────────────────┐  │
│  │ [Progress bar - initially hidden]        │  │
│  │ Margin-bottom: 24px                      │  │
│  └──────────────────────────────────────────┘  │
│                                                 │
│  ┌──────────────────────────────────────────┐  │
│  │  Button Row (horizontal, spacing: 8px)  │  │
│  │  ┌─────────────┐ ┌─────────────┐ ┌──────┐ │
│  │  │ 📂 파일선택 │ │ 🔄 송장생성 │ │ 💾  │ │
│  │  │ (enabled)   │ │ (disabled)  │ │ 다운 │ │
│  │  └─────────────┘ └─────────────┘ │로드 │ │
│  │                                    │     │ │
│  │                                    │(dis)│ │
│  │                                    └──────┘ │
│  └──────────────────────────────────────────┘  │
│                                                 │
│  Flex: 1 (grows to fill space)                │
│                                                 │
└─────────────────────────────────────────────────┘

Window Size: 800px × 600px (minimum)
Font: System default (14px base)
Background: #FFFFFF (white)
Border: 1px #E5E7EB (gray-200)
```

### 6.2 Button Design Detail

**Button Dimensions:**
- Height: 44px (accessibility: touch target)
- Min-width: 120px
- Padding: 12px 20px
- Icon: 18px (if included)

**Button States Visual:**

```
NORMAL STATE:
┌──────────────────────┐
│  📂 파일 선택        │
│  (Blue bg, white txt)│
│  (Shadow: md)        │
└──────────────────────┘

HOVER STATE:
┌──────────────────────┐ ← Border glow
│  📂 파일 선택        │
│  (Darker blue bg)    │
│  (Shadow: lg)        │
└──────────────────────┘

ACTIVE/PRESSED STATE:
┌──────────────────────┐
│  📂 파일 선택        │
│  (Even darker blue)  │
│  (Shadow: sm - shrink)
└──────────────────────┘

DISABLED STATE:
┌──────────────────────┐
│  📂 파일 선택        │
│  (Gray bg, gray txt) │
│  (No shadow)         │
│  (Opacity: 0.6)      │
└──────────────────────┘

LOADING STATE:
┌──────────────────────┐
│  ⟳ 생성 중...        │ ← Spinner animation
│  (Blue bg)           │
└──────────────────────┘
```

### 6.3 Alert Messages

**Success Alert:**
```
┌─────────────────────────────────────────────┐
│ ✅ 파일 저장됨: 가송장_생성기_20251027.xlsx  │
├─────────────────────────────────────────────┤
│ Background: #D1FAE5 (emerald-100)          │
│ Text: #065F46 (emerald-900)                │
│ Border: 1px solid #6EE7B7                  │
│ Icon: ✅ (18px)                            │
│ Padding: 12px 16px                         │
│ Border-radius: 8px                         │
│ Duration: 3 seconds (auto-dismiss)         │
└─────────────────────────────────────────────┘
```

**Error Alert:**
```
┌─────────────────────────────────────────────┐
│ ❌ 오류: 파일이 손상되었습니다              │
├─────────────────────────────────────────────┤
│ Background: #FEE2E2 (red-100)              │
│ Text: #7F1D1D (red-900)                    │
│ Border: 1px solid #FCA5A5                  │
│ Icon: ❌ (18px)                            │
│ Padding: 12px 16px                         │
│ Border-radius: 8px                         │
│ Duration: 5 seconds (wait for user dismiss)│
└─────────────────────────────────────────────┘
```

---

## 7. Accessibility (A11Y)

### 7.1 WCAG 2.1 AA Compliance

- ✅ **Contrast Ratio:** All text ≥ 4.5:1 (AAA for buttons)
- ✅ **Focus Indicators:** Visible focus ring (2px blue)
- ✅ **Keyboard Navigation:** Tab/Shift+Tab works
- ✅ **Color Contrast:**
  - Text: #1F2937 on #FFFFFF = 18:1 ✓
  - Button text: #FFFFFF on #2563EB = 8.5:1 ✓
  - Status text: #6B7280 on #FFFFFF = 6:1 ✓

### 7.2 Keyboard Navigation

| Key | Action |
|-----|--------|
| Tab | Next element |
| Shift+Tab | Previous element |
| Enter/Space | Activate button |
| Escape | Cancel dialog |

### 7.3 Screen Reader Support

- Button labels: Clear and descriptive
- Status updates: Announced
- Progress: Numeric feedback
- Error messages: Focused

---

## 8. Dark Mode (Optional Future)

**Dark Mode Palette:**
```
Background: #1F2937 (gray-800)
Surface: #111827 (gray-900)
Text Primary: #F9FAFB (gray-50)
Text Secondary: #D1D5DB (gray-300)
Border: #374151 (gray-700)
Primary Button: #3B82F6 (blue-500)
```

---

## 9. Animation & Microinteractions

### 9.1 Button Interactions

```
Hover:
- Duration: 200ms
- Effect: Color fade + shadow increase
- Easing: ease-in-out

Press:
- Duration: 100ms
- Effect: Slight scale (0.98x)
- Feedback: Immediate

Disabled:
- Opacity: 60%
- Cursor: not-allowed
- No hover effect
```

### 9.2 Progress Bar

```
Animation:
- Smooth fill from 0% to 100%
- Duration: varies (1-3 seconds)
- Easing: linear
- Color: #2563EB
```

### 9.3 Message Notifications

```
Slide In:
- Origin: top-center
- Duration: 300ms
- Easing: ease-out
- Distance: 20px slide down

Auto Dismiss:
- Delay: 3 seconds (success), 5 seconds (error)
- Fade out: 200ms

Manual Close:
- Click X button or anywhere outside
```

---

## 10. Design System Documentation

### 10.1 Component Usage Examples

**Button Primary:**
```python
button = QPushButton("📂 파일 선택")
button.setStyleSheet("""
    QPushButton {
        background-color: #2563EB;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 20px;
        font-size: 14px;
        font-weight: 500;
    }
    QPushButton:hover {
        background-color: #1D4ED8;
    }
    QPushButton:pressed {
        background-color: #1E40AF;
    }
""")
```

**Status Label:**
```python
status = QLabel("✅ 파일 로드됨: 100 개 주문")
status.setStyleSheet("""
    QLabel {
        color: #10B981;
        font-size: 14px;
        font-weight: 500;
    }
""")
```

### 10.2 Color Reference for Developers

| Element | Color Code | Usage |
|---------|-----------|-------|
| Primary Button | #2563EB | Main CTA |
| Button Hover | #1D4ED8 | Hover state |
| Success Text | #10B981 | Success messages |
| Error Text | #EF4444 | Error messages |
| Disabled Button | #9CA3AF | Disabled state |
| Border | #E5E7EB | Dividers, borders |
| Text | #1F2937 | Main text |
| Text Secondary | #6B7280 | Secondary text |

---

## 11. File Naming & Export Design

### 11.1 Output File Naming Convention

```
Format: 가송장_생성기_[DATE]_[TIME].[EXT]
Example: 가송장_생성기_20251027_153045.xlsx

Components:
- Prefix: "가송장_생성기" (fixed)
- Date: YYYYMMDD format
- Time: HHMMSS format (24-hour)
- Extension: .xlsx (Excel format)

Rationale:
- Easy to identify application
- Chronologically sortable
- Unique per execution
- Professional appearance
```

### 11.2 Output Excel Formatting

**Column Order (Fixed):**
1. **주문고유코드** (Order ID) - From first column of input
2. **송장번호** (Tracking Number) - Generated 14-digit number
3. **택배사** (Delivery Company) - Always "경동택배"
4. All remaining original columns from input file

**Column Headers:**
- Font: Bold, 12px
- Background: #F3F4F6 (gray-100)
- Text Color: #1F2937 (gray-800)
- Border: 1px solid #E5E7EB

**Data Rows:**
- Font: Regular, 12px
- Background: #FFFFFF (white, alternate #F9FAFB)
- Text Color: #1F2937 (gray-800)

**주문고유코드 Column:**
- Font: Regular, 12px
- Alignment: Left
- Content: From first column of input file

**송장번호 Column (Tracking Number):**
- Font: Monospace (Courier New), 12px
- Alignment: Center
- Format: 14-digit number (e.g., "20253291170804")
- Example: Year 2025, Day 329, Month 11, Random 708-04

**택배사 Column:**
- Font: Regular, 12px
- Text: "경동택배" (fixed value)
- Alignment: Center

**Column Widths:**
- Auto-adjust based on content
- Minimum: 100px
- Maximum: 300px
- 송장번호: 150px (fixed-width font for readability)

---

## 12. Design Checklist

- [ ] Colors match Tailwind/shadcn palette
- [ ] Typography follows specification
- [ ] Button states fully implemented
- [ ] Spacing uses 4px grid system
- [ ] Focus indicators visible
- [ ] Error messages clear
- [ ] Success feedback provided
- [ ] Loading state shown
- [ ] All buttons labeled in Korean
- [ ] Window size: 800x600 minimum
- [ ] Icons included (emoji)
- [ ] Hover effects smooth
- [ ] Disabled states clear
- [ ] Progress bar animated
- [ ] Message notifications auto-dismiss
- [ ] Output filename convention followed

---

## 13. Design Review Checklist

**Visual Design:**
- [ ] Consistent color usage
- [ ] Typography hierarchy clear
- [ ] Whitespace adequate
- [ ] No visual clutter
- [ ] Professional appearance

**Interaction Design:**
- [ ] Button purpose obvious
- [ ] Status clear at all times
- [ ] Feedback immediate
- [ ] Error recovery clear
- [ ] User never confused

**Accessibility:**
- [ ] WCAG 2.1 AA compliant
- [ ] Keyboard navigable
- [ ] Screen reader compatible
- [ ] Color contrast adequate
- [ ] Focus visible

**User Experience:**
- [ ] One-click workflow
- [ ] Zero learning curve
- [ ] Fast feedback
- [ ] No errors possible
- [ ] Delightful to use

---

**Design PRD Version:** 1.0
**Last Updated:** 2025-10-27
**Status:** Ready for Implementation

**Design System Reference:**
- 🎨 [Tailwind CSS](https://tailwindcss.com/)
- 🧩 [shadcn/ui](https://ui.shadcn.com/)
- ♿ [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
