"""
Application constants and configuration

This module contains all constant values used throughout the application.
"""

from typing import Final

# Application Info
APP_NAME: Final[str] = "가송장 생성기"
APP_VERSION: Final[str] = "1.0.0"
DELIVERY_COMPANY: Final[str] = "경동택배"

# File Configuration
SUPPORTED_FORMATS: Final[tuple] = ('.xls', '.xlsx')
MAX_FILE_SIZE: Final[int] = 100 * 1024 * 1024  # 100MB in bytes
HISTORY_FILE: Final[str] = "number_history.json"

# Tracking Number Configuration
TRACKING_NUMBER_LENGTH: Final[int] = 14
YEAR_DIGITS: Final[int] = 4
SESSION_DIGITS: Final[int] = 4
SEQUENCE_DIGITS: Final[int] = 6

# Session ID Range (4 digits: 1000-9999)
SESSION_ID_MIN: Final[int] = 1000
SESSION_ID_MAX: Final[int] = 9999

# Sequence Range (6 digits: 000000-999999)
SEQUENCE_MIN: Final[int] = 0
SEQUENCE_MAX: Final[int] = 999999

# Generation Configuration
MAX_RETRY_ATTEMPTS: Final[int] = 10
BATCH_PROGRESS_UPDATE_INTERVAL: Final[int] = 100  # Update UI every N items

# Performance Targets
TARGET_GENERATION_TIME_PER_1000: Final[int] = 1  # seconds
TARGET_TOTAL_TIME_PER_1000: Final[int] = 5  # seconds

# UI Configuration
WINDOW_WIDTH: Final[int] = 800
WINDOW_HEIGHT: Final[int] = 600
WINDOW_MIN_WIDTH: Final[int] = 600
WINDOW_MIN_HEIGHT: Final[int] = 400

# Colors (shadcn/ui + Tailwind CSS)
COLOR_PRIMARY: Final[str] = "#2563EB"  # blue-600
COLOR_PRIMARY_HOVER: Final[str] = "#1D4ED8"  # blue-700
COLOR_PRIMARY_ACTIVE: Final[str] = "#1E40AF"  # blue-800
COLOR_SUCCESS: Final[str] = "#10B981"  # emerald-500
COLOR_ERROR: Final[str] = "#EF4444"  # red-500
COLOR_WARNING: Final[str] = "#F59E0B"  # amber-500
COLOR_TEXT_PRIMARY: Final[str] = "#1F2937"  # gray-800
COLOR_TEXT_SECONDARY: Final[str] = "#6B7280"  # gray-500
COLOR_BACKGROUND: Final[str] = "#FFFFFF"  # white
COLOR_SURFACE: Final[str] = "#F9FAFB"  # gray-50
COLOR_BORDER: Final[str] = "#E5E7EB"  # gray-200
COLOR_DISABLED: Final[str] = "#9CA3AF"  # gray-400

# Excel Column Names
COLUMN_TRACKING_NUMBER: Final[str] = "가송장 번호"
COLUMN_DELIVERY_COMPANY: Final[str] = "택배사"

# Status Messages
MSG_INITIAL: Final[str] = "📂 파일을 선택하세요"
MSG_FILE_LOADED: Final[str] = "✅ 파일 로드됨: {} 개 주문"
MSG_GENERATING: Final[str] = "{} / {} 개 생성 중..."
MSG_GENERATION_COMPLETE: Final[str] = "✅ {} 개 송장번호 생성 완료"
MSG_FILE_SAVED: Final[str] = "✅ 파일 저장됨: {}"

# Error Messages
ERR_FILE_FORMAT: Final[str] = "파일 형식이 잘못되었습니다. .xls 또는 .xlsx 파일을 사용하세요."
ERR_FILE_TOO_LARGE: Final[str] = "파일이 너무 큽니다. 최대 크기: 100MB"
ERR_FILE_EMPTY: Final[str] = "파일이 비어있습니다. 데이터가 있는 파일을 선택하세요."
ERR_FILE_READ: Final[str] = "파일을 읽을 수 없습니다: {}"
ERR_GENERATION_FAILED: Final[str] = "송장 생성에 실패했습니다. 다시 시도하세요."
ERR_EXPORT_FAILED: Final[str] = "파일 저장에 실패했습니다: {}"
ERR_NO_FILE_SELECTED: Final[str] = "파일이 선택되지 않았습니다."
ERR_PERMISSION_DENIED: Final[str] = "파일에 접근할 권한이 없습니다."
