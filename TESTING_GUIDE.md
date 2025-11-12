# TrackingGeneratorControl Testing Guide

## Application Status
✅ **Build**: Successful (0 errors, 0 warnings)
✅ **Runtime**: Application launched
⏳ **Testing**: Ready for user testing

## How to Run
```bash
cd "C:\Users\Mi.Stay\OneDrive\Coding\Auto_generate_trackingID\dotnet9\TestApp"
dotnet run
```

Or double-click:
```
C:\Users\Mi.Stay\OneDrive\Coding\Auto_generate_trackingID\dotnet9\TestApp\bin\Debug\net9.0-windows\TestApp.exe
```

## Testing Checklist

### Visual Verification
- [ ] **Title**: "가송장 생성기" displays in dark gray (28px bold)
- [ ] **Status**: "📂 파일을 선택하세요" displays in medium gray (14px)
- [ ] **Dividers**: Two gray horizontal lines visible
- [ ] **File Status Box**: Light gray box with "파일 상태" and "대기 중"
- [ ] **Progress Box**: Hidden initially, appears during generation
- [ ] **Buttons**: Three buttons in a row (blue primary, two gray secondary)
- [ ] **Korean Text**: All Korean characters render correctly (no squares/corruption)
- [ ] **Layout**: Clean, centered, no overlapping elements

### Button Functionality

#### 1. File Upload Button (📂 파일 선택)
**Initial State**:
- [ ] Blue background (#2563EB)
- [ ] White text
- [ ] Clickable (hand cursor)

**Testing**:
1. Click button
2. [ ] File dialog opens
3. Select an Excel file (.xlsx or .xls)
4. [ ] Status changes to "✅ 파일 로드 완료 (N개 항목)"
5. [ ] Status color changes to green
6. [ ] File status text shows "N개 준비"
7. [ ] "송장 생성" button becomes enabled (white background → clickable)

**Error Cases**:
- [ ] Empty file: Shows warning message
- [ ] Invalid file: Shows error message
- [ ] Cancel dialog: No changes to UI

#### 2. Generate Button (🔄 송장 생성)
**Initial State**:
- [ ] Disabled (grayed out)
- [ ] Gray background (#F3F4F6)
- [ ] Dark gray text

**After File Upload**:
- [ ] Enabled
- [ ] Clickable

**Testing**:
1. Click button after uploading file
2. [ ] All buttons disable temporarily
3. [ ] Progress box appears
4. [ ] Progress bar animates from 0% to 100%
5. [ ] Progress text updates: "0 / N 개 생성 중..." → "N / N 개 생성 완료"
6. [ ] Status changes to "✅ 송장번호 생성 완료"
7. [ ] Progress box hides
8. [ ] "Excel 다운로드" button becomes enabled
9. [ ] "파일 선택" button re-enabled

**Error Cases**:
- [ ] Click without file: Shows info message "먼저 Excel 파일을 선택하세요"

#### 3. Download Button (💾 Excel 다운로드)
**Initial State**:
- [ ] Disabled
- [ ] Gray background
- [ ] Dark gray text

**After Generation**:
- [ ] Enabled
- [ ] Clickable

**Testing**:
1. Click button after generating tracking numbers
2. [ ] Save file dialog opens
3. [ ] Default filename: "가송장_생성기_YYYYMMDD_HHMMSS.xlsx"
4. Save to a location
5. [ ] Status changes to "✅ 파일 저장 완료"
6. [ ] Success message box shows saved filename
7. [ ] UI resets for new operation
8. [ ] Open saved Excel file and verify:
   - [ ] All original columns present
   - [ ] New "송장번호" column added
   - [ ] Tracking numbers in format: KD-20251106-XXXXXXXX

**Error Cases**:
- [ ] Click before generation: Shows info message "먼저 송장번호를 생성하세요"
- [ ] Cancel dialog: No changes to UI

### Progress Animation
During tracking number generation:
- [ ] Progress bar fills smoothly (not jumpy)
- [ ] Progress text updates incrementally
- [ ] Animation completes before hiding
- [ ] No visual glitches or flashing

### Window Resize
- [ ] Minimum window size: 700x500
- [ ] Layout stable at minimum size
- [ ] Layout stable at larger sizes
- [ ] No text cutoff or overlap
- [ ] All controls remain visible

### State Management
Test the complete workflow multiple times:

**Workflow 1**: Complete cycle
1. [ ] Upload file
2. [ ] Generate tracking numbers
3. [ ] Download Excel
4. [ ] UI resets correctly
5. [ ] Can repeat process

**Workflow 2**: Cancel operations
1. [ ] Upload file
2. [ ] Upload different file (replaces first)
3. [ ] Generate tracking numbers
4. [ ] Cancel save dialog
5. [ ] Can still download
6. [ ] Download works

**Workflow 3**: Error handling
1. [ ] Try to generate without file (blocked)
2. [ ] Try to download without generating (blocked)
3. [ ] Upload invalid file (error message)
4. [ ] UI recovers correctly

### Performance
- [ ] File upload: < 5 seconds for 100 rows
- [ ] Tracking generation: < 3 seconds for 100 rows
- [ ] File download: < 5 seconds for 100 rows
- [ ] UI remains responsive throughout

### Accessibility
- [ ] Tab navigation works (Upload → Generate → Download)
- [ ] Enter key triggers focused button
- [ ] Cursor changes to hand on buttons
- [ ] Button states clear (enabled/disabled)

## Known Issues to Verify Fixed
- [x] Custom painted controls removed
- [x] Text overlap/corruption eliminated
- [x] Button clicks work reliably
- [x] Korean text renders correctly
- [x] Layout stable at all sizes
- [x] No AutoSize chain issues

## Test Excel Files
Create test files with:
- **Small**: 10 rows
- **Medium**: 100 rows
- **Large**: 1000 rows
- **Mixed**: Different delivery companies (직접전달, 경동택배)

Required columns in test Excel:
- 주문번호 (Order Number)
- 상품명 (Product Name)
- 수령인 (Recipient)
- 배송사 (Delivery Company)
- 기타 필요 컬럼들...

## Success Criteria
All checkboxes above should be checked (✅) for successful validation.

## Bug Reporting Template
If issues found:
```
**Issue**: [Brief description]
**Steps**:
1. [Step to reproduce]
2. [Step to reproduce]
**Expected**: [What should happen]
**Actual**: [What actually happened]
**Screenshot**: [If applicable]
```

## Next Steps After Testing
1. If all tests pass → Publish release build
2. If issues found → Document and fix
3. Update installer package
4. Deploy to production

## Build Commands

**Debug Build**:
```bash
cd dotnet9/TestApp
dotnet build
```

**Release Build**:
```bash
cd dotnet9/TestApp
dotnet publish -c Release -r win-x64 --self-contained
```

**Installer**:
```bash
cd dotnet
iscc "가송장생성기_installer.iss"
```
