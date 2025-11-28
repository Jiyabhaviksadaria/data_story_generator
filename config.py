"""
Configuration settings for the Data Story Generator
"""

import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "outputs"
REPORTS_DIR = OUTPUT_DIR / "reports"

# Ensure directories exist
DATA_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)
REPORTS_DIR.mkdir(exist_ok=True)

# App Settings
APP_TITLE = "Interactive Data Story Generator"
APP_ICON = "📊"
MAX_FILE_SIZE_MB = 200

# Visualization Settings
DEFAULT_COLOR_SCHEME = ['#667eea', '#764ba2', '#f093fb', '#4facfe']
CHART_HEIGHT = 400

# Data Processing Settings
MAX_UNIQUE_VALUES_FOR_CATEGORICAL = 50
CORRELATION_THRESHOLD = 0.7
OUTLIER_THRESHOLD = 3  # Z-score threshold

# AI Settings
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
MODEL_NAME = "gpt-4o-mini"
MAX_TOKENS = 2000
