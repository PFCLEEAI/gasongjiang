# 🔧 Technical Specification
## 가송장 생성기 (Tracking Number Generator)

---

## 1. System Architecture

```
┌─────────────────────────────────────────────────────┐
│                User Interface (PyQt5)               │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐│
│  │ Upload Button│ │ Generate Btn │ │ Download Btn ││
│  └──────────────┘ └──────────────┘ └──────────────┘│
└──────────────────────┬──────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────┐
│            Application Logic Layer                  │
│  ┌────────────────────────────────────────────┐   │
│  │ ExcelUploadHandler                        │   │
│  │ - Validate file format                    │   │
│  │ - Parse Excel data                        │   │
│  │ - Handle errors gracefully                │   │
│  └────────────────────────────────────────────┘   │
│  ┌────────────────────────────────────────────┐   │
│  │ TrackingNumberGenerator                   │   │
│  │ - Generate unique numbers                 │   │
│  │ - Check for duplicates                    │   │
│  │ - Maintain uniqueness history             │   │
│  └────────────────────────────────────────────┘   │
│  ┌────────────────────────────────────────────┐   │
│  │ ExcelExportHandler                        │   │
│  │ - Create output file                      │   │
│  │ - Assign tracking numbers                 │   │
│  │ - Add metadata (택배사)                    │   │
│  └────────────────────────────────────────────┘   │
└──────────────────────┬──────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────┐
│              Data Storage Layer                     │
│  ┌────────────────────────────────────────────┐   │
│  │ File System                               │   │
│  │ - Input Excel files                       │   │
│  │ - Output Excel files                      │   │
│  │ - History/Cache (optional)                │   │
│  └────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

---

## 2. Tech Stack

| Layer | Technology | Version | Reason |
|-------|-----------|---------|--------|
| **UI Framework** | PyQt5 | 5.15+ | Modern, cross-platform, responsive |
| **Excel Processing** | openpyxl | 3.9+ | Full .xlsx support, preserves formatting |
| **Data Handling** | pandas | 2.0+ | Easy row/column manipulation |
| **Randomization** | secrets + random | Built-in | Cryptographically secure random numbers |
| **File Dialogs** | PyQt5.QtWidgets | 5.15+ | Native OS file picker |
| **Data Validation** | pydantic | 2.0+ | Type checking, validation |

---

## 3. Module Structure

```
가송장_생성기/
├── main.py                 # Application entry point
├── src/
│   ├── __init__.py
│   ├── ui/
│   │   ├── __init__.py
│   │   └── main_window.py  # PyQt5 UI components
│   ├── core/
│   │   ├── __init__.py
│   │   ├── tracking_generator.py      # Core number generation logic
│   │   ├── uniqueness_checker.py      # Collision detection
│   │   └── history_manager.py         # Track used numbers
│   ├── handlers/
│   │   ├── __init__.py
│   │   ├── excel_uploader.py          # Upload and parse Excel
│   │   └── excel_exporter.py          # Create output Excel
│   └── utils/
│       ├── __init__.py
│       ├── validators.py              # Input validation
│       ├── logger.py                  # Logging utility
│       └── constants.py               # App constants
├── resources/
│   ├── styles.qss                     # PyQt5 stylesheet
│   └── icons/                         # UI icons (optional)
├── tests/
│   ├── test_tracking_generator.py
│   ├── test_excel_handler.py
│   └── test_uniqueness.py
├── requirements.txt
├── setup.py
└── README.md
```

---

## 4. Core Algorithms

### 4.1 Tracking Number Generation

```python
def generate_tracking_number(session_id: int) -> str:
    """
    Generate unique 14-digit tracking number

    Format: YYYY + XXXX + XXXXXX
    - YYYY: Current year (e.g., 2025)
    - XXXX: Session-specific 4-digit random ID
    - XXXXXX: Order-specific 6-digit random number

    Returns:
        str: 14-digit tracking number (e.g., "20254661035527")
    """
    year = datetime.now().year

    # Generate session ID (random, 4 digits: 1000-9999)
    session_part = secrets.randbelow(9000) + 1000

    # Generate sequence (random, 6 digits: 000000-999999)
    sequence_part = secrets.randbelow(1000000)

    # Format: YYYY + XXXX + XXXXXX
    tracking_number = f"{year}{session_part:04d}{sequence_part:06d}"

    return tracking_number
```

**Logic Explanation:**
- `Year Component (2025)`: Always current year
- `Session ID (4 digits)`: Random per application session (ensures different users get different numbers)
- `Sequence (6 digits)`: Random per order (ensures high uniqueness)
- **Total Combinations:** 9000 × 1,000,000 = 9 billion possible numbers

---

### 4.2 Uniqueness Validation

```python
class UniquenessChecker:
    def __init__(self, history_file: str = "number_history.json"):
        self.history_file = history_file
        self.used_numbers = self._load_history()

    def is_unique(self, number: str) -> bool:
        """Check if number hasn't been used before"""
        return number not in self.used_numbers

    def register_number(self, number: str) -> bool:
        """Register number as used"""
        if not self.is_unique(number):
            return False

        self.used_numbers.add(number)
        self._save_history()
        return True

    def _load_history(self) -> set:
        """Load used numbers from file"""
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r') as f:
                return set(json.load(f))
        return set()

    def _save_history(self):
        """Persist used numbers to file"""
        with open(self.history_file, 'w') as f:
            json.dump(list(self.used_numbers), f)
```

**Collision Detection Strategy:**
1. Check against in-memory set (fast)
2. Check against persistent history (comprehensive)
3. If duplicate: regenerate and retry (max 10 attempts)
4. If 10 failures: alert user (statistically impossible)

---

### 4.3 Batch Generation Algorithm

```python
def generate_batch(num_orders: int, max_retries: int = 10) -> List[str]:
    """
    Generate unique tracking numbers for entire batch

    Args:
        num_orders: Number of tracking numbers needed
        max_retries: Max attempts per number before failure

    Returns:
        List of unique tracking numbers

    Raises:
        GenerationError: If unable to generate unique numbers
    """
    generated = []
    uniqueness_checker = UniquenessChecker()
    session_id = secrets.randbelow(9000) + 1000

    for i in range(num_orders):
        for attempt in range(max_retries):
            number = generate_tracking_number(session_id)

            # Check uniqueness (both in-session and historical)
            if number not in generated and uniqueness_checker.is_unique(number):
                generated.append(number)
                uniqueness_checker.register_number(number)
                break
        else:
            # Failed after max_retries
            raise GenerationError(f"Failed to generate unique number for order {i}")

    return generated
```

---

## 5. Excel Processing

### 5.1 Upload Handler

```python
class ExcelUploadHandler:
    SUPPORTED_FORMATS = ['.xls', '.xlsx']
    MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB

    @staticmethod
    def validate_file(file_path: str) -> bool:
        """Validate file format and size"""
        # Check extension
        if not any(file_path.endswith(fmt) for fmt in ExcelUploadHandler.SUPPORTED_FORMATS):
            raise ValueError(f"Unsupported format. Use {ExcelUploadHandler.SUPPORTED_FORMATS}")

        # Check file size
        if os.path.getsize(file_path) > ExcelUploadHandler.MAX_FILE_SIZE:
            raise ValueError(f"File too large. Max size: {ExcelUploadHandler.MAX_FILE_SIZE}")

        return True

    @staticmethod
    def read_excel(file_path: str) -> pd.DataFrame:
        """Read Excel file and return DataFrame"""
        try:
            df = pd.read_excel(file_path)

            # Validate non-empty
            if df.empty:
                raise ValueError("Excel file is empty")

            return df
        except Exception as e:
            raise ValueError(f"Error reading Excel file: {str(e)}")
```

### 5.2 Export Handler

```python
class ExcelExportHandler:
    DELIVERY_COMPANY = "경동택배"

    @staticmethod
    def create_output(df: pd.DataFrame, tracking_numbers: List[str],
                     output_path: str) -> bool:
        """
        Create output Excel with tracking numbers assigned

        Args:
            df: Original DataFrame from input file
            tracking_numbers: List of generated tracking numbers
            output_path: Path to save output file

        Returns:
            bool: Success status
        """
        # Add tracking numbers column
        df['가송장 번호'] = tracking_numbers

        # Add delivery company column
        df['택배사'] = ExcelExportHandler.DELIVERY_COMPANY

        # Reorder columns: original columns + new columns
        columns = list(df.columns[:-2]) + ['가송장 번호', '택배사']
        df = df[columns]

        # Write to Excel with formatting
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Sheet1')

            # Auto-adjust column widths
            worksheet = writer.sheets['Sheet1']
            for column in worksheet.columns:
                max_length = 0
                column = [cell for cell in column]
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(cell.value)
                    except:
                        pass
                adjusted_width = (max_length + 2)
                worksheet.column_dimensions[column[0].column_letter].width = adjusted_width

        return True
```

---

## 6. UI Implementation (PyQt5)

### 6.1 Main Window Layout

```python
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.current_df = None
        self.generated_numbers = None

    def initUI(self):
        """Initialize user interface"""
        self.setWindowTitle("가송장 생성기")
        self.setGeometry(100, 100, 800, 600)

        # Central widget with layout
        central_widget = QWidget()
        layout = QVBoxLayout()

        # Title
        title = QLabel("가송장 생성기 (경동택배)")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        layout.addWidget(title)

        # Status area
        self.status_label = QLabel("파일을 선택하세요")
        layout.addWidget(self.status_label)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        # Button layout
        button_layout = QHBoxLayout()

        # Button 1: Select File
        self.upload_btn = QPushButton("📂 파일 선택")
        self.upload_btn.clicked.connect(self.upload_file)
        button_layout.addWidget(self.upload_btn)

        # Button 2: Generate Numbers
        self.generate_btn = QPushButton("🔄 송장 생성")
        self.generate_btn.setEnabled(False)
        self.generate_btn.clicked.connect(self.generate_numbers)
        button_layout.addWidget(self.generate_btn)

        # Button 3: Download
        self.download_btn = QPushButton("💾 Excel 다운로드")
        self.download_btn.setEnabled(False)
        self.download_btn.clicked.connect(self.download_excel)
        button_layout.addWidget(self.download_btn)

        layout.addLayout(button_layout)
        layout.addStretch()

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def upload_file(self):
        """Handle file upload"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Excel 파일 선택", "", "Excel Files (*.xls *.xlsx)"
        )

        if file_path:
            try:
                self.current_df = ExcelUploadHandler.read_excel(file_path)
                self.status_label.setText(
                    f"✅ 파일 로드됨: {len(self.current_df)} 개 주문"
                )
                self.generate_btn.setEnabled(True)
            except Exception as e:
                self.show_error(f"파일 로드 실패: {str(e)}")

    def generate_numbers(self):
        """Generate tracking numbers"""
        if self.current_df is None:
            return

        try:
            self.progress_bar.setVisible(True)
            self.generate_btn.setEnabled(False)

            num_orders = len(self.current_df)
            self.progress_bar.setMaximum(num_orders)

            # Generate numbers
            self.generated_numbers = []
            for i in range(num_orders):
                number = TrackingNumberGenerator.generate_unique()
                self.generated_numbers.append(number)
                self.progress_bar.setValue(i + 1)

            self.status_label.setText(
                f"✅ {num_orders} 개 송장번호 생성 완료"
            )
            self.download_btn.setEnabled(True)
            self.progress_bar.setVisible(False)
        except Exception as e:
            self.show_error(f"생성 실패: {str(e)}")

    def download_excel(self):
        """Save output Excel file"""
        if self.current_df is None or self.generated_numbers is None:
            return

        try:
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"가송장_생성기_{timestamp}.xlsx"

            # Show save dialog
            file_path, _ = QFileDialog.getSaveFileName(
                self, "파일 저장", filename, "Excel Files (*.xlsx)"
            )

            if file_path:
                ExcelExportHandler.create_output(
                    self.current_df, self.generated_numbers, file_path
                )
                self.show_success(f"✅ 파일 저장됨: {file_path}")
                self.reset_ui()
        except Exception as e:
            self.show_error(f"저장 실패: {str(e)}")

    def show_error(self, message: str):
        """Show error dialog"""
        QMessageBox.critical(self, "오류", message)

    def show_success(self, message: str):
        """Show success dialog"""
        QMessageBox.information(self, "성공", message)

    def reset_ui(self):
        """Reset UI for next operation"""
        self.current_df = None
        self.generated_numbers = None
        self.generate_btn.setEnabled(False)
        self.download_btn.setEnabled(False)
        self.status_label.setText("파일을 선택하세요")
```

---

## 7. Error Handling Strategy

```python
class ApplicationError(Exception):
    """Base application exception"""
    pass

class FileValidationError(ApplicationError):
    """File validation failed"""
    pass

class GenerationError(ApplicationError):
    """Number generation failed"""
    pass

class ExportError(ApplicationError):
    """Excel export failed"""
    pass

# Error handling with user-friendly messages
ERROR_MESSAGES = {
    FileValidationError: "파일 형식이 잘못되었습니다. .xls 또는 .xlsx 파일을 사용하세요.",
    GenerationError: "송장 생성에 실패했습니다. 다시 시도하세요.",
    ExportError: "파일 저장에 실패했습니다.",
    PermissionError: "파일에 접근할 권한이 없습니다.",
}
```

---

## 8. Testing Strategy

### 8.1 Unit Tests

```python
# test_tracking_generator.py
def test_number_format():
    """Test tracking number format (14 digits)"""
    number = TrackingNumberGenerator.generate()
    assert len(number) == 14
    assert number.isdigit()

def test_uniqueness():
    """Test uniqueness across multiple generations"""
    numbers = set()
    for _ in range(1000):
        number = TrackingNumberGenerator.generate_unique()
        assert number not in numbers
        numbers.add(number)

def test_no_duplicates_in_batch():
    """Test batch generation produces unique numbers"""
    batch = TrackingNumberGenerator.generate_batch(100)
    assert len(batch) == len(set(batch))

# test_excel_handler.py
def test_excel_read_write():
    """Test Excel file reading and writing"""
    df = pd.DataFrame({"주문번호": ["A001", "A002"], "고객명": ["김철수", "이영희"]})
    ExcelExportHandler.create_output(df, ["20251234567890", "20251234567891"], "test.xlsx")
    assert os.path.exists("test.xlsx")
```

### 8.2 Integration Tests

```python
def test_full_workflow():
    """Test complete application workflow"""
    # 1. Upload file
    df = ExcelUploadHandler.read_excel("sample.xlsx")
    assert df is not None

    # 2. Generate numbers
    numbers = TrackingNumberGenerator.generate_batch(len(df))
    assert len(numbers) == len(df)

    # 3. Export
    ExcelExportHandler.create_output(df, numbers, "output.xlsx")
    assert os.path.exists("output.xlsx")
```

---

## 9. Performance Optimization

| Optimization | Implementation |
|--------------|----------------|
| **Number Generation** | Use `secrets` module (cryptographically secure) |
| **Batch Processing** | Generate all at once (not one-by-one) |
| **Uniqueness Check** | In-memory set lookup (O(1) complexity) |
| **File I/O** | Use pandas/openpyxl (optimized) |
| **UI Responsiveness** | Threading for long operations |

---

## 10. Deployment & Distribution

### 10.1 Development Setup

```bash
# Clone/download project
cd 가송장_생성기

# Create virtual environment
python -m venv venv
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run application
python main.py
```

### 10.2 Build as Executable

```bash
# Install PyInstaller
pip install pyinstaller

# Build executable
pyinstaller --onefile --windowed --icon=icon.ico main.py

# Executable location: dist/main.exe (Windows)
```

---

## 11. Database/Storage

**Option 1: File-Based (Current)**
```
number_history.json
[
  "20254661035527",
  "20254441017927",
  ...
]
```

**Option 2: SQLite (Future)**
```sql
CREATE TABLE used_numbers (
    id INTEGER PRIMARY KEY,
    number VARCHAR(14) UNIQUE,
    used_at TIMESTAMP,
    session_id INTEGER
);
```

---

## 12. Security Considerations

- ✅ No external API calls (offline only)
- ✅ No user data collection
- ✅ Input validation for all file uploads
- ✅ Secure random number generation (secrets module)
- ✅ No sensitive data in logs

---

## 13. Dependencies

```txt
# requirements.txt
PyQt5==5.15.9
pandas==2.0.3
openpyxl==3.1.2
pydantic==2.4.2
python-dateutil==2.8.2
```

---

**Technical Specification Version:** 1.0
**Last Updated:** 2025-10-27
**Status:** Ready for Implementation
